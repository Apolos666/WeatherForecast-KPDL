import React, { useState, useCallback } from 'react';

const useGetSpiderChartData = () => {
  const [loading, setLoading] = useState(false);
  const getSpiderChartData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8084/api/analysis/spiderchart?year=2024`,
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
      console.error(error);
      return { ok: false, data: [] };
    } finally {
      setLoading(false);
    }
  }, []);

  return { getSpiderChartData, loading };
};

export default useGetSpiderChartData;
