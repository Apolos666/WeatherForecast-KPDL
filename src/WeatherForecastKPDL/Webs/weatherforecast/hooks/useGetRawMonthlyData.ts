import React, { useState, useCallback } from 'react';

const useGetRawMonthlyData = (monthRange: number) => {
  const [loading, setLoading] = useState(false);

  const getRawData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8084/api/weather/months-ago?monthsAgo=${monthRange}`,
        {
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
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
  }, [monthRange]);

  return { getRawData, loading };
};

export default useGetRawMonthlyData;
