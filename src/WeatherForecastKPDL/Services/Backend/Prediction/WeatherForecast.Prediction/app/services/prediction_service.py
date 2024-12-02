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
from ..models import prediction

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PredictionService:
    def prepare_data(self, weather_data_list: List[prediction.WeatherData]):
        df = pd.DataFrame([vars(data) for data in weather_data_list])
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
        X_pressure, y_pressure = [], []
        X_wind, y_wind = [], []
        X_cloud, y_cloud = [], []  # cho mây
        step = observed_size - overlap_size
        
        for i in range(0, len(df) - observed_size - 1, step):
            # Cho nhiệt độ (dùng Humidity, Pressure, Cloud)
            features_temp = df.iloc[i:i + observed_size][['Humidity', 'PressureMb', 'Cloud']]
            target_temp = df.iloc[i + observed_size]['TempC']
            X_temp.append(features_temp.values)
            y_temp.append(target_temp)
            
            # Cho độ ẩm (dùng Temp, Pressure, Cloud)
            features_humidity = df.iloc[i:i + observed_size][['TempC','PressureMb', 'Cloud']]
            target_humidity = df.iloc[i + observed_size]['Humidity']
            X_humidity.append(features_humidity.values)
            y_humidity.append(target_humidity)
            
            # Cho áp suất (dùng TempC, Humidity, Cloud)
            features_pressure = df.iloc[i:i + observed_size][['TempC','Humidity', 'Cloud']]
            target_pressure = df.iloc[i + observed_size]['PressureMb']
            X_pressure.append(features_pressure.values)
            y_pressure.append(target_pressure)

            # Cho tốc độ gió (dùng TempC, Humidity, Cloud, PressureMb)
            features_wind = df.iloc[i:i + observed_size][['TempC','Humidity', 'Cloud', 'PressureMb']]
            target_wind = df.iloc[i + observed_size]['WindKph']
            X_wind.append(features_wind.values)
            y_wind.append(target_wind)

            # Cho mây (dùng TempC, Humidity, PressureMb)
            features_cloud = df.iloc[i:i + observed_size][['TempC','Humidity', 'PressureMb']]
            target_cloud = df.iloc[i + observed_size]['Cloud']
            X_cloud.append(features_cloud.values)
            y_cloud.append(target_cloud)
            
        return (np.array(X_temp), np.array(y_temp), 
                np.array(X_humidity), np.array(y_humidity),
                np.array(X_pressure), np.array(y_pressure),
                np.array(X_wind), np.array(y_wind),
                np.array(X_cloud), np.array(y_cloud))

    def train_model(self, data):
        logging.info("Bắt đầu quá trình huấn luyện mô hình...")
        df = self.prepare_data(data)
        
        logging.info("Tạo sequences cho training...")
        X_temp, y_temp, X_humidity, y_humidity, X_pressure, y_pressure, X_wind, y_wind, X_cloud, y_cloud = self.create_sequences(df)
        
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
        
        # Train model cho áp suất
        X_train_pressure, X_test_pressure, y_train_pressure, y_test_pressure = train_test_split(
            X_pressure, y_pressure, test_size=0.3, random_state=42
        )
        model_pressure = RandomForestRegressor(n_estimators=100, random_state=42)
        model_pressure.fit(X_train_pressure.reshape(X_train_pressure.shape[0], -1), y_train_pressure)
        score_pressure = model_pressure.score(X_test_pressure.reshape(X_test_pressure.shape[0], -1), y_test_pressure)
        logging.info(f"Score của mô hình áp suất: {score_pressure}")

        # Train model cho tốc độ gió
        X_train_wind, X_test_wind, y_train_wind, y_test_wind = train_test_split(
            X_wind, y_wind, test_size=0.3, random_state=42
        )
        model_wind = RandomForestRegressor(n_estimators=100, random_state=42)
        model_wind.fit(X_train_wind.reshape(X_train_wind.shape[0], -1), y_train_wind)
        score_wind = model_wind.score(X_test_wind.reshape(X_test_wind.shape[0], -1), y_test_wind)
        logging.info(f"Score của mô hình tốc độ gió: {score_wind}")

        # Train model cho mây
        X_train_cloud, X_test_cloud, y_train_cloud, y_test_cloud = train_test_split(
            X_cloud, y_cloud, test_size=0.3, random_state=42
        )
        model_cloud = RandomForestRegressor(n_estimators=100, random_state=42)
        model_cloud.fit(X_train_cloud.reshape(X_train_cloud.shape[0], -1), y_train_cloud)
        score_cloud = model_cloud.score(X_test_cloud.reshape(X_test_cloud.shape[0], -1), y_test_cloud)
        logging.info(f"Score của mô hình mây: {score_cloud}")
        
        logging.info("Lưu các mô hình...")
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'trained_models')
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump(model_temp, os.path.join(model_dir, 'temp_prediction_model.joblib'))
        joblib.dump(model_humidity, os.path.join(model_dir, 'humidity_prediction_model.joblib'))
        joblib.dump(model_pressure, os.path.join(model_dir, 'pressure_prediction_model.joblib'))
        joblib.dump(model_wind, os.path.join(model_dir, 'wind_prediction_model.joblib'))
        joblib.dump(model_cloud, os.path.join(model_dir, 'cloud_prediction_model.joblib'))
        
        logging.info("Hoàn thành quá trình training!")
        return {
            'temperature_score': score_temp,
            'humidity_score': score_humidity,
            'pressure_score': score_pressure,
            'wind_score': score_wind,
            'cloud_score': score_cloud
        }
    
    def predict(self, weather_data: List[prediction.WeatherData]):
        logging.info("Bắt đầu quá trình dự đoán...")
        try:
            # Chuyển đổi dữ liệu từ request thành DataFrame
            df = pd.DataFrame([data.model_dump() for data in weather_data])
            df['Time'] = pd.to_datetime(df['Time'])
            
            if len(df) < 7:
                raise ValueError(f"Không đủ dữ liệu để dự đoán. Cần ít nhất 7 ngày, hiện có {len(df)} ngày.")
            
            # Lấy 7 bản ghi gần nhất để dự đoán
            recent_data = df.tail(7)
            
            # Chuẩn bị features cho dự đoán
            features_temp = recent_data[['Humidity', 'PressureMb', 'Cloud']].values.reshape(1, -1)
            features_humidity = recent_data[['TempC', 'PressureMb', 'Cloud']].values.reshape(1, -1)
            features_pressure = recent_data[['TempC', 'Humidity', 'Cloud']].values.reshape(1, -1)
            features_wind = recent_data[['TempC', 'Humidity', 'Cloud', 'PressureMb']].values.reshape(1, -1)
            features_cloud = recent_data[['TempC', 'Humidity', 'PressureMb']].values.reshape(1, -1)
            
            # Load và sử dụng các model
            model_dir = os.path.join(os.path.dirname(__file__), '..', 'trained_models')
            model_temp = joblib.load(os.path.join(model_dir, 'temp_prediction_model.joblib'))
            model_humidity = joblib.load(os.path.join(model_dir, 'humidity_prediction_model.joblib'))
            model_pressure = joblib.load(os.path.join(model_dir, 'pressure_prediction_model.joblib'))
            model_wind = joblib.load(os.path.join(model_dir, 'wind_prediction_model.joblib'))
            model_cloud = joblib.load(os.path.join(model_dir, 'cloud_prediction_model.joblib'))
            
            # Dự đoán
            temp_prediction = model_temp.predict(features_temp)
            humidity_prediction = model_humidity.predict(features_humidity)
            pressure_prediction = model_pressure.predict(features_pressure)
            wind_prediction = model_wind.predict(features_wind)
            cloud_prediction = model_cloud.predict(features_cloud)
            
            return {
                'predicted_temperature': float(temp_prediction[0]),
                'predicted_humidity': float(humidity_prediction[0]),
                'predicted_pressure': float(pressure_prediction[0]),
                'predicted_wind': float(wind_prediction[0]),
                'predicted_cloud': float(cloud_prediction[0])
            }
            
        except Exception as e:
            logging.error(f"Lỗi trong quá trình dự đoán: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
