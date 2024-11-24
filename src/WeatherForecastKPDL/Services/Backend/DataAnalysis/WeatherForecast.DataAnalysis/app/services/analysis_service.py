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

            df['Time'] = pd.to_datetime(df['Time'])
            df['year_month'] = df['Time'].dt.strftime('%Y-%m')

            last_month = df['year_month'].max()
            month_data = df[df['year_month'] == last_month]

            if month_data.empty:
                raise ValueError("Không có dữ liệu để phân tích")

            result = SeasonalAnalysis(
                date=month_data['Time'].max().strftime('%Y-%m-%d'),
                year_month=last_month,
                avg_temp=month_data['TempC'].mean(),
                avg_humidity=month_data['Humidity'].mean(),
                total_precip=month_data['PrecipMm'].sum(),
                avg_wind=month_data['WindKph'].mean(),
                avg_pressure=month_data['PressureMb'].mean(),
                max_temp=month_data['TempC'].max(),
                min_temp=month_data['TempC'].min(),
                rainy_hours=month_data[month_data['PrecipMm'] > 0].shape[0]
            )

            logger.info(f"Kết quả phân tích: {result.model_dump()}")
            return result
        except Exception as e:
            logger.error(f"Lỗi khi phân tích dữ liệu theo mùa: {str(e)}")
            raise

    def analyze_correlation(self, hourly_data: List[HourlyWeatherData]) -> CorrelationAnalysis:
        logger.info(f"Bắt đầu phân tích tương quan với {len(hourly_data)} bản ghi")
        try:
            df = pd.DataFrame([vars(data) for data in hourly_data])
            
            if df.empty:
                raise ValueError("Không có dữ liệu để phân tích")
            
            # Chuyển đổi cột Time sang datetime để lấy ngày
            df['Time'] = pd.to_datetime(df['Time'])
            
            # Các biến quan trọng cần phân tích tương quan
            variables = {
                'TempC': ['Humidity', 'PressureMb', 'WindKph', 'FeelslikeC', 'WindchillC', 'HeatindexC'],
                'Humidity': ['PressureMb', 'WindKph', 'PrecipMm', 'Cloud'],
                'PressureMb': ['WindKph', 'Cloud'],
                'WindKph': ['Cloud', 'WindchillC'],
                'PrecipMm': ['Cloud', 'Humidity']
            }
            
            correlations = {}
            for var1, related_vars in variables.items():
                for var2 in related_vars:
                    corr_name = f"{var1.lower()}_{var2.lower()}_corr"
                    correlations[corr_name] = round(df[var1].corr(df[var2]), 3)
            
            result = CorrelationAnalysis(
                date=df['Time'].iloc[0].strftime('%Y-%m-%d'),
                temp_humidity_corr=correlations['tempc_humidity_corr'],
                temp_pressure_corr=correlations['tempc_pressuremb_corr'],
                temp_wind_corr=correlations['tempc_windkph_corr'],
                humidity_pressure_corr=correlations['humidity_pressuremb_corr'],
                humidity_wind_corr=correlations['humidity_windkph_corr'],
                pressure_wind_corr=correlations['pressuremb_windkph_corr'],
                rain_humidity_corr=correlations['precipmm_humidity_corr'],
                feels_temp_corr=correlations['tempc_feelslikec_corr'],
                windchill_temp_corr=correlations['tempc_windchillc_corr'],
                heatindex_temp_corr=correlations['tempc_heatindexc_corr'],
                cloud_humidity_corr=correlations['humidity_cloud_corr'],
                cloud_wind_corr=correlations['windkph_cloud_corr']
            )
            
            logger.info(f"Kết quả phân tích tương quan: {result.model_dump()}")
            return result
            
        except Exception as e:
            logger.error(f"Lỗi khi phân tích tương quan: {str(e)}")
            raise
