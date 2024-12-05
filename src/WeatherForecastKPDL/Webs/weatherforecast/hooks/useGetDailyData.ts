import { useState, useCallback, useEffect } from 'react';
import { useSignalR } from './useSignalR';

interface DailyAnalysis {
  date: string;
  averageTemperature: number;
  averageHumidity: number;
  averageWindSpeed: number;
  totalPrecipitation: number;
  averagePressure: number;
}

const useGetDailyData = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<DailyAnalysis[]>([]);
  const connection = useSignalR();

  useEffect(() => {
    if (connection) {
      connection.start()
        .then(() => {
          connection.on('ReceiveDailyAnalysis', (newData: DailyAnalysis) => {
            setData(prevData => {
              const updatedData = [...prevData];
              const index = updatedData.findIndex(item => item.date === newData.date);
              if (index !== -1) {
                updatedData[index] = newData;
              } else {
                updatedData.push(newData);
              }
              return updatedData;
            });
          });
        });
    }
  }, [connection]);

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

      const fetchedData = await response.json();
      setData(fetchedData); // Update the same data state
      return { ok: true, data: fetchedData };
    } catch (error) {
      console.error(error);
      return { ok: false, data: [] as DailyAnalysis[] };
    } finally {
      setLoading(false);
    }
  }, []);

  return { getDailyData, loading, data };
};
export default useGetDailyData;