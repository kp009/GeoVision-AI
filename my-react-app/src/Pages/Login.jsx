import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true); // Set loading to true while the API request is in progress

    try {
      // Step 1: Login to get the JWT token
      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await response.json();
      const { access_token, role } = data;

      if (!access_token) {
        throw new Error("Authentication failed");
      }

      // Store token and role in localStorage
      localStorage.setItem("user", JSON.stringify({ token: access_token, role }));
      console.log(localStorage)

      // Redirect based on role
      if (role === "superadmin") navigate("/superadmin");
      else if (role === "admin") navigate("/admin");
      else navigate("/user");

    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false); // Set loading to false after request completion
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="text"
        placeholder="Username"
        onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
        value={credentials.username}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        value={credentials.password}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
};

export default Login;
