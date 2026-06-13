import { useEffect, useState } from "react";
import { fetchJSON } from "../api";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip
} from "recharts";

export default function ErrorsByServiceChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchJSON("/stats/errors-by-service")
      .then((res) => {
        console.log("SERVICES:", res);
        setData(res);
      })
      .catch(console.error);
  }, []);

  return (
    <div>
      <h2>Errors By Service</h2>

      <BarChart
        width={800}
        height={300}
        data={data}
      >
        <XAxis dataKey="_id" />
        <YAxis />
        <Tooltip />

        <Bar
          dataKey="count"
          fill="#ff4444"
        />
      </BarChart>
    </div>
  );
}