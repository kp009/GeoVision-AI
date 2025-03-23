import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SuperAdminDashboard from "./Pages/SuperAdminDashboard";
import AdminDashboard from "./Pages/AdminDashboard";
import UserDashboard from "./Pages/UserDashboard";
import Login from "./Pages/Login";
import ProtectedRoute from "./ProtectedRoute";
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    console.log(storedUser)
    console.log(user?.role)
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <h1>Loading...</h1>; // Show loading until the user state is initialized
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />

        {/* SuperAdmin Dashboard */}
        <Route element={<ProtectedRoute role={user?.role} allowedRoles={['superadmin']} />}>
          <Route path="/superadmin" element={<SuperAdminDashboard />} />
        </Route>

        {/* Admin Dashboard */}
        <Route element={<ProtectedRoute role={user?.role} allowedRoles={['admin', 'superadmin']} />}>
          <Route path="/admin" element={<AdminDashboard />} />
        </Route>

        {/* User Dashboard */}
        <Route element={<ProtectedRoute role={user?.role} allowedRoles={['user', 'admin', 'superadmin']} />}>
          <Route path="/user" element={<UserDashboard />} />
        </Route>

        <Route path="/unauthorized" element={<h1>Access Denied</h1>} />
      </Routes>
    </Router>
  );
};

export default App;
