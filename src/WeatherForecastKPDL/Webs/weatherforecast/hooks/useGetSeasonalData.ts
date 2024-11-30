import React, { useState, useCallback } from 'react';

const useGetSeasonalData = (year?: string, quarter?: string) => {
  const [loading, setLoading] = useState(false);

  const getSeasonalData = useCallback(async () => {
    setLoading(true);
    try {
      let url = 'http://localhost:8084/api/analysis/seasonal';
      const params = new URLSearchParams();

      // Thêm params nếu có giá trị
      if (year) params.append('year', year);
      if (quarter) params.append('quarter', quarter);

      // Chỉ thêm dấu ? và params nếu có ít nhất 1 param
      if (params.toString()) {
        url += `?${params.toString()}`;
      }

      const response = await fetch(url, {
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
  }, [year, quarter]);

  return { getSeasonalData, loading };
};

export default useGetSeasonalData;
