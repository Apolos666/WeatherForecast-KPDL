'use client';
import React, { useEffect, useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import useGetCorrelationData from '../../../../hooks/useGetCorrelationData';
import Plot from 'react-plotly.js';
import { toast } from 'react-toastify';

interface WeatherData {
  tempCHumidityCorrelation: number;
  tempCPressureMbCorrelation: number;
  tempCWindKphCorrelation: number;
  tempCCloudCorrelation: number;
  humidityTempCCorrelation: number;
  humidityPressureMbCorrelation: number;
  humidityWindKphCorrelation: number;
  humidityCloudCorrelation: number;
  pressureMbTempCCorrelation: number;
  pressureMbHumidityCorrelation: number;
  pressureMbWindKphCorrelation: number;
  pressureMbCloudCorrelation: number;
  windKphTempCCorrelation: number;
  windKphHumidityCorrelation: number;
  windKphPressureMbCorrelation: number;
  windKphCloudCorrelation: number;
  cloudTempCCorrelation: number;
  cloudHumidityCorrelation: number;
  cloudPressureMbCorrelation: number;
  cloudWindKphCorrelation: number;
}

const FourthPattern = () => {
  const [data, setData] = useState<WeatherData[]>([]);
  const [selectedScale, setSelectedScale] = useState('RdBu');
  const { getCorrelationData, loading } = useGetCorrelationData();

  const fetchData = async () => {
    try {
      const result = await getCorrelationData();

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

  if (data.length === 0) return null;

  const variables = ['Nhiệt độ', 'Độ ẩm', 'Áp suất', 'Tốc độ gió', 'Mây'];
  const correlationValues = [
    [
      1,
      data[0].tempCHumidityCorrelation,
      data[0].tempCPressureMbCorrelation,
      data[0].tempCWindKphCorrelation,
      data[0].tempCCloudCorrelation,
    ],
    [
      data[0].humidityTempCCorrelation,
      1,
      data[0].humidityPressureMbCorrelation,
      data[0].humidityWindKphCorrelation,
      data[0].humidityCloudCorrelation,
    ],
    [
      data[0].pressureMbTempCCorrelation,
      data[0].pressureMbHumidityCorrelation,
      1,
      data[0].pressureMbWindKphCorrelation,
      data[0].pressureMbCloudCorrelation,
    ],
    [
      data[0].windKphTempCCorrelation,
      data[0].windKphHumidityCorrelation,
      data[0].windKphPressureMbCorrelation,
      1,
      data[0].windKphCloudCorrelation,
    ],
    [
      data[0].cloudTempCCorrelation,
      data[0].cloudHumidityCorrelation,
      data[0].cloudPressureMbCorrelation,
      data[0].cloudWindKphCorrelation,
      1,
    ],
  ];

  const handleScaleChange = (e: any) => setSelectedScale(e.target.value);

  const flatValues = correlationValues.flat();
  const maxValue = Math.max(...flatValues).toFixed(3);
  const minValue = Math.min(...flatValues).toFixed(3);

  return (
    <div className="p-8 bg-[url('/bg4.jpg')] bg-cover bg-center shadow-lg min-h-screen space-y-10">
      <div className="p-8 h-full w-full bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 space-y-10">
        {/* Navbar */}
        <header className="bg-blue-600 text-white p-4 shadow-md">
          <h1 className="text-lg font-bold">Weather Correlation Dashboard</h1>
        </header>

        {/* Main content */}
        <main className="flex flex-col items-center justify-center p-6 flex-grow">
          {/* Tiêu đề và mô tả */}
          <div className="text-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-800">
              Ma trận tương quan giữa các biến thời tiết
            </h2>
            <p className="text-gray-600 mt-2">
              Heatmap thể hiện mối quan hệ giữa các biến thời tiết, từ tương
              quan âm (-1) đến tương quan dương (1).
            </p>
          </div>

          {/* Bộ chọn thang đo màu */}
          <div className="mb-4 flex items-center gap-4">
            <label className="text-gray-700 font-medium">
              Chọn thang màu:
              <select
                className="ml-2 border border-gray-300 rounded px-2 py-1"
                value={selectedScale}
                onChange={handleScaleChange}
              >
                <option value="RdBu">RdBu</option>
                <option value="Viridis">Viridis</option>
                <option value="Cividis">Cividis</option>
                <option value="Portland">Portland</option>
              </select>
            </label>
          </div>

          {/* Heatmap */}
          <div className="bg-white shadow-md rounded-lg p-4">
            <Plot
              data={[
                {
                  type: 'heatmap',
                  z: correlationValues,
                  x: variables,
                  y: variables,
                  colorscale: selectedScale,
                  zmin: -1,
                  zmax: 1,
                  text: correlationValues
                    .map((row) => row.map((value) => value.toFixed(3)))
                    .flat(),
                  showscale: true,
                },
              ]}
              layout={{
                width: 800,
                height: 800,
                xaxis: { side: 'bottom' },
                yaxis: { autorange: 'reversed' },
                annotations: correlationValues
                  .map((row, i) =>
                    row.map((value, j) => ({
                      x: variables[j],
                      y: variables[i],
                      text: value.toFixed(3),
                      showarrow: false,
                      font: { color: 'white' },
                    }))
                  )
                  .flat(),
              }}
              config={{ responsive: true }}
            />
          </div>

          {/* Insights */}
          <div className="mt-6 bg-gray-100 p-4 rounded shadow-md w-full max-w-lg">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Thông tin chi tiết
            </h3>
            <p className="text-gray-700">
              <strong>Giá trị tương quan cao nhất:</strong> {maxValue}
            </p>
            <p className="text-gray-700">
              <strong>Giá trị tương quan thấp nhất:</strong> {minValue}
            </p>
          </div>
        </main>
      </div>
    </div>
  );
};

export default FourthPattern;
