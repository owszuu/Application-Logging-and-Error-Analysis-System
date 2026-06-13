import { useEffect, useState } from "react";
import { fetchJSON } from "../api";

export default function LiveLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const loadLogs = () => {
      fetchJSON("/logs/latest?limit=20")
        .then(setLogs)
        .catch(console.error);
    };

    loadLogs();

    const interval = setInterval(loadLogs, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>Latest Logs</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Service</th>
            <th>Level</th>
            <th>Message</th>
          </tr>
        </thead>

        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{new Date(log.timestamp).toLocaleString()}</td>
              <td>{log.service}</td>
              <td>{log.level}</td>
              <td>{log.message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}