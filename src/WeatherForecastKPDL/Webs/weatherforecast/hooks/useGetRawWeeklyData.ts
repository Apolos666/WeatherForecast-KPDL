import React, { useState, useCallback } from 'react';

const useGetRawWeeklyData = (weekRange: number) => {
  const [loading, setLoading] = useState(false);

  const getRawData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8084/api/weather/weeks-ago?weeksAgo=${weekRange}`,
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
      return { ok: true, data };
    } catch (error) {
      console.error('API Error:', error);
      return { ok: false, data: [] };
    } finally {
      setLoading(false);
    }
  }, [weekRange]);

  return { getRawData, loading };
};

export default useGetRawWeeklyData;
