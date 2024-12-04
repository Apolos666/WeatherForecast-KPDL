import traceback
import pandas as pd
from typing import List
import numpy as np

from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler
from ..models.clustering import (
    Centroid,
    ClusteringResultData,
    HourlyWeatherData,
    SeasonProbability,
    SeasonQuantityData,
)
from ..core.logging import logger
from ..services.database_api import DatabaseApiService


class WeatherClusteringService:
    def __init__(self):
        logger.info("Khởi tạo WeatherAnalysisService")
        self.analysis_types = {
            'spider_chart': self.process_clustering_data
        }
        self.database_api = DatabaseApiService()

    @staticmethod
    def customize_kmean_label(kmean_label, half_year, labels):
        if half_year == 'First':
            if kmean_label in labels:
                return labels[0]
            return kmean_label
        else:
            if kmean_label in labels:
                return labels[1]
            return kmean_label

    def _get_season_quantity(self, data, season_labels, year) -> SeasonQuantityData:
        spring_quantity = len(
            data[data['kmean_label'] == season_labels['spring']])
        summer_quantity = len(
            data[data['kmean_label'] == season_labels['summer']])
        autumn_quantity = len(
            data[data['kmean_label'] == season_labels['autumn']])
        winter_quantity = len(
            data[data['kmean_label'] == season_labels['winter']])

        return SeasonQuantityData(
            year=year,
            spring_quantity=spring_quantity,
            summer_quantity=summer_quantity,
            autumn_quantity=autumn_quantity,
            winter_quantity=winter_quantity
        )

    async def process_clustering_data(self, hourly_data: List[HourlyWeatherData]):
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

            if daily_data.isnull().any().any():
                logger.warning("Có giá trị null trong kết quả phân tích")

            daily_data.columns = ['avg_temp']

            # ########################################################################################################################
            # Bắt đầu clustering
            features = daily_data[['avg_temp']].to_numpy().reshape(-1, 1)

            # Chuẩn hóa dữ liệu
            scaler = StandardScaler()
            normalized_features = scaler.fit_transform(features)

            # Apply KMeans clustering
            kmeans = KMeans(n_clusters=4, random_state=42)
            daily_data['kmean_label'] = kmeans.fit_predict(normalized_features)

            # Lấy labels
            unique_labels = np.unique(kmeans.labels_)

            # Lấy giá trị min và max avg_temp
            min_temp = daily_data['avg_temp'].min()
            max_temp = daily_data['avg_temp'].max()

            # Lấy trường có giá trị avg_temp min và max
            filtered_min_max = daily_data[(daily_data['avg_temp'] == min_temp) | (
                daily_data['avg_temp'] == max_temp)]

            # Lấy ra 2 label tượng trưng cho nhiệt độ min và max
            summer_winter_labels = np.unique(filtered_min_max['kmean_label'])

            # Xoá 2 label trên và chỉ lấy 2 label ở giữa
            spring_antumn_labels = list(
                set(unique_labels) - set(summer_winter_labels))
            filtered_labels = [int(x) for x in spring_antumn_labels]

            # Add half_year column
            # Thay đổi từ daily_data.date thành daily_data.index
            daily_data['half_year'] = daily_data.index.month.map(
                lambda x: 'First' if x <= 6 else 'Second')

            daily_data['kmean_label'] = daily_data.apply(
                lambda row: WeatherClusteringService.customize_kmean_label(
                    row['kmean_label'], 
                    row['half_year'], 
                    labels=filtered_labels
                ), 
                axis=1
            )

            # Lấy ra số ngày mùa xuân, hạ, thu, đông
            # 1. Lấy ra label mùa hạ (có nhiệt độ cao nhất) - Lấy dựa vào max_temp
            summer_data = daily_data[daily_data['avg_temp'] == max_temp]
            summer_label = summer_data.iloc[0]['kmean_label']
            # 2. Lấy ra label mùa đông (có nhiêt độ thấp nhất) - Lấy dựa vào min_temp
            winter_data = daily_data[daily_data['avg_temp'] == min_temp]
            winter_label = winter_data.iloc[0]['kmean_label']
            # 3. Lấy ra label mùa xuân - dựa vào half_year và spring_autumn_labels
            spring_data = daily_data[(daily_data['half_year'] == 'First') & (
                daily_data['kmean_label'].isin(spring_antumn_labels))]
            spring_label = spring_data.iloc[0]['kmean_label']
            # 4. Lấy ra label mùa thu - dựa vào half_year và spring_autumn_labels
            autumn_data = daily_data[(daily_data['half_year'] == 'Second') & (
                daily_data['kmean_label'].isin(spring_antumn_labels))]
            autumn_label = autumn_data.iloc[0]['kmean_label']

            season_labels = {
                "spring": spring_label,
                "summer": summer_label,
                "autumn": autumn_label,
                "winter": winter_label
            }

            # Nhóm dữ liệu lại theo năm
            dailydatas_by_year = {
                year: group for year, group in daily_data.groupby(daily_data.index.year)}

            # Tiến hành lấy dữ liệu số lượng mùa xuân, hạ, thu, đông cho từng năm riêng biệt
            season_quantity_result = []
            for year, year_df in dailydatas_by_year.items():
                logger.info(f"Tiến hành lấy dữ liệu từng mùa cho năm {year}")
                result = self._get_season_quantity(
                    data=year_df, season_labels=season_labels, year=year)
                season_quantity_result.append(result)

            logger.info(
                f"Dữ liệu số lượng mùa sau khi tiến hành phân cụm {season_quantity_result}")

            # ########################################################################################################################
            # Lấy ra centroid cho mùa xuân, hạ, thu, đông
            # Nhận thấy sự tăng dần nhiệt độ max của mùa là sự tăng dần giá trị trong centroids
            # 1. Lấy ra nhiệt độ max của từng mùa
            cluster_temp_ranges = daily_data.groupby(
                'kmean_label')['avg_temp'].agg(['min', 'max']).reset_index()
            # 2. Sắp xếp theo chiều tăng dần của nhiệt độ max
            cluster_temp_ranges = cluster_temp_ranges.sort_values(
                by='max', ascending=True)
            # 3. Chuyển dữ liệu centroid bị chuẩn hóa về nhiệt độ gốc
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
            centroid_result = Centroid(
                  SpringCentroid=spring_centroid,
                  SummerCentroid=summer_centroid,
                  AutumnCentroid=autumn_centroid,
                  WinterCentroid=winter_centroid
            )

            logger.info(
                f"Dữ liệu centroids sau khi tiến hành phân cụm {season_quantity_result}")
            # ########################################################################################################################

            result = ClusteringResultData(
                centroids=centroid_result,
                quantity=season_quantity_result
            )

            logger.info(f"Kết quả phân tích: {result.model_dump()}")
            return result

        except Exception as e:
            logger.error(f"Lỗi khi phân cụm hàng ngày: {str(e)}")
            logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
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
                raise ValueError(
                    "probability_dict thiếu một hoặc nhiều khóa cần thiết")

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
