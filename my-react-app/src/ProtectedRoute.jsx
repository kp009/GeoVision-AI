import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = ({ role, allowedRoles }) => {
  if (role === null) {
    return <Navigate to="/" />; // Redirect to login page if role is null
  }

  if (!allowedRoles.includes(role)) {
    return <Navigate to="/unauthorized" />; // Access denied page
  }

  return <Outlet />;
};

export default ProtectedRoute;
