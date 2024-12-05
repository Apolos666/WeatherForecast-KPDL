import { useState, useCallback, useEffect } from 'react';
import { useSignalR } from './useSignalR';

export interface SeasonalData {
  date: string;
  year: number;
  quarter: number;
  avgTemp: number;
  avgHumidity: number;
  totalPrecip: number;
  avgWind: number;
  avgPressure: number;
  maxTemp: number;
  minTemp: number;
}

const useGetSeasonalData = (year?: string, quarter?: string) => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<SeasonalData[]>([]);
  const connection = useSignalR();

  useEffect(() => {
    if (connection) {
      connection.start()
        .then(() => {
          connection.on('ReceiveSeasonalAnalysis', (seasonalAnalysis: SeasonalData) => {
            setData(prevData => {
              const newData = [...prevData];
              const index = newData.findIndex(item => item.date === seasonalAnalysis.date);
              if (index !== -1) {
                newData[index] = seasonalAnalysis;
              } else {
                newData.push(seasonalAnalysis);
              }
              return newData;
            });
          });
        })
        .catch(err => console.error('SignalR Connection Error:', err));

      // Cleanup function
      return () => {
        connection.off('ReceiveSeasonalAnalysis');
        connection.stop();
      };
    }
  }, [connection]);

  const getSeasonalData = useCallback(async () => {
    setLoading(true);
    try {
      let url = 'http://localhost:8084/api/analysis/seasonal';
      const params = new URLSearchParams();

      if (year) params.append('year', year);
      if (quarter) params.append('quarter', quarter);

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

      const result = await response.json();
      setData(result);
      return { ok: true, data: result };
    } catch (error) {
      console.error(error);
      return { ok: false, data: [] };
    } finally {
      setLoading(false);
    }
  }, [year, quarter]);

  return { getSeasonalData, loading, data };
};

export default useGetSeasonalData;
