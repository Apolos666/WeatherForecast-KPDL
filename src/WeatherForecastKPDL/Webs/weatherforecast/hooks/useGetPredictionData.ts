import React, { useState, useCallback } from 'react';

const useGetPredictionData = () => {
  const [loading, setLoading] = useState(false);
  const getPredictionData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8084/api/prediction/next-day`,
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

  return { getPredictionData, loading };
};

export default useGetPredictionData;
