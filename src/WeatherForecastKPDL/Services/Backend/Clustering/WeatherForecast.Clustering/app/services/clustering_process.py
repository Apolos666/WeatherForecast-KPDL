import pandas as pd
from typing import List
import numpy as np

from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler
from ..models.clustering import (
    Centroid,
    HourlyWeatherData,
    SeasonProbability,
    SpiderChartData
)
from ..core.logging import logger
from ..services.database_api import DatabaseApiService


class WeatherClusteringService:
    def __init__(self):
        logger.info("Khởi tạo WeatherAnalysisService")
        self.analysis_types = {
            'spider_chart': self.process_spider_chart
        }
        self.database_api = DatabaseApiService()

    async def process_spider_chart(self, hourly_data: List[HourlyWeatherData]) -> List[SpiderChartData]:
        logger.info(
            f"Bắt đầu phân cụm dữ liệu cho spider chart với {len(hourly_data)} bản ghi")
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
            filtered_min_max = daily_data[(daily_data['TempC'] == min_temp) | (
                daily_data['TempC'] == max_temp)]

            # Lấy ra 2 label tượng trưng cho nhiệt độ min và max
            deleted_labels = np.unique(filtered_min_max['kmean_label'])

            # Xoá 2 label trên và chỉ lấy 2 label ở giữa
            spring_antumn_labels = list(
                set(unique_labels) - set(deleted_labels))
            filtered_labels = [int(x) for x in spring_antumn_labels]

            # Add half_year column
            # Thay đổi từ daily_data.date thành daily_data.index
            daily_data['half_year'] = daily_data.index.month.map(
                lambda x: 'First' if x <= 6 else 'Second')

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

            daily_data['kmean_label'] = daily_data.apply(
                lambda row: customize_kmean_label(row['kmean_label'], row['half_year']), axis=1)

            winter_label = filtered_min_max[filtered_min_max['TempC']
                                            == min_temp]['kmean_label'].values[0]
            summer_label = filtered_min_max[filtered_min_max['TempC']
                                            == max_temp]['kmean_label'].values[0]

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
            all_seasons = pd.DataFrame(
                {'Season': ['Mùa Đông', 'Mùa Hạ', 'Mùa Xuân', 'Mùa Thu'], 'NumberOfDays': [0, 0, 0, 0]})

            # Tính số ngày cho mỗi mùa
            season_counts = daily_data['seasonal'].value_counts().reset_index()
            season_counts.columns = ['Season', 'NumberOfDays']

            # Cập nhật số ngày cho mỗi mùa trong DataFrame all_seasons
            for _, row in season_counts.iterrows():
                all_seasons.loc[all_seasons['Season'] ==
                                row['Season'], 'NumberOfDays'] = row['NumberOfDays']

            for _, row in all_seasons.iterrows():
                logger.info(
                    f"Số ngày của {row['Season']}: {row['NumberOfDays']}")

            # Tạo danh sách SpiderChartData
            spider_chart_data = []
            for _, row in all_seasons.iterrows():
                year = daily_data.index.year[0]
                spider_chart_data.append(SpiderChartData(
                    Year=year, Season=row['Season'], NumberOfDays=row['NumberOfDays']))

            return spider_chart_data

        except Exception as e:
            logger.error(f"Lỗi khi phân cụm dữ liệu: {str(e)}")
            raise

    async def process_centroid(self, hourly_data: List[HourlyWeatherData]) -> Centroid:
        logger.info(f"Bắt đầu xử lý centroid với {len(hourly_data)} bản ghi")
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
            filtered_min_max = daily_data[(daily_data['TempC'] == min_temp) | (
                daily_data['TempC'] == max_temp)]

            # Lấy ra 2 label tượng trưng cho nhiệt độ min và max
            deleted_labels = np.unique(filtered_min_max['kmean_label'])

            # Xoá 2 label trên và chỉ lấy 2 label ở giữa
            spring_antumn_labels = list(
                set(unique_labels) - set(deleted_labels))
            filtered_labels = [int(x) for x in spring_antumn_labels]

            # Add half_year column
            # Thay đổi từ daily_data.date thành daily_data.index
            daily_data['half_year'] = daily_data.index.month.map(
                lambda x: 'First' if x <= 6 else 'Second')

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

            daily_data['kmean_label'] = daily_data.apply(
                lambda row: customize_kmean_label(row['kmean_label'], row['half_year']), axis=1)

            winter_label = filtered_min_max[filtered_min_max['TempC']
                                            == min_temp]['kmean_label'].values[0]
            summer_label = filtered_min_max[filtered_min_max['TempC']
                                            == max_temp]['kmean_label'].values[0]

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

            # Lấy ra số ngày mùa xuân, hạ, thu, đông
            # 1. Lấy ra label mùa hạ (có nhiệt độ cao nhất) - Lấy dựa vào max_temp
            summer_data = daily_data[daily_data['TempC'] == max_temp]
            summer_quantity = len(
                daily_data[daily_data['kmean_label'] == summer_label])
            # 2. Lấy ra label mùa đông (có nhiêt độ thấp nhất) - Lấy dựa vào min_temp
            winter_data = daily_data[daily_data['TempC'] == min_temp]
            winter_label = winter_data.iloc[0]['kmean_label']
            # 3. Lấy ra label mùa xuân - dựa vào half_year và spring_autumn_labels
            spring_data = daily_data[(daily_data['half_year'] == 'First') & (
                daily_data['kmean_label'].isin(spring_antumn_labels))]
            spring_label = spring_data.iloc[0]['kmean_label']
            # 4. Lấy ra label mùa thu - dựa vào half_year và spring_autumn_labels
            autumn_data = daily_data[(daily_data['half_year'] == 'Second') & (
                daily_data['kmean_label'].isin(spring_antumn_labels))]
            autumn_label = autumn_data.iloc[0]['kmean_label']

            # Lấy ra centroid cho mùa xuân, hạ, thu, đông
            # 1. Lấy ra nhiệt độ max của từng mùa
            cluster_temp_ranges = daily_data.groupby(
                'kmean_label')['TempC'].agg(['min', 'max']).reset_index()
            cluster_temp_ranges = cluster_temp_ranges.sort_values(
                by='max', ascending=True)
            centroids = (scaler.inverse_transform(
                kmeans.cluster_centers_)).ravel()
            cluster_temp_ranges['centroid'] = np.sort(centroids)

            spring_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label']
                                                  == spring_label].iloc[0]['centroid']
            summer_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label']
                                                  == summer_label].iloc[0]['centroid']
            autumn_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label']
                                                  == autumn_label].iloc[0]['centroid']
            winter_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label']
                                                  == winter_label].iloc[0]['centroid']

            centroid = Centroid(SpringCentroid=spring_centroid, SummerCentroid=summer_centroid,
                                AutumnCentroid=autumn_centroid, WinterCentroid=winter_centroid)

            return centroid
        except Exception as e:
            logger.error(f"Lỗi khi phân cụm dữ liệu: {str(e)}")
            raise

    async def process_prediction_with_probability(self) -> SeasonProbability:
        try:
            logger.info("Bắt đầu dự đoán mùa dựa trên nhiệt độ dự đoán")
            predict_data = await self.database_api.get_predict_temperature_next_day()
            predict_temp = predict_data.predicted_temperature

            centroids_data = await self.database_api.get_centroid()
            centroids = [
                centroids_data.springCentroid,
                centroids_data.summerCentroid,
                centroids_data.autumnCentroid,
                centroids_data.winterCentroid
            ]

            # Calculate distances from input temperature to each centroid
            distance = np.abs(np.array(centroids) - predict_temp)

            # Convert distances to probabilities (inverse of distance)
            # Add small value to avoid division by zero
            inverse_distances = 1 / (distance + 1e-10)
            probabilities = inverse_distances / np.sum(inverse_distances)

            seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
            probability_dict = dict(zip(seasons, probabilities))

            # Đảm bảo probability_dict chứa tất cả các khóa cần thiết
            if not all(season in probability_dict for season in seasons):
                raise ValueError("probability_dict thiếu một hoặc nhiều khóa cần thiết")

            spring_prob = probability_dict['Spring']
            summer_prob = probability_dict['Summer']
            autumn_prob = probability_dict['Autumn']
            winter_prob = probability_dict['Winter']

            season_probability = SeasonProbability(
                Spring=spring_prob,
                Summer=summer_prob,
                Autumn=autumn_prob,
                Winter=winter_prob
            ) 

            logger.info(f"Xác suất cho mỗi mùa: {season_probability}")

            return season_probability

        except Exception as e:
            logger.error(f"Lỗi khi dự đoán mùa dựa trên nhiệt độ: {str(e)}")
            raise
