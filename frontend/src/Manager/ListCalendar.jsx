import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";  
import Sidebar_Manager from "../components/Sidebar_Manager"; 
import BaseUrl from "../components/BaseUrl";  
import axios from "axios";  

const ListCalendar = () => {
  const [calendars, setCalendars] = useState([]);  
  const [loading, setLoading] = useState(true);  
  const [error, setError] = useState(null);  

  useEffect(() => {
    const fetchCalendars = async () => {
      try {
        const baseUrl = BaseUrl(); 
        console.log("Base URL: ", baseUrl);

        const response = await axios.get(`${baseUrl}schedules/fetch`);
        console.log("Resposta da API:", response);

        if (response.data) {
          setCalendars(response.data);  
        } else {
          setError("Nenhum dado encontrado.");
        }
        
      } catch (error) {
        setError("Erro ao buscar calendários. Tente novamente.");
        console.error("Erro ao buscar calendários:", error);
      } finally {
        setLoading(false);  
      }
    };

    fetchCalendars();  
  }, []);

  if (loading) {
    return (
      <div className="admin-container">
        <Sidebar_Manager />
        <div className="main-content">
          <h2 className="heading">Carregando...</h2>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-container">
        <Sidebar_Manager />
        <div className="main-content">
          <h2 className="heading">{error}</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <Sidebar_Manager />  
      <div className="main-content">
        <h2 className="heading">List Calendar</h2>
        {calendars.length > 0 ? (
          calendars.map((calendar) => (
            <Link 
              key={calendar.id} 
              to={`/manager/calendar/${calendar.id}`} 
              className="btn"
            >
              {calendar.title}  
            </Link>
          ))
        ) : (
          <p>Nenhum calendário encontrado.</p> 
        )}
      </div> 
    </div>
  );
};

export default ListCalendar;
