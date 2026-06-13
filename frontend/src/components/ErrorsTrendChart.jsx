import { useEffect, useState } from "react";
import { fetchJSON } from "../api";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip
} from "recharts";

export default function ErrorsTrendChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchJSON("/stats/errors-trend")
      .then((res) => {
        console.log("TREND:", res);
        setData(res);
      })
      .catch(console.error);
  }, []);

  return (
    <div>
      <h2>Error Trend</h2>

      <LineChart
        width={800}
        height={300}
        data={data}
      >
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />

        <Line
          type="monotone"
          dataKey="count"
          stroke="#3366ff"
          strokeWidth={2}
          dot={{ r: 5 }}
        />
      </LineChart>
    </div>
  );
}