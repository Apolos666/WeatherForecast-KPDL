'use client';
import React, { useEffect, useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import useGetSeasonalData from '../../../../hooks/useGetSeasonalData';
import useGetSpiderChartData from '../../../../hooks/useGetSpiderChartData';
import Plot from 'react-plotly.js';
import { toast } from 'react-toastify';
import { Data, Layout } from 'plotly.js';

interface WeatherData {
  date: string;
  year: number;
  quarter: number;
  avgTemp: number;
  avgHumidity: number;
  totalPrecip: number;
  avgWind: number;
  avgPressure: number;
  maxTemp: number;
  minTemp: number;
}

interface Divider {
  type: 'line';
  x0: string;
  x1: string;
  y0: number;
  y1: number;
  yref: 'paper' | 'y';
  line: {
    color: string;
    width: number;
    dash: 'solid' | 'dot' | 'dash' | 'longdash' | 'dashdot' | 'longdashdot';
    spape: 'linear' | 'spline';
  };
}

interface SpiderWeatherData {
  id: number;
  year: number;
  springQuantity: number;
  summerQuantity: number;
  autumnQuantity: number;
  winterQuantity: number;
}

const ThirdPattern = () => {
  const [data, setData] = useState<WeatherData[]>([]);
  const [year, setYear] = useState('');
  const [quarter, setQuarter] = useState('');

  const [spiderData, setSpiderData] = useState<SpiderWeatherData[]>([]);

  const { getSeasonalData } = useGetSeasonalData(year, quarter);

  const { getSpiderChartData } = useGetSpiderChartData();

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

  const fetchSpiderData = async () => {
    try {
      const result = await getSpiderChartData();

      if (result.ok) {
        setSpiderData(result.data);
      } else {
        toast.error('Error fetching data');
      }
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchData();
    fetchSpiderData();
  }, []);

  useEffect(() => {
    if (year && quarter) {
      fetchData();
    }
  }, [year, quarter]);

  const handleFilter = () => {
    if (year || quarter) {
      fetchData();
    } else if (!year && !quarter) {
      fetchData(); // Fetch lại tất cả dữ liệu
    } else {
      toast.warning('Please enter year or quarter');
    }
  };

  console.log(data);

  const date = data.map((item) => item.date);
  const Year = data.map((item) => item.year);
  const Quarter = data.map((item) => item.quarter);
  const avgTemp = data.map((item) => item.avgTemp);
  const avgHumidity = data.map((item) => item.avgHumidity);
  const totalPrecip = data.map((item) => item.totalPrecip);
  const avgWind = data.map((item) => item.avgWind);
  const avgPressure = data.map((item) => item.avgPressure);
  const maxTemp = data.map((item) => item.maxTemp);
  const minTemp = data.map((item) => item.minTemp);

  // Tạo các đường phân chia quý
  const createQuarterDividers = () => {
    if (!data.length) return [];

    const dividers: Divider[] = [];
    let currentQuarter: number | null = null;

    data.forEach((item, index) => {
      if (currentQuarter !== item.quarter) {
        currentQuarter = item.quarter;
        dividers.push({
          type: 'line',
          x0: item.date,
          x1: item.date,
          y0: 0,
          y1: 1,
          yref: 'paper',
          line: {
            color: 'rgba(156, 156, 156, 0.5)',
            width: 3,
            dash: 'dash',
            spape: 'spline',
          },
        });
      }
    });

    return dividers;
  };

  // Tổ chức dữ liệu theo quý cho độ ẩm
  const organizeHumidityByQuarter = (): Data[] => {
    const quarterData = data.reduce<Record<number, WeatherData[]>>(
      (acc, item) => {
        if (!acc[item.quarter]) {
          acc[item.quarter] = [];
        }
        acc[item.quarter].push(item);
        return acc;
      },
      {}
    );

    return Object.entries(quarterData).map(([quarter, items]) => ({
      x: items.map((item) => item.date),
      y: items.map((item) => item.avgHumidity),
      name: `Quý ${quarter}`,
      type: 'scatter' as const,
      mode: 'lines+markers',
      marker: {
        size: 8,
        symbol: ['circle', 'square', 'diamond', 'star'][Number(quarter) - 1],
        color: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'][
          Number(quarter) - 1
        ],
      },
      line: {
        shape: 'spline',
      },
      hovertemplate:
        'Ngày: %{x}<br>' +
        'Quý: ' +
        quarter +
        '<br>' +
        'Độ ẩm: %{y:.1f}%<br>' +
        '<extra></extra>',
    }));
  };

  // Tổ chức dữ liệu theo quý cho áp suất
  const organizePressureByQuarter = (): Data[] => {
    const quarterData = data.reduce<Record<number, WeatherData[]>>(
      (acc, item) => {
        if (!acc[item.quarter]) {
          acc[item.quarter] = [];
        }
        acc[item.quarter].push(item);
        return acc;
      },
      {}
    );

    return Object.entries(quarterData).map(([quarter, items]) => ({
      x: items.map((item) => item.date),
      y: items.map((item) => item.avgPressure),
      name: `Quý ${quarter}`,
      type: 'scatter' as const,
      mode: 'lines+markers',
      marker: {
        size: 8,
        symbol: ['circle', 'square', 'diamond', 'star'][Number(quarter) - 1],
        color: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'][
          Number(quarter) - 1
        ],
      },
      hovertemplate:
        'Ngày: %{x}<br>' +
        'Quý: ' +
        quarter +
        '<br>' +
        'Áp suất: %{y:.1f} hPa<br>' +
        '<extra></extra>',
    }));
  };

  // Tổ chức dữ liệu theo quý cho tốc độ gió
  const organizeWindByQuarter = (): Data[] => {
    const quarterData = data.reduce<Record<number, WeatherData[]>>(
      (acc, item) => {
        if (!acc[item.quarter]) {
          acc[item.quarter] = [];
        }
        acc[item.quarter].push(item);
        return acc;
      },
      {}
    );

    return Object.entries(quarterData).map(([quarter, items]) => ({
      x: items.map((item) => item.date),
      y: items.map((item) => item.avgWind),
      name: `Quý ${quarter}`,
      type: 'scatter' as const,
      mode: 'lines+markers',
      marker: {
        size: 8,
        symbol: ['circle', 'square', 'diamond', 'star'][Number(quarter) - 1],
        color: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'][
          Number(quarter) - 1
        ],
      },
      hovertemplate:
        'Ngày: %{x}<br>' +
        'Quý: ' +
        quarter +
        '<br>' +
        'Tốc độ gió: %{y:.1f} m/s<br>' +
        '<extra></extra>',
    }));
  };

  // Thêm hàm helper để xác định quý
  const getQuarter = (date: string) => {
    const month = new Date(date).getMonth() + 1;
    return Math.ceil(month / 3);
  };

  // Tổ chức dữ liệu theo quý cho nhiệt độ
  const organizeDataByQuarter = (): Data[] => {
    const quarterData = data.reduce<Record<number, WeatherData[]>>(
      (acc, item) => {
        if (!acc[item.quarter]) {
          acc[item.quarter] = [];
        }
        acc[item.quarter].push(item);
        return acc;
      },
      {}
    );

    return Object.entries(quarterData).map(([quarter, items]) => ({
      x: items.map((item) => item.date),
      y: items.map((item) => item.avgTemp),
      name: `Quý ${quarter}`,
      type: 'scatter' as const,
      mode: 'lines+markers',
      marker: {
        size: 8,
        symbol: ['circle', 'square', 'diamond', 'star'][Number(quarter) - 1],
        color: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'][
          Number(quarter) - 1
        ],
      },
      line: {
        shape: 'spline',
      },
      hovertemplate:
        'Ngày: %{x}<br>' +
        'Quý: ' +
        quarter +
        '<br>' +
        'Nhiệt độ: %{y:.1f}°C<br>' +
        '<extra></extra>',
    }));
  };

  const categories = ['Mùa Xuân', 'Mùa Hạ', 'Mùa Thu', 'Mùa Đông'];

  const values = spiderData.length > 0 ? [
    spiderData[0].springQuantity,
    spiderData[0].summerQuantity,
    spiderData[0].autumnQuantity,
    spiderData[0].winterQuantity
  ] : [0, 0, 0, 0];

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

        <div className="flex flex-row justify-end items-center gap-8 mt-8">
          <div className="space-y-3">
            <label className="text-lg font-semibold">Year:</label>
            <input
              type="number"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg shadow-md focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all duration-200"
              placeholder="Enter Year"
            />
          </div>
          <div className="space-y-3">
            <label className="text-lg font-semibold">Quarter:</label>
            <select
              value={quarter}
              onChange={(e) => setQuarter(e.target.value)}
              className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg shadow-md focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all duration-200"
            >
              <option value="">Pick Quarter</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
          </div>
          <button
            onClick={handleFilter}
            className="mt-auto px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Filter Data
          </button>
        </div>

        <div className="space-y-6">
          {/* Hàng đầu tiên: Chart độ ẩm và Spider chart */}
          <div className="grid grid-cols-5 gap-6">
            {/* Chart độ ẩm */}
            <div className="col-span-3 bg-white p-6 rounded-xl shadow-md">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <i className="fas fa-tint text-blue-500"></i>
                Biểu đồ độ ẩm theo quý
              </h2>
              <Plot
                data={organizeHumidityByQuarter()}
                layout={{
                  title: 'Độ ẩm trung bình',
                  xaxis: {
                    title: 'Thời gian',
                    tickangle: 45,
                    showgrid: true,
                    gridcolor: 'rgba(156, 156, 156, 0.1)',
                    zeroline: false,
                  },
                  yaxis: {
                    title: 'Độ ẩm (%)',
                    zeroline: false,
                  },
                  showlegend: true,
                  legend: {
                    orientation: 'h',
                    y: -0.2,
                    x: 0.5,
                    xanchor: 'center',
                  },
                  hovermode: 'closest',
                  plot_bgcolor: 'white',
                  margin: {
                    l: 50,
                    r: 50,
                    t: 50,
                    b: 100,
                  },
                  shapes: createQuarterDividers(),
                  annotations: [
                    {
                      x: 1.02,
                      y: 1.1,
                      xref: 'paper',
                      yref: 'paper',
                      text:
                        'Chú thích:<br>' +
                        '⭕ Quý 1 | ⬛ Quý 2 | ♦️ Quý 3 | ⭐ Quý 4',
                      showarrow: false,
                      font: { size: 12 },
                      align: 'right',
                    },
                  ],
                  height: 400,
                }}
                style={{ width: '100%', height: '100%' }}
                config={{
                  displayModeBar: true,
                  scrollZoom: true,
                }}
              />
            </div>

            {/* Spider chart */}
            <div className="col-span-2 bg-white p-6 rounded-xl shadow-md">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <i className="fas fa-chart-pie text-blue-500"></i>
                Phân bố số ngày theo mùa
              </h2>
              <Plot
                data={[
                  {
                    type: 'scatterpolar',
                    r: values,
                    theta: categories,
                    fill: 'toself',
                    name: 'Số ngày theo mùa',
                    marker: { color: '#3B82F6' },
                    fillcolor: 'rgba(59, 130, 246, 0.5)',
                    line: { color: '#1D4ED8', width: 2 },
                    hovertemplate:
                      'Mùa: %{theta}<br>' +
                      'Số ngày: %{r}<br>' +
                      '<extra></extra>',
                  },
                ]}
                layout={{
                  polar: {
                    radialaxis: {
                      visible: true,
                      title: {
                        text: 'Số ngày',
                        font: { size: 14, color: '#374151' },
                      },
                      tickfont: { size: 12, color: '#374151' },
                      gridcolor: 'rgba(156, 163, 175, 0.3)',
                      linecolor: 'rgba(156, 163, 175, 0.5)',
                    },
                    angularaxis: {
                      tickfont: { size: 14, color: '#374151' },
                      gridcolor: 'rgba(156, 163, 175, 0.3)',
                      linecolor: 'rgba(156, 163, 175, 0.5)',
                    },
                    bgcolor: 'white',
                  },
                  paper_bgcolor: 'white',
                  plot_bgcolor: 'white',
                  showlegend: false,
                  margin: { t: 50, b: 50, l: 50, r: 50 },
                  height: 400,
                }}
                style={{ width: '100%', height: '100%' }}
                config={{ responsive: true }}
              />
            </div>
          </div>

          {/* Hàng thứ hai: Chart nhiệt độ */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <i className="fas fa-temperature-high text-blue-500"></i>
              Biểu đồ nhiệt độ theo quý
            </h2>
            <Plot
              data={organizeDataByQuarter()}
              layout={{
                title: 'Nhiệt độ trung bình theo quý',
                xaxis: {
                  title: 'Thời gian',
                  tickangle: 45,
                  showgrid: true,
                  gridcolor: 'rgba(156, 156, 156, 0.1)',
                  zeroline: false,
                },
                yaxis: {
                  title: 'Nhiệt độ (°C)',
                  zeroline: false,
                },
                shapes: createQuarterDividers(),
                showlegend: true,
                legend: {
                  orientation: 'h',
                  y: -0.2,
                  x: 0.5,
                  xanchor: 'center',
                },
                hovermode: 'closest',
                plot_bgcolor: 'white',
                annotations: [
                  {
                    x: 1.02,
                    y: 1.1,
                    xref: 'paper',
                    yref: 'paper',
                    text:
                      'Chú thích:<br>' +
                      '⭕ Quý 1 | ⬛ Quý 2 | ♦️ Quý 3 | ⭐ Quý 4',
                    showarrow: false,
                    font: { size: 12 },
                    align: 'right',
                  },
                ],
                margin: {
                  l: 50,
                  r: 50,
                  t: 50,
                  b: 100,
                },
                height: 400,
              }}
              style={{ width: '100%', height: '100%' }}
              config={{
                displayModeBar: true,
                scrollZoom: true,
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThirdPattern;
