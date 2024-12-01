'use client';
import React, { useEffect, useState } from 'react';
import DatePicker from 'react-datepicker';
import { format } from 'date-fns';
import 'react-datepicker/dist/react-datepicker.css';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Select from 'react-select';
import useGetRawDailyData from '../../../../../hooks/useGetRawDailyData';
import Image from 'next/image';
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

const RawDailyData = () => {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  const router = useRouter();
  const [startDate, setStartDate] = useState<Date | null>(yesterday);
  const [endDate, setEndDate] = useState<Date | null>(yesterday);
  const formattedStartDate = startDate ? format(startDate, 'yyyy-MM-dd') : '';
  const formattedEndDate = endDate ? format(endDate, 'yyyy-MM-dd') : '';
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

  const { getRawData, loading } = useGetRawDailyData(
    formattedStartDate,
    formattedEndDate
  );

  const fetchData = async () => {
    try {
      const result = await getRawData();

      if (result?.ok) {
        setData(result.data);
      } else {
        console.error('Failed to fetch data');
      }
    } catch (error) {
      console.error('Error in fetchData:', error);
    }
  };

  useEffect(() => {
    if (formattedStartDate && formattedEndDate) {
      fetchData();
      toast.success(
        `New data fetched from ${formattedStartDate} to ${formattedEndDate}`
      );
    }
  }, [getRawData, formattedStartDate, formattedEndDate]);

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
        {/* Header Section */}
        <div className="flex justify-between items-center bg-gradient-to-r from-blue-500 to-indigo-500 text-white p-6 rounded-lg shadow-md">
          <div className="flex flex-col gap-2">
            <h1 className="text-3xl font-bold">Daily Data Insights</h1>
            <p className="text-sm mt-1">
              Quickly analyze data by selecting your preferred date range.
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

        {/* Date Picker Section */}
        <div className="flex flex-row justify-end items-center gap-8 mt-8">
          {/* Start Date */}
          <div className="space-y-3">
            <label
              htmlFor="startDate"
              className="block text-base font-semibold text-gray-800"
            >
              Start Date
              <span className="text-gray-700 ml-1 font-medium">(From)</span>
            </label>
            <div className="flex flex-row gap-2">
              <DatePicker
                id="startDate"
                selected={startDate}
                onChange={(date: Date | null) => setStartDate(date)}
                placeholderText="Select start date"
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg shadow-md focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all duration-200"
                dateFormat="dd/MM/yyyy"
                showMonthDropdown
                showYearDropdown
                dropdownMode="select"
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="3rem"
                height="3rem"
                viewBox="0 0 28 28"
              >
                <g fill="none">
                  <path
                    fill="url(#fluentColorCalendar280)"
                    d="M25 21.75A3.25 3.25 0 0 1 21.75 25H6.25A3.25 3.25 0 0 1 3 21.75V9l11-1l11 1z"
                  />
                  <path
                    fill="url(#fluentColorCalendar281)"
                    d="M25 21.75A3.25 3.25 0 0 1 21.75 25H6.25A3.25 3.25 0 0 1 3 21.75V9l11-1l11 1z"
                  />
                  <g filter="url(#fluentColorCalendar284)">
                    <path
                      fill="url(#fluentColorCalendar282)"
                      d="M8.749 17.502a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m5.254 0a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m-5.254-5a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m5.254 0a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m5.255 0a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5"
                    />
                  </g>
                  <path
                    fill="url(#fluentColorCalendar283)"
                    d="M21.75 3A3.25 3.25 0 0 1 25 6.25V9H3V6.25A3.25 3.25 0 0 1 6.25 3z"
                  />
                  <defs>
                    <linearGradient
                      id="fluentColorCalendar280"
                      x1="17.972"
                      x2="11.828"
                      y1="27.088"
                      y2="8.803"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#b3e0ff" />
                      <stop offset="1" stop-color="#b3e0ff" />
                    </linearGradient>
                    <linearGradient
                      id="fluentColorCalendar281"
                      x1="16.357"
                      x2="19.402"
                      y1="14.954"
                      y2="28.885"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#dcf8ff" stop-opacity="0" />
                      <stop
                        offset="1"
                        stop-color="#3b3b3b"
                        stop-opacity="0.7"
                      />
                    </linearGradient>
                    <linearGradient
                      id="fluentColorCalendar282"
                      x1="12.821"
                      x2="15.099"
                      y1="11.636"
                      y2="26.649"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#0078d4" />
                      <stop offset="1" stop-color="#0067bf" />
                    </linearGradient>
                    <linearGradient
                      id="fluentColorCalendar283"
                      x1="3"
                      x2="21.722"
                      y1="3"
                      y2="-3.157"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#0094f0" />
                      <stop offset="1" stop-color="#2764e7" />
                    </linearGradient>
                    <filter
                      id="fluentColorCalendar284"
                      width="15.676"
                      height="10.167"
                      x="6.165"
                      y="11.835"
                      color-interpolation-filters="sRGB"
                      filterUnits="userSpaceOnUse"
                    >
                      <feFlood flood-opacity="0" result="BackgroundImageFix" />
                      <feColorMatrix
                        in="SourceAlpha"
                        result="hardAlpha"
                        values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                      />
                      <feOffset dy=".667" />
                      <feGaussianBlur stdDeviation=".667" />
                      <feColorMatrix values="0 0 0 0 0.1242 0 0 0 0 0.323337 0 0 0 0 0.7958 0 0 0 0.32 0" />
                      <feBlend
                        in2="BackgroundImageFix"
                        result="effect1_dropShadow_378174_9797"
                      />
                      <feBlend
                        in="SourceGraphic"
                        in2="effect1_dropShadow_378174_9797"
                        result="shape"
                      />
                    </filter>
                  </defs>
                </g>
              </svg>
            </div>
          </div>

          {/* End Date */}
          <div className="space-y-3">
            <label
              htmlFor="endDate"
              className="block text-base font-semibold text-gray-800 "
            >
              End Date
              <span className="text-gray-700 ml-1 font-medium">(To)</span>
            </label>
            <div className="flex flex-row gap-2">
              <DatePicker
                id="endDate"
                selected={endDate}
                onChange={(date: Date | null) => setEndDate(date)}
                placeholderText="Select end date"
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg shadow-md focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all duration-200"
                dateFormat="dd/MM/yyyy"
                showMonthDropdown
                showYearDropdown
                dropdownMode="select"
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="3rem"
                height="3rem"
                viewBox="0 0 28 28"
              >
                <g fill="none">
                  <path
                    fill="url(#fluentColorCalendar280)"
                    d="M25 21.75A3.25 3.25 0 0 1 21.75 25H6.25A3.25 3.25 0 0 1 3 21.75V9l11-1l11 1z"
                  />
                  <path
                    fill="url(#fluentColorCalendar281)"
                    d="M25 21.75A3.25 3.25 0 0 1 21.75 25H6.25A3.25 3.25 0 0 1 3 21.75V9l11-1l11 1z"
                  />
                  <g filter="url(#fluentColorCalendar284)">
                    <path
                      fill="url(#fluentColorCalendar282)"
                      d="M8.749 17.502a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m5.254 0a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m-5.254-5a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m5.254 0a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5m5.255 0a1.25 1.25 0 1 1 0 2.5a1.25 1.25 0 0 1 0-2.5"
                    />
                  </g>
                  <path
                    fill="url(#fluentColorCalendar283)"
                    d="M21.75 3A3.25 3.25 0 0 1 25 6.25V9H3V6.25A3.25 3.25 0 0 1 6.25 3z"
                  />
                  <defs>
                    <linearGradient
                      id="fluentColorCalendar280"
                      x1="17.972"
                      x2="11.828"
                      y1="27.088"
                      y2="8.803"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#b3e0ff" />
                      <stop offset="1" stop-color="#b3e0ff" />
                    </linearGradient>
                    <linearGradient
                      id="fluentColorCalendar281"
                      x1="16.357"
                      x2="19.402"
                      y1="14.954"
                      y2="28.885"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#dcf8ff" stop-opacity="0" />
                      <stop
                        offset="1"
                        stop-color="#3b3b3b"
                        stop-opacity="0.7"
                      />
                    </linearGradient>
                    <linearGradient
                      id="fluentColorCalendar282"
                      x1="12.821"
                      x2="15.099"
                      y1="11.636"
                      y2="26.649"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#0078d4" />
                      <stop offset="1" stop-color="#0067bf" />
                    </linearGradient>
                    <linearGradient
                      id="fluentColorCalendar283"
                      x1="3"
                      x2="21.722"
                      y1="3"
                      y2="-3.157"
                      gradientUnits="userSpaceOnUse"
                    >
                      <stop stop-color="#0094f0" />
                      <stop offset="1" stop-color="#2764e7" />
                    </linearGradient>
                    <filter
                      id="fluentColorCalendar284"
                      width="15.676"
                      height="10.167"
                      x="6.165"
                      y="11.835"
                      color-interpolation-filters="sRGB"
                      filterUnits="userSpaceOnUse"
                    >
                      <feFlood flood-opacity="0" result="BackgroundImageFix" />
                      <feColorMatrix
                        in="SourceAlpha"
                        result="hardAlpha"
                        values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                      />
                      <feOffset dy=".667" />
                      <feGaussianBlur stdDeviation=".667" />
                      <feColorMatrix values="0 0 0 0 0.1242 0 0 0 0 0.323337 0 0 0 0 0.7958 0 0 0 0.32 0" />
                      <feBlend
                        in2="BackgroundImageFix"
                        result="effect1_dropShadow_378174_9797"
                      />
                      <feBlend
                        in="SourceGraphic"
                        in2="effect1_dropShadow_378174_9797"
                        result="shape"
                      />
                    </filter>
                  </defs>
                </g>
              </svg>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3">
          <div className="col-span-1 bg-white/90 backdrop-blur-sm shadow-xl p-8 rounded-tl-lg rounded-bl-lg">
            <h2 className="flex flex-row text-3xl font-semibold text-blue-800 mb-4">
              <span>Temperature Daily Weather Overview</span>
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore daily temperature data, including trends in average,
              maximum, and minimum temperatures. Use this information to make
              informed decisions and optimize your daily planning. The chart on
              the right visualizes temperature patterns over time, highlighting
              key metrics to help you track weather changes more effectively.
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

                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Average Temperature',
                      line: { color: '#1E90FF' }, // Blue
                    },
                    {
                      x: date,
                      y: maxTemperature,

                      type: 'scatter',
                      mode: 'lines+markers',
                      name: 'Max Temperature',
                      line: { color: '#FF4500' }, // Red
                    },
                    {
                      x: date,
                      y: minTemperature,

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
                      type: 'scatter',
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
              Humidity Daily Weather Overview
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore daily humidity data, including trends in average humidity
              levels. Use this information to make informed decisions and
              optimize your daily planning. The chart on the left visualizes
              humidity patterns over time, highlighting key metrics to help you
              track weather changes more effectively.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-3">
          <div className="col-span-1 bg-white/90 backdrop-blur-sm shadow-xl p-8 rounded-tl-lg rounded-bl-lg">
            <h2 className="text-3xl font-semibold text-blue-800 mb-4">
              Pressure Daily Weather Overview
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore daily pressure data, including trends in average pressure.
              Use this information to make informed decisions and optimize your
              daily planning. The chart on the right visualizes pressure
              patterns over time, highlighting key metrics to help you track
              weather changes more effectively.
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
              Wind Speed Daily Weather Overview
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              Explore daily wind speed data, including trends in average and max
              wind speed. Use this information to make informed decisions and
              optimize your daily planning. The chart on the left visualizes
              wind speed patterns over time, highlighting key metrics to help
              you track weather changes more effectively.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RawDailyData;
