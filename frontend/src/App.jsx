import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./login/Login";  
import Manager from "./Manager/manager";  
import Admin from "./Admin/Admin";
import Add_Algor from "./Admin/Add_Algor"; 
import List_Calendar from "./Manager/ListCalendar";
import Teams from "./Manager/Teams";
import Employer from "./Manager/Employer";
import Calendar from "./Manager/Calender";  
import CreateCalendar from "./Manager/CreateCalendar";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import NotFound from "./components/NotFound";

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          
          {/* aqu1 em baxio as rotas estao protegidas */}
          <Route path="/admin" element={<ProtectedRoute role="admin"><Admin /></ProtectedRoute>} />
          <Route path="/admin/add_algor" element={<ProtectedRoute role="admin"><Add_Algor /></ProtectedRoute>} />
          <Route path="/manager" element={<ProtectedRoute role="manager"><Manager /></ProtectedRoute>} />
          <Route path="/manager/listcalendar" element={<ProtectedRoute role="manager"><List_Calendar /></ProtectedRoute>} />
          <Route path="/manager/teams" element={<ProtectedRoute role="manager"><Teams /></ProtectedRoute>} />
          <Route path="/manager/employer" element={<ProtectedRoute role="manager"><Employer /></ProtectedRoute>} />
          <Route path="/manager/calendar/:calendarId" element={<ProtectedRoute role="manager"><Calendar /></ProtectedRoute>} />
          <Route path="/manager/createCalendar" element={<ProtectedRoute role="manager"><CreateCalendar /></ProtectedRoute>} />

          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
