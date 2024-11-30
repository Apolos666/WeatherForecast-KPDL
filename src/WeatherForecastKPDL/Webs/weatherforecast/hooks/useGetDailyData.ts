import { useState, useCallback } from 'react';

const useGetDailyData = () => {
  const [loading, setLoading] = useState(false);

  const getDailyData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8084/api/analysis/daily`, {
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      });

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

  return { getDailyData, loading };
};

export default useGetDailyData;
