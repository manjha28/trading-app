import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./auth.css";

interface User {
  id: number;
  name: string;
  email: string;
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const userStr = localStorage.getItem("user");

    if (!token || !userStr) {
      // no auth → kick to login
      navigate("/login");
      return;
    }

    try {
      setUser(JSON.parse(userStr));
    } catch {
      navigate("/login");
    }
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  }

  return (
    <div className="auth-page">
      <div className="auth-card narrow">
        <h2>Trading Dashboard</h2>
        <p className="subheading">
          Welcome{user ? `, ${user.name}` : ""}. This is where your journal will live.
        </p>

        <div style={{ marginTop: 16, marginBottom: 16 }}>
          <p className="small-note">
            Next steps: we&apos;ll add:
          </p>
          <ul className="small-note">
            <li>List of trades</li>
            <li>P&amp;L stats</li>
            <li>Broker connections</li>
          </ul>
        </div>

        <Link to="/" className="btn ghost full" style={{ marginBottom: 8 }}>
          ← Back to landing
        </Link>

        <button className="btn primary full" onClick={handleLogout}>
          Log out
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
