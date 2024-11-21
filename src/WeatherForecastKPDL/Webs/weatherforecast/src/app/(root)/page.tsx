import React from 'react';

const HomePage = () => {
  return (
    <div className="h-screen bg-[url('/bg.jpg')] bg-cover bg-center text-white flex flex-col items-center justify-center">
      <div className=" h-[95%] w-[95%] bg-gray-400 rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 border border-gray-100 flex flex-col justify-center items-center">
        <h1 className="text-7xl font-semibold text-gray-200">
          Weather Forecast
        </h1>
        <p className="text-xl text-gray-200 text-center max-w-3xl">
          Welcome to Weather Forecast! Get real-time updates on weather
          conditions, including temperature, humidity, and precipitation. Stay
          informed and plan your day with confidence.
        </p>
      </div>
    </div>
  );
};

export default HomePage;
