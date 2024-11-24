"use client";
import { useEffect, useState, useRef, useLayoutEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

interface User {
  id: number;
  name: string;
  surname: string;
  patronymic: string;
  heart_rate: number;
  stress_index: number;
}

const DataTable = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [chartWidth, setChartWidth] = useState<number>(0);
  const [sortKey, setSortKey] = useState<string>("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:3001/events");

    eventSource.onmessage = (event) => {
      const newUsers = JSON.parse(event.data);
      setUsers(newUsers);
      setFilteredUsers(newUsers);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  useLayoutEffect(() => {
    if (chartContainerRef.current) {
      setChartWidth(chartContainerRef.current.offsetWidth);
    }

    const handleResize = () => {
      if (chartContainerRef.current) {
        setChartWidth(chartContainerRef.current.offsetWidth);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortOrder("asc");
    }
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    const query = event.target.value.toLowerCase();
    setSearchQuery(query);
    const filtered = users.filter((user) =>
      Object.values(user).some((value) =>
        value.toString().toLowerCase().includes(query)
      )
    );
    setFilteredUsers(filtered);
  };

  const sortedUsers = [...filteredUsers].sort((a, b) => {
    const aValue = a[sortKey as keyof User];
    const bValue = b[sortKey as keyof User];

    if (sortKey === "heart_rate" || sortKey === "stress_index") {
      return sortOrder === "asc" ? bValue - aValue : aValue - bValue;
    }

    if (aValue < bValue) {
      return sortOrder === "asc" ? -1 : 1;
    }
    if (aValue > bValue) {
      return sortOrder === "asc" ? 1 : -1;
    }
    return 0;
  });

  // Преобразуем данные для графика
  const chartData = users.map((user) => ({
    name: `${user.surname} ${user.name}`,
    heart_rate: user.heart_rate,
    stress_index: user.stress_index,
  }));

  return (
    <div>
      <h1>Таблица пользователей</h1>
      <div style={{ marginBottom: "20px" }}>
        <label htmlFor="sortSelect">Сортировать по:</label>
        <select
          id="sortSelect"
          value={sortKey}
          onChange={(e) => handleSort(e.target.value)}
        >
          <option value="id">ID</option>
          <option value="surname">Фамилия</option>
          <option value="name">Имя</option>
          <option value="patronymic">Отчество</option>
          <option value="heart_rate">ЧСС</option>
          <option value="stress_index">Индекс напряжения</option>
        </select>
      </div>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Фамилия</th>
            <th>Имя</th>
            <th>Отчество</th>
            <th>ЧСС</th>
            <th>Индекс напряжения</th>
          </tr>
        </thead>
        <tbody>
          {sortedUsers.map((user, index) => {
            const isRed = user.heart_rate >= 100 || user.stress_index >= 400;
            const isYellow =
              (user.heart_rate > 80 && user.heart_rate < 100) ||
              (user.stress_index > 100 && user.stress_index < 400);
            const rowColor = isRed ? "red" : isYellow ? "yellow" : "white";

            return (
              <tr key={user.id} style={{ backgroundColor: rowColor }}>
                <td>{user.id}</td>
                <td>{user.surname}</td>
                <td>{user.name}</td>
                <td>{user.patronymic}</td>
                <td>{user.heart_rate}</td>
                <td>{user.stress_index}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <div
        className="chart-container"
        ref={chartContainerRef}
        style={{ width: "100%", height: "400px" }}
      >
        <LineChart
          width={chartWidth}
          height={400}
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="heart_rate"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
          <Line type="monotone" dataKey="stress_index" stroke="#82ca9d" />
        </LineChart>
      </div>
    </div>
  );
};

export default DataTable;
