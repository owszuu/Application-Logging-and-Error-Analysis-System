import ErrorsByServiceChart from "../components/ErrorsByServiceChart";
import ErrorsTrendChart from "../components/ErrorsTrendChart";
import LiveLogs from "../components/LiveLogs";

export default function Dashboard() {
  return (
    <div style={{ padding: 20 }}>
      <h1>Application Logging Dashboard</h1>

      <ErrorsByServiceChart />

      <br />

      <ErrorsTrendChart />

      <br />

      <LiveLogs />
    </div>
  );
}