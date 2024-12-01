import pandas as pd
from typing import List
import numpy as np

from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler
from ..models.clustering import (
    HourlyWeatherData, 
    SpiderChartData
)
from ..core.logging import logger

class WeatherClusteringService:
    def __init__(self):
        logger.info("Khởi tạo WeatherAnalysisService")
        self.analysis_types = {
            'spider_chart': self.process_spider_chart,
            # 'seasonal': self.analyze_seasonal_data,
            # 'correlation': self.process_spider_chart
        }

    def process_spider_chart(self, hourly_data: List[HourlyWeatherData]) -> List[SpiderChartData]:
        logger.info(f"Bắt đầu phân cụm dữ liệu cho spider chart với {len(hourly_data)} bản ghi")
        try:
            df = pd.DataFrame([data.model_dump() for data in hourly_data])
            
            if df.empty:
                raise ValueError("Không có dữ liệu để phân tích")
            
            df['Time'] = pd.to_datetime(df['Time'])
            df.set_index('Time', inplace=True)
            
            # Resample to daily data
            daily_data = df.resample('D').agg({
                'TempC': 'mean',
            })

            # Chuẩn hóa dữ liệu
            features = ['TempC']
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(daily_data[features])
            
            # Apply KMeans clustering
            kmeans = KMeans(n_clusters=4, random_state=42)
            daily_data['kmean_label'] = kmeans.fit_predict(scaled_features)

            unique_labels = np.unique(kmeans.labels_)

            # Lấy giá trị min và max tempC
            min_temp = daily_data['TempC'].min()
            max_temp = daily_data['TempC'].max()

            # Lấy trường có giá trị tempC min và max
            filtered_min_max = daily_data[(daily_data['TempC'] == min_temp) | (daily_data['TempC'] == max_temp)]

            # Lấy ra 2 label tượng trưng cho nhiệt độ min và max
            deleted_labels = np.unique(filtered_min_max['kmean_label'])

            # Xoá 2 label trên và chỉ lấy 2 label ở giữa
            needed_labels = list(set(unique_labels) - set(deleted_labels))
            filtered_labels = [int(x) for x in needed_labels]
            
            # Add half_year column
            # Thay đổi từ daily_data.date thành daily_data.index
            daily_data['half_year'] = daily_data.index.month.map(lambda x: 'First' if x <= 6 else 'Second')
            
            # Define season labeling function
            def customize_kmean_label(kmean_label, half_year):
                if half_year == 'First':
                    if kmean_label in filtered_labels:
                        return filtered_labels[0]
                    return kmean_label
                else:
                    if kmean_label in filtered_labels:
                        return filtered_labels[1]
                    return kmean_label

            daily_data['kmean_label'] = daily_data.apply(lambda row: customize_kmean_label(row['kmean_label'], row['half_year']), axis=1)

            winter_label = filtered_min_max[filtered_min_max['TempC'] == min_temp]['kmean_label'].values[0]
            summer_label = filtered_min_max[filtered_min_max['TempC'] == max_temp]['kmean_label'].values[0]

            def assign_season(row):
                if row['kmean_label'] == winter_label:
                    return 'Mùa Đông'
                elif row['kmean_label'] == summer_label:
                    return 'Mùa Hạ'
                elif row['kmean_label'] == filtered_labels[0]:
                    return 'Mùa Xuân'
                elif row['kmean_label'] == filtered_labels[1]:
                    return 'Mùa Thu'

            daily_data['seasonal'] = daily_data.apply(assign_season, axis=1)

            # Tạo DataFrame chứa tất cả các mùa
            all_seasons = pd.DataFrame({'Season': ['Mùa Đông', 'Mùa Hạ', 'Mùa Xuân', 'Mùa Thu'], 'NumberOfDays': [0, 0, 0, 0]})

            # Tính số ngày cho mỗi mùa
            season_counts = daily_data['seasonal'].value_counts().reset_index()
            season_counts.columns = ['Season', 'NumberOfDays']

            # Cập nhật số ngày cho mỗi mùa trong DataFrame all_seasons
            for _, row in season_counts.iterrows():
                all_seasons.loc[all_seasons['Season'] == row['Season'], 'NumberOfDays'] = row['NumberOfDays']

            for _, row in all_seasons.iterrows():
                logger.info(f"Số ngày của {row['Season']}: {row['NumberOfDays']}")    

            # Tạo danh sách SpiderChartData
            spider_chart_data = []
            for _, row in all_seasons.iterrows():
                year = daily_data.index.year[0]
                spider_chart_data.append(SpiderChartData(Year=year, Season=row['Season'], NumberOfDays=row['NumberOfDays']))

            return spider_chart_data

        except Exception as e:
            logger.error(f"Lỗi khi phân cụm dữ liệu: {str(e)}")
            raise
