import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";  
import Papa from "papaparse";
import Sidebar_Manager from "../components/Sidebar_Manager";
import CalendarTable from "../components/manager/CalendarTable";
import CalendarHeader from "../components/manager/CalendarHeader"; 

const Calendar = () => {
  const [data, setData] = useState([]);
  const [selectedMonth, setSelectedMonth] = useState(1);

  const { calendarId } = useParams();

  const months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
  ];

  const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

  useEffect(() => {
    fetch(`/${calendarId}.csv`)
      .then((response) => response.text())
      .then((csvText) => {
        Papa.parse(csvText, {
          complete: (result) => {
            setData(result.data);
          },
          header: false,
        });
      })
      .catch((error) => console.error("Erro ao carregar o CSV:", error));
  }, [calendarId]); 

  const downloadCSV = () => {
    const csvContent = data.map(row => row.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${calendarId}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="admin-container">
      <Sidebar_Manager />
      <div className="main-content">
        <CalendarHeader 
          months={months} 
          selectedMonth={selectedMonth} 
          setSelectedMonth={setSelectedMonth} 
          downloadCSV={downloadCSV}
        />
        <CalendarTable data={data} selectedMonth={selectedMonth} daysInMonth={daysInMonth} />
      </div>
    </div>
  );
};

export default Calendar;
