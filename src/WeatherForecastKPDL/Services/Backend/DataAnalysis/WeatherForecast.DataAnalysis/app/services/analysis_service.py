import pandas as pd
from typing import List
from ..models.analysis import (
    HourlyWeatherData, 
    DailyAnalysis,
    SeasonalAnalysis,
    CorrelationAnalysis,
    MonthlyAnalysis
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

    def analyze_seasonal_data(self, data: List[HourlyWeatherData]) -> MonthlyAnalysis:
        logger.info(f"Bắt đầu phân tích dữ liệu theo tháng với {len(data)} bản ghi")
        try:
            df = pd.DataFrame([vars(d) for d in data])
            
            if df.empty:
                raise ValueError("Không có dữ liệu để phân tích")
            
            df['Time'] = pd.to_datetime(df['Time'])
            df['year_month'] = df['Time'].dt.strftime('%Y-%m')
            
            last_month = df['year_month'].max()
            month_data = df[df['year_month'] == last_month]
            
            if month_data.empty:
                raise ValueError(f"Không có dữ liệu cho tháng {last_month}")
            
            # Tính toán các giá trị trung bình
            result = MonthlyAnalysis(
                year_month=last_month,
                avg_temp=round(float(month_data['TempC'].mean()), 2),
                avg_humidity=round(float(month_data['Humidity'].mean()), 2),
                total_precip=round(float(month_data['PrecipMm'].sum()), 2),
                avg_wind=round(float(month_data['WindKph'].mean()), 2),
                avg_pressure=round(float(month_data['PressureMb'].mean()), 2),
                max_temp=round(float(month_data['TempC'].max()), 2),
                min_temp=round(float(month_data['TempC'].min()), 2),
                rainy_days=int((month_data['PrecipMm'] > 0).sum())
            )
            
            logger.info(f"Kết quả phân tích theo tháng: {result.model_dump()}")
            return result
        
        except Exception as e:
            logger.error(f"Lỗi khi phân tích dữ liệu theo tháng: {str(e)}")
            raise


    def analyze_correlation(self, data: List[HourlyWeatherData]) -> CorrelationAnalysis:
        # Sẽ implement sau
        pass
