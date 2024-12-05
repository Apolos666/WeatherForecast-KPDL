import { HubConnectionBuilder, HubConnection } from '@microsoft/signalr';
import { useState, useEffect } from 'react';

export const useSignalR = () => {
  const [connection, setConnection] = useState<HubConnection | null>(null);

  useEffect(() => {
    const newConnection = new HubConnectionBuilder()
      .withUrl('http://localhost:8084/hubs/analysis')
      .withAutomaticReconnect()
      .build();

    setConnection(newConnection);

    return () => {
      newConnection.stop();
    };
  }, []);

  return connection;
};
