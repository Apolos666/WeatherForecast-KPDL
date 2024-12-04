import pandas as pd
from typing import List
from ..models.analysis import (
    HourlyWeatherData, 
    DailyAnalysis,
    SeasonalAnalysis,
    CorrelationAnalysis
)
from ..core.logging import logger

class WeatherAnalysisService:
    def __init__(self):
        logger.info("Khởi tạo WeatherAnalysisService")
        self.analysis_types = {
            'daily': self.analyze_daily_data,
            'seasonal': self.analyze_seasonal_data,
            'correlation': self.analyze_correlation
        }

    def analyze_daily_data(self, hourly_data: List[HourlyWeatherData]) -> DailyAnalysis:
        logger.info(f"Bắt đầu phân tích dữ liệu hàng ngày với {len(hourly_data)} bản ghi")
        try:
            df = pd.DataFrame([vars(data) for data in hourly_data])
            
            # Kiểm tra dữ liệu đầu vào
            if df.empty:
                raise ValueError("Không có dữ liệu để phân tích")
            
            # Kiểm tra giá trị null
            if df['TempC'].isnull().any() or df['Humidity'].isnull().any():
                logger.warning("Có giá trị null trong dữ liệu")
            
            df['Time'] = pd.to_datetime(df['Time'])
            df.set_index('Time', inplace=True)
            
            daily_data = pd.DataFrame()
            daily_data['avg_temp'] = df['TempC'].resample('D').mean()
            daily_data['avg_humidity'] = df['Humidity'].resample('D').mean()
            daily_data['total_precip'] = df['PrecipMm'].resample('D').sum()
            daily_data['avg_wind'] = df['WindKph'].resample('D').mean()
            daily_data['avg_pressure'] = df['PressureMb'].resample('D').mean()
            
            # Kiểm tra kết quả phân tích
            if daily_data.isnull().any().any():
                logger.warning("Có giá trị null trong kết quả phân tích")
            
            result = DailyAnalysis(
                date=daily_data.index[0].strftime('%Y-%m-%d'),
                avg_temp=round(float(daily_data['avg_temp'][0]), 2),
                avg_humidity=round(float(daily_data['avg_humidity'][0]), 2),
                total_precip=round(float(daily_data['total_precip'][0]), 2),
                avg_wind=round(float(daily_data['avg_wind'][0]), 2),
                avg_pressure=round(float(daily_data['avg_pressure'][0]), 2)
            )
            
            logger.info(f"Kết quả phân tích: {result.model_dump()}")
            return result
        except Exception as e:
            logger.error(f"Lỗi khi phân tích dữ liệu hàng ngày: {str(e)}")
            raise

    def analyze_seasonal_data(self, data: List[HourlyWeatherData]) -> SeasonalAnalysis:
        logger.info(f"Bắt đầu phân tích dữ liệu theo mùa với {len(data)} bản ghi")
        try:
            df = pd.DataFrame([vars(d) for d in data])
            
            if df.empty:
                raise ValueError("Không có dữ liệu để phân tích")

            # Convert Time to datetime and set as index
            df['Time'] = pd.to_datetime(df['Time'])
            df.set_index('Time', inplace=True)

            # Perform daily resampling with proper aggregations
            seasonal_data = df.resample('D').agg({
                'TempC': ['mean', 'max', 'min'],
                'Humidity': 'mean',
                'PrecipMm': 'sum',
                'WindKph': 'mean',
                'PressureMb': 'mean'
            })

            # Flatten column names
            seasonal_data.columns = ['avg_temp', 'max_temp', 'min_temp', 'avg_humidity', 
                                'total_precip', 'avg_wind', 'avg_pressure']
            
            seasonal_data = seasonal_data.reset_index()

            # Extract date components
            seasonal_data['date'] = seasonal_data['Time'].dt.strftime('%Y-%m-%d')
            seasonal_data['year'] = seasonal_data['Time'].dt.year
            seasonal_data['quarter'] = seasonal_data['Time'].dt.quarter

            # Convert to list of SeasonalAnalysis objects
            seasonal_analysis_list = []

            for _, row in seasonal_data.iterrows():
                analysis = SeasonalAnalysis(
                    date=row['date'],
                    year=int(row['year']),
                    quarter=int(row['quarter']),  # Note: matches the typo in your model
                    avg_temp=float(row['avg_temp']),
                    max_temp=float(row['max_temp']),
                    min_temp=float(row['min_temp']),
                    avg_humidity=float(row['avg_humidity']),
                    total_precip=float(row['total_precip']),
                    avg_wind=float(row['avg_wind']),
                    avg_pressure=float(row['avg_pressure'])
                )
                seasonal_analysis_list.append(analysis)

                logger.info(f"Đã phân tích và chuyển dữ liệu hourly thành {len(seasonal_analysis_list)} dòng daily có chứa quarter")

            return seasonal_analysis_list
            
        except Exception as e:
            logger.error(f"Lỗi khi phân tích dữ liệu theo mùa: {str(e)}")
            raise

    def analyze_correlation(self, hourly_data: List[HourlyWeatherData]) -> List[CorrelationAnalysis]:
        logger.info(f"Bắt đầu phân tích tương quan với {len(hourly_data)} bản ghi")
        try:
            df = pd.DataFrame([data.model_dump() for data in hourly_data])
            
            if df.empty:
                raise ValueError("Không có dữ liệu để phân tích")
            
            df['Time'] = pd.to_datetime(df['Time'])
            df['Year'] = df['Time'].dt.year
            
            # Sort by time and log the first and last timestamps
            df = df.sort_values('Time')
            logger.info(f"First timestamp: {df['Time'].iloc[0]}")
            logger.info(f"Last timestamp: {df['Time'].iloc[-1]}")
            
            # Variables for correlation analysis
            variables = ['TempC', 'Humidity', 'PressureMb', 'WindKph', 'Cloud']
            
            results = []
            # Group by year and calculate correlations
            for year, year_data in df.groupby('Year'):
                correlations = {}
                for i in range(len(variables)):
                    for j in range(len(variables)):
                        if i != j:
                            var1 = variables[i]
                            var2 = variables[j]
                            corr_name = f"{var1.lower()}_{var2.lower()}_corr"
                            correlations[corr_name] = round(year_data[var1].corr(year_data[var2]), 3)
                
                result = CorrelationAnalysis(
                    date=year_data['Time'].iloc[0].strftime('%Y-%m-%d'),
                    temp_humidity_corr=correlations.get('tempc_humidity_corr', None),
                    temp_pressure_corr=correlations.get('tempc_pressuremb_corr', None),
                    temp_wind_corr=correlations.get('tempc_windkph_corr', None),
                    temp_cloud_corr=correlations.get('tempc_cloud_corr', None),
                    humidity_temp_corr=correlations.get('humidity_tempc_corr', None),
                    humidity_pressure_corr=correlations.get('humidity_pressuremb_corr', None),
                    humidity_wind_corr=correlations.get('humidity_windkph_corr', None),
                    humidity_cloud_corr=correlations.get('humidity_cloud_corr', None),
                    pressure_temp_corr=correlations.get('pressuremb_tempc_corr', None),
                    pressure_humidity_corr=correlations.get('pressuremb_humidity_corr', None),
                    pressure_wind_corr=correlations.get('pressuremb_windkph_corr', None),
                    pressure_cloud_corr=correlations.get('pressuremb_cloud_corr', None),
                    wind_temp_corr=correlations.get('windkph_tempc_corr', None),
                    wind_humidity_corr=correlations.get('windkph_humidity_corr', None),
                    wind_pressure_corr=correlations.get('windkph_pressuremb_corr', None),
                    wind_cloud_corr=correlations.get('windkph_cloud_corr', None),
                    cloud_temp_corr=correlations.get('cloud_tempc_corr', None),
                    cloud_humidity_corr=correlations.get('cloud_humidity_corr', None),
                    cloud_pressure_corr=correlations.get('cloud_pressuremb_corr', None),
                    cloud_wind_corr=correlations.get('cloud_windkph_corr', None)
                )
                results.append(result)
                logger.info(f"Đã phân tích tương quan cho năm {year}")

            return results

        except Exception as e:
            logger.error(f"Lỗi khi phân tích tương quan: {str(e)}")
            raise
