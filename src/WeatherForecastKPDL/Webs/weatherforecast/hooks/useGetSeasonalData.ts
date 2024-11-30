import React, { useState, useCallback } from 'react';

const useGetSeasonalData = () => {
  const [loading, setLoading] = useState(false);
  const getSeasonalData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8084/api/analysis/seasonal`,
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
      console.error(error);
      return { ok: false, data: [] };
    } finally {
      setLoading(false);
    }
  }, []);

  return { getSeasonalData, loading };
};

export default useGetSeasonalData;