'use client';
import React, { useEffect, useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import useGetSeasonalData from '../../../../hooks/useGetSeasonalData';
import Plot from 'react-plotly.js';
import { toast } from 'react-toastify';

interface WeatherData {
  date: string;
  yearMonth: string;
  avgTemp: number;
  avgHumidity: number;
  totalPrecip: number;
  avgWind: number;
  avgPressure: number;
  maxTemp: number;
  minTemp: number;
  rainyHours: number;
}

const ThirdPattern = () => {
  const [data, setData] = useState<WeatherData[]>([]);

  const { getSeasonalData, loading } = useGetSeasonalData();

  const fetchData = async () => {
    try {
      const result = await getSeasonalData();

      if (result.ok) {
        setData(result.data);
      } else {
        toast.error('Error fetching data');
      }
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const yearMonth = data.map((item) => item.yearMonth);
  const avgTemp = data.map((item) => item.avgTemp);
  const avgHumidity = data.map((item) => item.avgHumidity);
  const avgPressure = data.map((item) => item.avgPressure);
  const avgWind = data.map((item) => item.avgWind);
  const rainyHours = data.map((item) => item.rainyHours);
  return (
    <div className="p-8 bg-[url('/bg3.jpg')] bg-cover bg-center shadow-lg min-h-screen space-y-10">
      <div className="p-8 h-full w-full bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 space-y-10">
        <header className="flex justify-between items-center bg-gradient-to-br from-blue-500 to-blue-700 text-white p-8 rounded-xl shadow-md">
          <div className="flex flex-col gap-4">
            <h1 className="text-4xl font-bold tracking-tight">Seasonal Data</h1>
            <p className="text-lg font-light">
              Explore aggregated seasonal data trends and uncover meaningful
              patterns.
            </p>
          </div>
        </header>

        <div className="grid lg:grid-cols-3 gap-2">
          <div className="bg-white p-2 rounded-xl shadow-md flex flex-col justify-between">
            <Plot
              data={[
                {
                  x: yearMonth,
                  y: avgHumidity,
                  fill: 'tozeroy',
                  type: 'scatter',
                  mode: 'lines',
                  marker: { color: 'green' },
                  name: 'Average Humidity',
                },
              ]}
              layout={{
                title: 'Average Humidity',
                xaxis: { title: 'Year-Month' },
                yaxis: { title: 'Humidity (%)' },
                legend: { orientation: 'h', y: -0.2 },
              }}
              style={{ width: '90%', height: '90%' }}
            />
          </div>
          <div className="bg-white p-2 rounded-xl shadow-md flex flex-col justify-between">
            <Plot
              data={[
                {
                  x: yearMonth,
                  y: avgPressure,
                  type: 'scatter',
                  mode: 'lines+markers',
                  marker: { color: 'purple' },
                  name: 'Average Pressure',
                },
              ]}
              layout={{
                title: 'Average Pressure',
                xaxis: { title: 'Year-Month' },
                yaxis: { title: 'Pressure (hPa)' },
                legend: { orientation: 'h', y: -0.2 },
              }}
              style={{ width: '90%', height: '90%' }}
            />
          </div>
          <div className="bg-white p-2 rounded-xl shadow-md flex flex-col justify-between">
            <Plot
              data={[
                {
                  x: yearMonth,
                  y: avgWind,
                  type: 'bar',
                  marker: { color: 'orange' },
                  name: 'Average Wind Speed',
                },
              ]}
              layout={{
                title: 'Average Wind Speed',
                xaxis: { title: 'Year-Month' },
                yaxis: { title: 'Wind Speed (m/s)' },
                legend: { orientation: 'h', y: -0.2 },
              }}
              style={{ width: '90%', height: '90%' }}
            />
          </div>
        </div>

        <div className="bg-white p-2 rounded-lg shadow-md flex flex-col justify-between">
          <Plot
            data={[
              {
                x: yearMonth,
                y: avgTemp,
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: 'red' },
                name: 'Average Temperature', // Nhãn hiển thị
                yaxis: 'y2', // Liên kết với trục y bên phải
              },
              {
                x: yearMonth,
                y: rainyHours,
                type: 'bar',
                marker: { color: 'blue' },
                name: 'Rainy Hours', // Nhãn hiển thị
              },
            ]}
            layout={{
              title: 'Average Temperature and Rainy Hours',
              xaxis: { title: 'Year-Month' },
              yaxis: {
                title: 'Rainy Hours',
                titlefont: { color: 'blue' },
                tickfont: { color: 'blue' },
              },
              yaxis2: {
                title: 'Temperature (°C)',
                titlefont: { color: 'red' },
                tickfont: { color: 'red' },
                overlaying: 'y',
                side: 'right', // Trục y2 hiển thị ở bên phải
              },
              legend: { orientation: 'h', y: -0.2 }, // Đặt chú thích ở dưới
              barmode: 'group', // Hiển thị cột gọn gàng
            }}
            style={{ width: '100%', height: '100%' }}
          />
        </div>
      </div>
    </div>
  );
};

export default ThirdPattern;
