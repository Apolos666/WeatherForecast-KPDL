import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import logging
from sklearn.impute import SimpleImputer  # Thêm import SimpleImputer

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_data(data):
    logging.info("Bắt đầu xử lý dữ liệu")
    df = pd.DataFrame(data)
    logging.info(f"Dữ liệu ban đầu:\n{df.head()}")

    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)
    logging.info(f"Dữ liệu sau khi thiết lập chỉ số là 'Time':\n{df.head()}")

    # Xóa các cột không cần thiết
    columns_to_drop = [
        'Id', 'WeatherForecastId', 'TimeEpoch', 'ConditionText', 'ConditionIcon', 'ConditionCode',
        'WindDir', 'WillItRain', 'ChanceOfRain', 'WillItSnow', 'ChanceOfSnow',
        'VisKm', 'VisMiles', 'Uv', 'IsDay', 'PrecipMm', 'PrecipIn', 'SnowCm', 'Cloud'
    ]
    df = df.drop(columns=columns_to_drop, errors='ignore')
    logging.info(f"Dữ liệu sau khi xóa các cột không cần thiết:\n{df.head()}")

    # Sử dụng SimpleImputer để thay thế NaN bằng giá trị trung bình của các cột
    imputer = SimpleImputer(strategy='mean')
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)  # Đảm bảo chỉ số được giữ nguyên
    logging.info(f"Dữ liệu sau khi thay thế NaN bằng giá trị trung bình:\n{df_imputed.head()}")

    # Resample dữ liệu theo ngày tính median
    daily_data = df_imputed.resample('D').median().reset_index()
    logging.info(f"Dữ liệu sau khi resample theo ngày tính median:\n{daily_data.head()}")

    # Chuẩn hóa dữ liệu
    X = daily_data.drop(columns=['Time']).values
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    logging.info(f"Dữ liệu sau khi chuẩn hóa:\n{X[:5]}")

    # Sử dụng KMeans để phân cụm dữ liệu
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    daily_data['Cluster'] = kmeans.labels_
    logging.info(f"Dữ liệu sau khi phân cụm:\n{daily_data.head()}")

    # Tính toán số ngày trong từng mùa và nửa năm
    daily_data['Month'] = daily_data['Time'].dt.month
    daily_data['Season'] = pd.cut(daily_data['Month'], bins=[0, 3, 6, 9, 12], labels=['Mùa Đông', 'Mùa Xuân', 'Mùa Hạ', 'Mùa Thu'])
    daily_data['HalfYear'] = pd.cut(daily_data['Month'], bins=[0, 6, 12], labels=['Nửa đầu năm', 'Nửa sau năm'])
    logging.info(f"Dữ liệu sau khi tính toán số ngày trong từng mùa và nửa năm:\n{daily_data.head()}")

    seasonal_data = daily_data.groupby(['Season', 'HalfYear']).size().reset_index(name='NumberOfDays')
    logging.info(f"Dữ liệu seasonal_data:\n{seasonal_data}")

    year = daily_data['Time'].dt.year.unique()[0]
    logging.info(f"Kết thúc xử lý dữ liệu, năm: {year}")
    return year, seasonal_data