'use client';
import React, { useEffect, useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import useGetSpiderChartData from '../../../../hooks/useGetSpiderChartData';
import Plot from 'react-plotly.js';
import { toast } from 'react-toastify';

interface WeatherData {
  season: string;
  halfYear: string;
  numberOfDays: number;
}
const FifthPattern = () => {
  const [data, setData] = useState<WeatherData[]>([]);

  const { getSpiderChartData, loading } = useGetSpiderChartData();

  const fetchData = async () => {
    try {
      const result = await getSpiderChartData();

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

  const season = data.map((item) => item.season);
  const halfYear = data.map((item) => item.halfYear);
  const numberOfDays = data.map((item) => item.numberOfDays);

  const categories = [
    'Mùa Xuân - Nửa đầu năm',
    'Mùa Xuân - Nửa sau năm',
    'Mùa Hạ - Nửa đầu năm',
    'Mùa Hạ - Nửa sau năm',
    'Mùa Thu - Nửa đầu năm',
    'Mùa Thu - Nửa sau năm',
    'Mùa Đông - Nửa đầu năm',
    'Mùa Đông - Nửa sau năm',
  ];

  const values = categories.map((category) => {
    const [season, halfYear] = category.split(' - ');
    const match = data.find(
      (item) => item.season === season && item.halfYear === halfYear
    );
    return match ? match.numberOfDays : 0; // Mặc định 0 nếu không có dữ liệu
  });

  return (
    <div className="p-8 bg-[url('/bg2.jpg')] bg-cover bg-center shadow-lg min-h-screen">
      <div className="p-8 h-full w-full bg-gray-400 backdrop-blur-sm bg-opacity-10 rounded-lg space-y-12">
        {/* Tiêu đề */}
        <header className="text-center text-white space-y-6">
          <h1 className="text-5xl font-extrabold tracking-tight">
            Seasonal Data Analysis
          </h1>
          <p className="text-xl font-light max-w-3xl mx-auto">
            Uncover trends and seasonal patterns through the visualization of
            the number of days in each season. Discover insights to plan better.
          </p>
        </header>

        {/* Nội dung chính */}

        {/* Biểu đồ Spider Chart */}
        <div className="col-span-2 bg-gradient-to-br from-blue-500 to-blue-700 shadow-xl p-8 rounded-2xl relative overflow-hidden hover:scale-105 transition-all duration-300 ease-in-out">
          {/* Gradient Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-blue-500 opacity-20 rounded-2xl"></div>
          <div className="relative z-10">
            <h2 className="text-3xl font-semibold text-white mb-4">
              Number of Days in Each Season
            </h2>
            <p className="text-white text-base mb-6 leading-relaxed">
              Below is a spider chart visualizing the number of days across
              different seasons and half-years.
            </p>
            <Plot
              data={[
                {
                  type: 'scatterpolar',
                  r: values, // Giá trị cho mỗi danh mục
                  theta: categories, // Danh mục trục
                  fill: 'toself',
                  name: 'Số ngày theo mùa và nửa năm',
                  marker: { color: 'rgba(100, 150, 255, 0.7)' },
                },
              ]}
              layout={{
                polar: {
                  radialaxis: {
                    visible: true,
                    title: 'Number of Days',
                    tickfont: { size: 14, color: '#4A5568' },
                  },
                },
                title: { text: '', font: { size: 16, color: '#2D3748' } },
                showlegend: true,
                legend: {
                  font: { size: 12, color: '#2D3748' },
                  x: 1,
                  y: 1,
                },
              }}
              style={{ width: '100%', height: '500px' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FifthPattern;
