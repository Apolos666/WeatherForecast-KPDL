'use client';
import React, { useEffect, useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import useGetPredictionData from '../../../../hooks/useGetPredictionData';
import { toast } from 'react-toastify';

interface WeatherData {
  predicted_temperature: number;
  predicted_humidity: number;
  predicted_pressure: number;
  predicted_wind: number;
  predicted_cloud: number;
}
const FifthPattern = () => {
  const [data, setData] = useState<WeatherData>();
  const [season, setSeason] = useState<string>('spring');
  const { getPredictionData, loading } = useGetPredictionData();

  useEffect(() => {
    const fetchData = async () => {
      const { ok, data } = await getPredictionData();
      if (!ok) {
        toast.error('Failed to fetch data');
        return;
      }
      setData(data);
    };
    fetchData();
  }, [getPredictionData]);

  console.log(data);

  return (
    <div
      className={`p-8 bg-cover bg-center shadow-lg min-h-screen space-y-10 
      ${season === 'spring' && "bg-[url('/spring.jpg')]"}
      ${season === 'summer' && "bg-[url('/summer.jpg')]"}
      ${season === 'autumn' && "bg-[url('/fall.jpg')]"}
      ${season === 'winter' && "bg-[url('/winter.jpg')]"}
      `}
    >
      <div className="p-8 h-auto w-full space-y-10">
        <h1 className="text-7xl font-bold text-center text-white">
          Weather Prediction
        </h1>
        {data && (
          <div className="space-y-6">
            <div className="grid grid-cols-6 gap-6">
              <div className="col-span-2 flex flex-col justify-start items-start gap-8 p-6 h-[470px] 2xl:h-[700px] shadow-md bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-20 border border-gray-100">
                <div className="flex flex-row gap-2 justify-center items-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="3rem"
                    height="3rem"
                    viewBox="0 0 24 24"
                  >
                    <path
                      fill="#fff"
                      d="M13.002 8.007c3.169 0 4.966 2.097 5.227 4.63h.08a3.687 3.687 0 0 1 3.692 3.683a3.687 3.687 0 0 1-3.692 3.682H7.695a3.687 3.687 0 0 1-3.692-3.682a3.687 3.687 0 0 1 3.692-3.683h.08c.263-2.55 2.059-4.63 5.227-4.63m-8.634 4.155a.75.75 0 0 1-.315.935l-.091.045l-.927.384a.75.75 0 0 1-.665-1.34l.091-.046l.927-.383a.75.75 0 0 1 .98.405m6.487-4.833l-.172.058c-1.784.63-3.062 2.005-3.615 3.823l-.07.25l-.058.238l-.206.039a4.6 4.6 0 0 0-1.67.714a3.942 3.942 0 0 1 5.791-5.122M2.94 7.36l.105.035l.927.384a.75.75 0 0 1-.469 1.42L3.4 9.166l-.927-.384a.75.75 0 0 1 .469-1.42m3.815-2.986l.045.091l.384.927a.75.75 0 0 1-1.34.665L5.8 5.968l-.383-.927a.75.75 0 0 1 1.34-.665m4.354-.319a.75.75 0 0 1 .44.875l-.035.105l-.383.927a.75.75 0 0 1-1.421-.469l.035-.106l.384-.926a.75.75 0 0 1 .98-.406"
                    />
                  </svg>
                  <h1 className="text-2xl 2xl:text-3xl font-bold text-center text-white">
                    Temperature
                  </h1>
                </div>

                <p className="text-6xl font-bold text-center text-white flex justify-center items-center w-full h-full 2xl:text-8xl">
                  {data ? `${data.predicted_temperature.toFixed(1)}°C` : ''}
                </p>
              </div>
              <div className="col-span-4 h-[450px] lg:h-[470px]">
                <div className="grid grid-cols-2 gap-6">
                  <div className="flex flex-col justify-start items-start gap-8  p-6  shadow-md h-[220px] 2xl:h-[335px] bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-20 border border-gray-100">
                    <div className="flex flex-row gap-2 justify-center items-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="2rem"
                        height="2rem"
                        viewBox="0 0 24 24"
                      >
                        <g
                          fill="none"
                          stroke="#fff"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="1.5"
                          color="#fff"
                        >
                          <path d="M3.5 13.678c0-4.184 3.58-8.319 6.094-10.706a3.463 3.463 0 0 1 4.812 0C16.919 5.36 20.5 9.494 20.5 13.678C20.5 17.78 17.281 22 12 22s-8.5-4.22-8.5-8.322" />
                          <path d="M4 12.284c1.465-.454 4.392-.6 7.984 1.418c3.586 2.014 6.532 1.296 8.016.433" />
                        </g>
                      </svg>
                      <h1 className="text-2xl 2xl:text-3xl font-bold text-center text-white">
                        Humidity
                      </h1>
                    </div>
                    <p className="text-5xl font-bold text-center text-white flex justify-center items-center w-full h-full 2xl:text-7xl">
                      {`${data.predicted_humidity.toFixed(1)}%`}
                    </p>
                  </div>
                  <div className="flex flex-col justify-start items-start gap-8  p-6  shadow-md h-[220px] 2xl:h-[335px] bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-20 border border-gray-100">
                    <div className="flex flex-row gap-2 justify-center items-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="2rem"
                        height="2rem"
                        viewBox="0 0 24 24"
                      >
                        <g fill="none" stroke="#fff" stroke-width="2">
                          <path
                            stroke-linecap="round"
                            d="M20.693 17.33a9 9 0 1 0-17.386 0"
                          />
                          <path d="M12.766 15.582c.487.71.144 1.792-.766 2.417c-.91.626-2.043.558-2.53-.151c-.52-.756-2.314-5.007-3.403-7.637c-.205-.495.4-.911.79-.542c2.064 1.96 5.39 5.157 5.909 5.913Z" />
                          <path
                            stroke-linecap="round"
                            d="M12 6v2m-6.364.636L7.05 10.05m11.314-1.414L16.95 10.05m3.743 7.28l-1.931-.518m-15.455.518l1.931-.518"
                          />
                        </g>
                      </svg>
                      <h1 className="text-2xl 2xl:text-3xl font-bold text-center text-white">
                        Pressure
                      </h1>
                    </div>
                    <p className="text-5xl font-bold text-center text-white flex justify-center items-center w-full h-full 2xl:text-7xl">
                      {`${data.predicted_pressure.toFixed(1)} hPa`}
                    </p>
                  </div>
                  <div className="flex flex-col justify-start items-start gap-8  p-6  shadow-md h-[220px] 2xl:h-[335px] bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-20 border border-gray-100">
                    <div className="flex flex-row gap-2 justify-center items-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="2rem"
                        height="2rem"
                        viewBox="0 0 24 24"
                      >
                        <path
                          fill="#fff"
                          d="m6 6l.69.06A5.5 5.5 0 0 1 12 2a5.5 5.5 0 0 1 5.5 5.5l-.08.95c.46-.29 1-.45 1.58-.45a3 3 0 0 1 3 3a3 3 0 0 1-3 3H6a4 4 0 0 1-4-4a4 4 0 0 1 4-4m0 2a2 2 0 0 0-2 2a2 2 0 0 0 2 2h13a1 1 0 0 0 1-1a1 1 0 0 0-1-1h-3.5V7.5A3.5 3.5 0 0 0 12 4a3.5 3.5 0 0 0-3.5 3.5V8zm12 10H4a1 1 0 0 1-1-1a1 1 0 0 1 1-1h14a3 3 0 0 1 3 3a3 3 0 0 1-3 3c-.83 0-1.58-.34-2.12-.88c-.38-.39-.38-1.02 0-1.41a.996.996 0 0 1 1.41 0c.18.18.43.29.71.29a1 1 0 0 0 1-1a1 1 0 0 0-1-1"
                        />
                      </svg>
                      <h1 className="text-2xl 2xl:text-3xl font-bold text-center text-white">
                        Wind
                      </h1>
                    </div>
                    <p className="text-5xl font-bold text-center text-white flex justify-center items-center w-full h-full 2xl:text-7xl">
                      {`${data.predicted_wind.toFixed(1)} km/h`}
                    </p>
                  </div>
                  <div className="flex flex-col justify-start items-start gap-8  p-6  shadow-md h-[220px] 2xl:h-[335px] bg-gray-200 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-20 border border-gray-100">
                    <div className="flex flex-row gap-2 justify-center items-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="2.4rem"
                        height="2.4rem"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fill="#fff"
                          d="M11 7c2.465 0 3.863 1.574 4.066 3.474h.062c1.586 0 2.872 1.237 2.872 2.763S16.714 16 15.128 16H6.872C5.286 16 4 14.763 4 13.237s1.286-2.763 2.872-2.763h.062C7.139 8.561 8.535 7 11 7m0 1c-1.65 0-3.087 1.27-3.087 3.025c0 .278-.254.496-.545.496h-.55C5.814 11.521 5 12.3 5 13.261C5 14.22 5.814 15 6.818 15h8.364C16.186 15 17 14.221 17 13.26c0-.96-.814-1.739-1.818-1.739h-.55c-.29 0-.545-.218-.545-.496C14.087 9.248 12.65 8 11 8M8.392 4c1.456 0 2.726.828 3.353 2.045a6 6 0 0 0-1.284-.022A2.65 2.65 0 0 0 8.375 5a2.67 2.67 0 0 0-2.62 2.225l-.037.21a1 1 0 0 1-.986.83h-.258C3.66 8.265 3 8.933 3 9.757c0 .57.315 1.065.778 1.316c-.214.272-.39.576-.52.902a2.622 2.622 0 0 1 1.2-4.856l.221-.005A3.77 3.77 0 0 1 8.392 4"
                        />
                      </svg>
                      <h1 className="text-2xl 2xl:text-3xl font-bold text-center text-white">
                        Cloud
                      </h1>
                    </div>
                    <p className="text-5xl font-bold text-center text-white flex justify-center items-center w-full h-full 2xl:text-7xl">
                      {`${data.predicted_cloud.toFixed(1)}%`}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FifthPattern;
