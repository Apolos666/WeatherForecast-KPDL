import React, { useState, useCallback } from 'react';

const useGetPredictionSeasonal = () => {
  const [loading, setLoading] = useState(false);
  const getPredictionSeasonal = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8084/api/clustering/predict-season-probability`,
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

  return { getPredictionSeasonal, loading };
};

export default useGetPredictionSeasonal;
