'use client';
import React, { useEffect } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import useGetDailyData from '../../../../hooks/useGetDailyData';
import Plot from 'react-plotly.js';
import { toast } from 'react-toastify';

const SecondPattern = () => {
  const { getDailyData, loading, data } = useGetDailyData();

  console.log(data)

  const fetchData = async () => {
    try {
      const result = await getDailyData();
      if (!result.ok) {
        toast.error('Error fetching data');
      }
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const date = data.map((item) => item.date);
  const averageTemperature = data.map((item) => item.averageTemperature);
  const averageHumidity = data.map((item) => item.averageHumidity);
  const averagePressure = data.map((item) => item.averagePressure);
  const averageWindSpeed = data.map((item) => item.averageWindSpeed);

  return (
    <div className="p-8 bg-[url('/bg2.jpg')] bg-cover bg-center shadow-lg min-h-screen space-y-10">
      <div className="p-8 h-full w-full bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 space-y-10">
        <header className="flex justify-between items-center bg-gradient-to-br from-blue-500 to-blue-700 text-white p-8 rounded-xl shadow-md">
          <div className="flex flex-col gap-4">
            <h1 className="text-4xl font-bold tracking-tight">
              Daily Trendy Data Insights
            </h1>
            <p className="text-lg font-light">
              Explore aggregated data trends and uncover meaningful patterns.
            </p>
          </div>
        </header>

        <div className="grid lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-md p-8 flex flex-col justify-between">
            <h2 className="text-2xl font-semibold text-blue-800-700 mb-4">
              Temperature Overview
            </h2>
            <p className="text-gray-600 text-base mb-6 leading-relaxed">
              Discover daily temperature trends, resampled to highlight average
              temperature fluctuations. Gain insights for planning better and
              understanding weather patterns with clarity.
            </p>
            <Plot
              data={[
                {
                  x: date,
                  y: averageTemperature,
                  type: 'scatter',
                  fill: 'tozeroy',
                  fillcolor: 'rgba(30, 144, 255, 0.3)',
                  line: { color: '#1E90FF', shape: 'spline', width: 3 },
                  mode: 'lines+markers',
                  marker: {
                    size: 4,
                    color: '#1E90FF',
                    opacity: 0.7,
                  },
                },
              ]}
              layout={{
                title: { text: 'Average Temperature', font: { size: 16 } },
                xaxis: { title: { text: 'Date', font: { size: 14 } } },
                yaxis: {
                  title: { text: 'Temperature (°C)', font: { size: 14 } },
                },
                margin: { l: 40, r: 20, t: 40, b: 50 },
                transition: {
                  duration: 1000,
                  easing: 'cubic-in-out',
                },
              }}
              style={{ width: '100%', height: '300px' }}
            />
          </div>

          <div className="bg-white rounded-xl shadow-md p-8 flex flex-col justify-between">
            <h2 className="text-2xl font-semibold text-blue-800 mb-4">
              Humidity Overview
            </h2>
            <p className="text-gray-600 text-base mb-6 leading-relaxed">
              Analyze resampled humidity data to understand trends in average
              humidity and prepare for changing weather conditions.
            </p>
            <Plot
              data={[
                {
                  x: date,
                  y: averageHumidity,
                  type: 'scatter',
                  fill: 'tozeroy',
                  fillcolor: 'rgba(255, 215, 0, 0.3)',
                  line: { color: '#FFD700', shape: 'spline', width: 3 },
                  mode: 'lines+markers',
                },
              ]}
              layout={{
                title: { text: 'Average Humidity', font: { size: 16 } },
                xaxis: { title: { text: 'Date', font: { size: 14 } } },
                yaxis: { title: { text: 'Humidity (%)', font: { size: 14 } } },
                margin: { l: 40, r: 20, t: 40, b: 50 },
                transition: {
                  duration: 1000,
                  easing: 'cubic-in-out',
                },
              }}
              style={{ width: '100%', height: '300px' }}
            />
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-md p-8 flex flex-col justify-between">
            <h2 className="text-2xl font-semibold text-blue-800 mb-4">
              Pressure Overview
            </h2>
            <p className="text-gray-600 text-base mb-6 leading-relaxed">
              Discover daily Pressure trends, resampled to highlight average
              Pressure fluctuations. Gain insights for planning better and
              understanding weather patterns with clarity.
            </p>
            <Plot
              data={[
                {
                  x: date,
                  y: averagePressure,
                  type: 'scatter',
                  fill: 'tozeroy',
                  fillcolor: 'rgba(255, 99, 71, 0.3)',
                  line: { color: '#FF6347', shape: 'spline', width: 3 },
                  mode: 'lines+markers',
                },
              ]}
              layout={{
                title: { text: 'Average Pressure', font: { size: 16 } },
                xaxis: { title: { text: 'Date', font: { size: 14 } } },
                yaxis: {
                  title: { text: 'Pressure (hPa)', font: { size: 14 } },
                },
                margin: { l: 40, r: 20, t: 40, b: 50 },
                transition: {
                  duration: 1000,
                  easing: 'cubic-in-out',
                },
              }}
              style={{ width: '100%', height: '300px' }}
            />
          </div>

          <div className="bg-white rounded-xl shadow-md p-8 flex flex-col justify-between">
            <h2 className="text-2xl font-semibold text-blue-800 mb-4">
              Wind Speed Overview
            </h2>
            <p className="text-gray-600 text-base mb-6 leading-relaxed">
              Analyze resampled Wind Speed data to understand trends in average
              Wind Speed and prepare for changing weather conditions.
            </p>
            <Plot
              data={[
                {
                  x: date,
                  y: averageWindSpeed,
                  type: 'scatter',
                  fill: 'tozeroy',
                  fillcolor: 'rgba(50, 205, 50, 0.3)',
                  line: { color: '#32CD32', shape: 'spline', width: 3 },
                  mode: 'lines+markers',
                },
              ]}
              layout={{
                title: { text: 'Average Wind Speed', font: { size: 16 } },
                xaxis: { title: { text: 'Date', font: { size: 14 } } },
                yaxis: {
                  title: { text: 'Wind Speed (km/h)', font: { size: 14 } },
                },
                margin: { l: 40, r: 20, t: 40, b: 50 },
                transition: {
                  duration: 1000,
                  easing: 'cubic-in-out',
                },
              }}
              style={{ width: '100%', height: '300px' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SecondPattern;
