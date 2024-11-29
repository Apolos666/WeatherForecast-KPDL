'use client';
import React, { useEffect, useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import { useRouter } from 'next/navigation';
import Select from 'react-select';
import useGetRawMonthlyData from '../../../../../hooks/useGetRawMonthlyData';
import Plot from 'react-plotly.js';
import { toast } from 'react-toastify';

interface WeatherData {
  date: string;
  averageTemperature: number;
  maxTemperature: number;
  minTemperature: number;
  averageHumidity: number;
  averageWindSpeed: number;
  maxWindSpeed: number;
  totalPrecipitation: number;
  averagePressure: number;
  mostCommonCondition: string;
  mostCommonWindDirection: string;
}

const RawMonthlyData = () => {
  const router = useRouter();
  const [monthRange, setMonthRange] = useState(1);
  const [data, setData] = useState<WeatherData[]>([]);

  const options = [
    { value: '1', label: 'Date' },
    { value: '2', label: 'Week' },
    { value: '3', label: 'Month' },
  ];

  const handleChange = (selectedOption: any) => {
    const value = selectedOption.value;
    if (value === '1') {
      router.push('/pattern1/date');
    } else if (value === '2') {
      router.push('/pattern1/week');
    } else if (value === '3') {
      router.push('/pattern1/month');
    }
  };

  const { getRawData, loading } = useGetRawMonthlyData(monthRange);

  const fetchData = async () => {
    try {
      const result = await getRawData();

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
    if (monthRange) {
      fetchData();
    }
  }, [monthRange]);

  const date = data.map((item) => item.date);
  const averageTemperature = data.map((item) => item.averageTemperature);
  const maxTemperature = data.map((item) => item.maxTemperature);
  const minTemperature = data.map((item) => item.minTemperature);
  const averageHumidity = data.map((item) => item.averageHumidity);
  const averagePressure = data.map((item) => item.averagePressure);
  const averageWindSpeed = data.map((item) => item.averageWindSpeed);
  const maxWindSpeed = data.map((item) => item.maxWindSpeed);

  return (
    <div className="p-8 bg-[url('/bg1.jpg')] bg-cover bg-center shadow-lg min-h-screen space-y-10">
      <div className="p-8 h-full w-full bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 space-y-10">
        <div className="flex justify-between items-center bg-gradient-to-r from-blue-500 to-indigo-500 text-white p-6 rounded-lg shadow-md">
          <div className="flex flex-col gap-2">
            <h1 className="text-3xl font-bold">Monthly Data Insights</h1>
            <p className="text-sm mt-1">
              Quickly analyze data by selecting your preferred month range.
            </p>
          </div>
          <Select
            options={options}
            onChange={handleChange}
            placeholder="Select period"
            className="w-[220px] text-black"
            classNamePrefix="custom-select"
            styles={{
              control: (base) => ({
                ...base,
                background: '#ffffff',
                borderColor: '#cbd5e1',
                borderRadius: '0.5rem',
                boxShadow: '0 2px 6px rgba(0, 0, 0, 0.1)',
                '&:hover': {
                  borderColor: '#94a3b8',
                },
              }),
              menu: (base) => ({
                ...base,
                boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
              }),
            }}
          />
        </div>

        <div className="flex flex-row justify-end items-center gap-8 mt-8">
          <div className="space-y-3">
            <label
              htmlFor="monthRange"
              className="block text-base font-semibold text-gray-800"
            >
              Month Range
              <input
                type="text"
                id="monthRange"
                name="monthRange"
                value={monthRange}
                onChange={(e) => setMonthRange(Number(e.target.value))}
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg shadow-md focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all duration-200"
              />
            </label>
          </div>
        </div>

        <div className="grid md:grid-cols-3">
          <div className="col-span-1 bg-white/90 backdrop-blur-sm shadow-xl p-8 rounded-tl-lg rounded-bl-lg">
            <h2 className="flex flex-row text-3xl font-semibold text-blue-800 mb-4">
              <span>Temperature Monthly Weather Overview</span>
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore monthly temperature data, including trends in average,
              maximum, and minimum temperatures. Use this information to make
              informed decisions and optimize your monthly planning. The chart
              on the right visualizes temperature patterns over time,
              highlighting key metrics to help you track weather changes more
              effectively.
            </p>
          </div>

          <div className="col-span-2 bg-white/80 backdrop-blur-sm">
            <div className="bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg p-8 hover:shadow-xl transition-shadow duration-300 rounded-tr-lg rounded-br-lg">
              <div className="bg-white rounded-lg p-2 shadow-md">
                <Plot
                  data={[
                    {
                      x: date,
                      y: averageTemperature,
                      fill: 'tozeroy',
                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Average Temperature',
                      line: { color: '#1E90FF' }, // Blue
                    },
                    {
                      x: date,
                      y: maxTemperature,
                      fill: 'tozeroy',
                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Max Temperature',
                      line: { color: '#FF4500' }, // Red
                    },
                    {
                      x: date,
                      y: minTemperature,
                      fill: 'tozeroy',
                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Min Temperature',
                      line: { color: '#32CD32' }, // Green
                    },
                  ]}
                  layout={{
                    title: {
                      text: 'Temperature',
                      font: { size: 18, color: '#333' },
                    },
                    xaxis: {
                      title: {
                        text: 'Date',
                        font: { size: 14, color: '#333' },
                      },
                      tickformat: '%Y-%m-%d',
                    },
                    yaxis: {
                      title: {
                        text: 'Temperature (°C)',
                        font: { size: 14, color: '#333' },
                      },
                    },
                    legend: {
                      orientation: 'h',
                      font: { size: 12, color: '#333' },
                    },
                    margin: { l: 50, r: 30, t: 50, b: 50 },
                  }}
                  style={{ width: '100%', height: '400px' }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3">
          <div className="col-span-2 bg-white/80 backdrop-blur-sm rounded-tl-lg rounded-bl-lg">
            <div className="bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg p-8 hover:shadow-xl transition-shadow duration-300 rounded-tl-lg rounded-bl-lg">
              <div className="bg-white rounded-lg p-6 shadow-md">
                <Plot
                  data={[
                    {
                      x: date,
                      y: averageHumidity,
                      type: 'bar',
                      mode: 'lines+markers',
                      name: 'Average Humidity',
                      line: { color: '#FFD700' }, // Gold
                    },
                  ]}
                  layout={{
                    title: {
                      text: 'Humidity',
                      font: { size: 18, color: '#333' },
                    },
                    xaxis: {
                      title: {
                        text: 'Date',
                        font: { size: 14, color: '#333' },
                      },
                      tickformat: '%Y-%m-%d',
                    },
                    yaxis: {
                      title: {
                        text: 'Humidity (%)',
                        font: { size: 14, color: '#333' },
                      },
                    },
                    legend: {
                      orientation: 'h',
                      font: { size: 12, color: '#333' },
                    },
                    margin: { l: 50, r: 30, t: 50, b: 50 },
                  }}
                  style={{ width: '100%', height: '400px' }}
                />
              </div>
            </div>
          </div>

          <div className="col-span-1 bg-white/90 backdrop-blur-sm shadow-xl p-8 rounded-tr-lg rounded-br-lg">
            <h2 className="text-3xl font-semibold text-blue-800 mb-4">
              Humidity Monthly Weather Overview
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore monthly humidity data, including trends in average
              humidity levels. Use this information to make informed decisions
              and optimize your monthly planning. The chart on the left
              visualizes humidity patterns over time, highlighting key metrics
              to help you track weather changes more effectively.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-3">
          <div className="col-span-1 bg-white/90 backdrop-blur-sm shadow-xl p-8 rounded-tl-lg rounded-bl-lg">
            <h2 className="text-3xl font-semibold text-blue-800 mb-4">
              Pressure Monthly Weather Overview
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore monthly pressure data, including trends in average
              pressure. Use this information to make informed decisions and
              optimize your monthly planning. The chart on the right visualizes
              pressure patterns over time, highlighting key metrics to help you
              track weather changes more effectively.
            </p>
          </div>

          <div className="col-span-2 bg-white/80 backdrop-blur-sm">
            <div className="bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg p-8 hover:shadow-xl transition-shadow duration-300 rounded-tr-lg rounded-br-lg">
              <div className="bg-white rounded-lg p-6 shadow-md">
                <Plot
                  data={[
                    {
                      x: date,
                      y: averagePressure,
                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Average Pressure',
                      line: { color: '#FF6347' }, // Tomato
                    },
                  ]}
                  layout={{
                    title: {
                      text: 'Pressure',
                      font: { size: 18, color: '#333' },
                    },
                    xaxis: {
                      title: {
                        text: 'Date',
                        font: { size: 14, color: '#333' },
                      },
                      tickformat: '%Y-%m-%d',
                    },
                    yaxis: {
                      title: {
                        text: 'Pressure (hPa)',
                        font: { size: 14, color: '#333' },
                      },
                    },
                    legend: {
                      orientation: 'h',
                      font: { size: 12, color: '#333' },
                    },
                    margin: { l: 50, r: 30, t: 50, b: 50 },
                  }}
                  style={{ width: '100%', height: '400px' }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3">
          <div className="col-span-2 bg-white/80 backdrop-blur-sm rounded-tl-lg rounded-bl-lg">
            <div className="bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg p-8 hover:shadow-xl transition-shadow duration-300 rounded-tl-lg rounded-bl-lg">
              <div className="bg-white rounded-lg p-6 shadow-md">
                <Plot
                  data={[
                    {
                      x: date,
                      y: averageWindSpeed,
                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Average Wind Speed',
                      line: { color: '#4682B4' }, // Steel Blue
                    },
                    {
                      x: date,
                      y: maxWindSpeed,
                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Max Wind Speed',
                      line: { color: '#FF8C00' }, // Dark Orange
                    },
                  ]}
                  layout={{
                    title: {
                      text: 'Wind Speed',
                      font: { size: 18, color: '#333' },
                    },
                    xaxis: {
                      title: {
                        text: 'Date',
                        font: { size: 14, color: '#333' },
                      },
                      tickformat: '%Y-%m-%d',
                    },
                    yaxis: {
                      title: {
                        text: 'Wind Speed (m/s)',
                        font: { size: 14, color: '#333' },
                      },
                    },
                    legend: {
                      orientation: 'h',
                      font: { size: 12, color: '#333' },
                    },
                    margin: { l: 50, r: 30, t: 50, b: 50 },
                  }}
                  style={{ width: '100%', height: '400px' }}
                />
              </div>
            </div>
          </div>

          <div className="col-span-1 bg-white/90 backdrop-blur-sm shadow-xl p-8 rounded-tr-lg rounded-br-lg">
            <h2 className="text-3xl font-semibold text-blue-800 mb-4">
              Wind Speed Monthly Weather Overview
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore monthly wind speed data, including trends in average and
              max wind speed. Use this information to make informed decisions
              and optimize your monthly planning. The chart on the left
              visualizes wind speed patterns over time, highlighting key metrics
              to help you track weather changes more effectively.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RawMonthlyData;
