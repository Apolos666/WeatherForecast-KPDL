import os
import pandas as pd
import numpy as np
from kafka import KafkaConsumer
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from datetime import timedelta
import logging
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WeatherData(BaseModel):
    Time: str
    TempC: float
    Humidity: int
    PressureMb: float
    WindKph: float
    Cloud: int

class PredictionService:
    def __init__(self):
        logging.info("Khởi tạo Kafka Consumer cho training...")
        self.consumer_train = KafkaConsumer(
            os.getenv("KAFKA_TOPIC", "weather-mysql.defaultdb.Hours"),
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092"),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=os.getenv("KAFKA_GROUP_ID", "weather_prediction_train_group"),
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=10000,
            session_timeout_ms=10000,
            request_timeout_ms=11000
        )

    def prepare_data(self, consumer):
        logging.info("Bắt đầu thu thập dữ liệu từ Kafka...")
        data = []
        message_count = 0
        
        for message in consumer:
            if message.value['payload']['after'] is not None:
                message_count += 1
                weather_data = message.value['payload']['after']
                data.append({
                    'Time': weather_data['Time'],
                    'TempC': weather_data['TempC'],
                    'Humidity': weather_data['Humidity'],
                    'PressureMb': weather_data['PressureMb'],
                    'WindKph': weather_data['WindKph'],
                    'Cloud': weather_data['Cloud']
                })
        
        logging.info(f"Đã thu thập xong {message_count} messages")
        df = pd.DataFrame(data)
        df['Time'] = pd.to_datetime(df['Time'])
        
        # Nhóm dữ liệu theo ngày
        df_daily = df.groupby(df['Time'].dt.date).agg({
            'TempC': 'mean',
            'Humidity': 'mean',
            'PressureMb': 'mean',
            'WindKph': 'mean',
            'Cloud': 'mean'
        }).reset_index()
        
        df_daily['Time'] = pd.to_datetime(df_daily['Time'])
        return df_daily

    def create_sequences(self, df, observed_size=7, overlap_size=2):
        X_temp, y_temp = [], []  # cho nhiệt độ
        X_humidity, y_humidity = [], []  # cho độ ẩm
        X_cloud, y_cloud = [], []  # cho mây
        step = observed_size - overlap_size
        
        for i in range(0, len(df) - observed_size - 1, step):
            # Cho nhiệt độ (dùng Humidity, Pressure, Wind)
            features_temp = df.iloc[i:i + observed_size][['Humidity', 'PressureMb', 'WindKph']]
            target_temp = df.iloc[i + observed_size]['TempC']
            X_temp.append(features_temp.values)
            y_temp.append(target_temp)
            
            # Cho độ ẩm (dùng Pressure, Wind)
            features_humidity = df.iloc[i:i + observed_size][['PressureMb', 'WindKph']]
            target_humidity = df.iloc[i + observed_size]['Humidity']
            X_humidity.append(features_humidity.values)
            y_humidity.append(target_humidity)
            
            # Cho mây (dùng Humidity, Wind)
            features_cloud = df.iloc[i:i + observed_size][['Humidity', 'WindKph']]
            target_cloud = df.iloc[i + observed_size]['Cloud']
            X_cloud.append(features_cloud.values)
            y_cloud.append(target_cloud)
            
        return (np.array(X_temp), np.array(y_temp), 
                np.array(X_humidity), np.array(y_humidity),
                np.array(X_cloud), np.array(y_cloud))

    def train_model(self):
        logging.info("Bắt đầu quá trình huấn luyện mô hình...")
        df = self.prepare_data(self.consumer_train)  # Sử dụng consumer cho training
        
        logging.info("Tạo sequences cho training...")
        X_temp, y_temp, X_humidity, y_humidity, X_cloud, y_cloud = self.create_sequences(df)
        
        logging.info("Training mô hình dự đoán nhiệt độ...")
        X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(
            X_temp, y_temp, test_size=0.3, random_state=42
        )
        model_temp = RandomForestRegressor(n_estimators=100, random_state=42)
        model_temp.fit(X_train_temp.reshape(X_train_temp.shape[0], -1), y_train_temp)
        score_temp = model_temp.score(X_test_temp.reshape(X_test_temp.shape[0], -1), y_test_temp)
        logging.info(f"Score của mô hình nhiệt độ: {score_temp}")
        
        # Train model cho độ ẩm
        X_train_humidity, X_test_humidity, y_train_humidity, y_test_humidity = train_test_split(
            X_humidity, y_humidity, test_size=0.3, random_state=42
        )
        model_humidity = RandomForestRegressor(n_estimators=100, random_state=42)
        model_humidity.fit(X_train_humidity.reshape(X_train_humidity.shape[0], -1), y_train_humidity)
        score_humidity = model_humidity.score(X_test_humidity.reshape(X_test_humidity.shape[0], -1), y_test_humidity)
        logging.info(f"Score của mô hình độ ẩm: {score_humidity}")
        
        # Train model cho mây
        X_train_cloud, X_test_cloud, y_train_cloud, y_test_cloud = train_test_split(
            X_cloud, y_cloud, test_size=0.3, random_state=42
        )
        model_cloud = RandomForestRegressor(n_estimators=100, random_state=42)
        model_cloud.fit(X_train_cloud.reshape(X_train_cloud.shape[0], -1), y_train_cloud)
        score_cloud = model_cloud.score(X_test_cloud.reshape(X_test_cloud.shape[0], -1), y_test_cloud)
        logging.info(f"Score của mô hình mây: {score_cloud}")
        
        logging.info("Lưu các mô hình...")
        joblib.dump(model_temp, 'temp_prediction_model.joblib')
        joblib.dump(model_humidity, 'humidity_prediction_model.joblib')
        joblib.dump(model_cloud, 'cloud_prediction_model.joblib')
        
        logging.info("Hoàn thành quá trình training!")
        return {
            'temperature_score': score_temp,
            'humidity_score': score_humidity,
            'cloud_score': score_cloud
        }

    def predict(self, weather_data: List[WeatherData]):
        logging.info("Bắt đầu quá trình dự đoán...")
        try:
            # Chuyển đổi dữ liệu từ request thành DataFrame
            df = pd.DataFrame([data.dict() for data in weather_data])
            df['Time'] = pd.to_datetime(df['Time'])
            
            if len(df) < 7:
                raise ValueError(f"Không đủ dữ liệu để dự đoán. Cần ít nhất 7 ngày, hiện có {len(df)} ngày.")
            
            # Lấy 7 bản ghi gần nhất để dự đoán
            recent_data = df.tail(7)
            
            # Chuẩn bị features cho dự đoán
            features_temp = recent_data[['Humidity', 'PressureMb', 'WindKph']].values.reshape(1, -1)
            features_humidity = recent_data[['PressureMb', 'WindKph']].values.reshape(1, -1)
            features_cloud = recent_data[['Humidity', 'WindKph']].values.reshape(1, -1)
            
            # Load và sử dụng các model
            model_temp = joblib.load('temp_prediction_model.joblib')
            model_humidity = joblib.load('humidity_prediction_model.joblib')
            model_cloud = joblib.load('cloud_prediction_model.joblib')
            
            # Dự đoán
            temp_prediction = model_temp.predict(features_temp)
            humidity_prediction = model_humidity.predict(features_humidity)
            cloud_prediction = model_cloud.predict(features_cloud)
            
            return {
                'predicted_temperature': float(temp_prediction[0]),
                'predicted_humidity': float(humidity_prediction[0]),
                'predicted_cloud': float(cloud_prediction[0])
            }
            
        except Exception as e:
            logging.error(f"Lỗi trong quá trình dự đoán: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
