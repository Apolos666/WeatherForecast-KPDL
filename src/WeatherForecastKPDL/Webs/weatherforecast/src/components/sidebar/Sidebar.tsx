'use client';
import Link from 'next/link';
import React from 'react';
import { usePathname } from 'next/navigation';
import { FaChartBar, FaChartPie, FaChartLine } from 'react-icons/fa';
import Image from 'next/image';

const Sidebar = () => {
  const pathname = usePathname();

  const menuItems = [
    {
      label: 'Raw Data Pattern',
      icon: <FaChartLine />,
      link: '/pattern1/date',
    },
    { label: 'Daily Pattern', icon: <FaChartBar />, link: '/pattern2' },
    { label: 'Seasonal Pattern', icon: <FaChartPie />, link: '/pattern3' },
    { label: 'Correlation Pattern', icon: <FaChartLine />, link: '/pattern4' },
    { label: 'Prediction', icon: <FaChartBar />, link: '/pattern5' },
  ];

  return (
    <div className="fixed top-0 left-0 h-full w-72 bg-[#212531] shadow-lg transition-transform transform duration-300 ease-in-out translate-x-0 md:translate-x-0">
      {/* Header */}
      <div className="px-6 py-4 border-b  border-gray-600">
        <Link href={'/'}>
          <h5 className="flex flex-row justify-center items-center gap-4 text-xl font-semibold text-white tracking-wide">
            <Image src={'/cloudy.png'} width={28} height={28} alt="logo" />
            <span className="mt-2">Weather Forecast</span>
          </h5>
        </Link>
      </div>

      <div className="pt-3 px-3 text-xl text-gray-300 font-semibold">
        Pattern
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-4">
        {menuItems.map((item, idx) => {
          const isActive = pathname === item.link;
          return (
            <Link href={item.link} key={idx}>
              <div
                className={`flex items-center justify-between p-3 rounded-lg cursor-pointer transition-transform ease-in-out duration-200 ${
                  isActive
                    ? 'bg-blue-600 text-white scale-105'
                    : 'hover:bg-gray-700 hover:text-gray-200 hover:scale-105'
                }`}
              >
                <div className="flex items-center space-x-4 text-gray-300">
                  <div className="text-xl">{item.icon}</div>
                  <span className="font-medium">{item.label}</span>
                </div>
              </div>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="absolute bottom-4 left-0 w-full px-4 text-center">
        <p className="text-gray-400 text-xs">
          Made with{' '}
          <a
            href="https://react-icons.github.io/react-icons/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-400 transition duration-300 ease-in-out"
          >
            3CBĐ
          </a>
        </p>
      </div>
    </div>
  );
};

export default Sidebar;
