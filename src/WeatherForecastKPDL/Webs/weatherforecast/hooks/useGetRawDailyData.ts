import React, { useState, useCallback } from 'react';

const useGetRawDailyData = (startDate: string, endDate: string) => {
  const [loading, setLoading] = useState(false);

  const getRawData = useCallback(async () => {
    setLoading(true);
    try {
      console.log('Calling API with dates:', { startDate, endDate });

      const response = await fetch(
        `http://localhost:8084/api/weather/date-range?fromDate=${startDate}&toDate=${endDate}`,
        {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('API Response data:', data);
      return { ok: true, data };

    } catch (error) {
      console.error('API Error:', error);
      return { ok: false, data: [] };
    } finally {
      setLoading(false);
    }
  }, [startDate, endDate]);

  return { getRawData, loading };
};

export default useGetRawDailyData;
