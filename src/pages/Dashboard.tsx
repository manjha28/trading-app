import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./auth.css";

import { getOverview } from "../api/analytics";
import { getOpenTrades, getClosedTrades } from "../api/trades";

/* ---------------- TYPES ---------------- */

interface User {
  id: number;
  name: string;
  email: string;
}

interface Overview {
  total_trades: number;
  win_rate: number;
  gross_pnl: number;
  net_pnl: number;
}

interface Trade {
  id: number;
  symbol: string;
  side: string;
  quantity: number;
  entry_price: number;
  exit_price?: number;
  pnl?: number;
}

/* ---------------- COMPONENT ---------------- */

const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [overview, setOverview] = useState<Overview | null>(null);
  const [openTrades, setOpenTrades] = useState<Trade[]>([]);
  const [closedTrades, setClosedTrades] = useState<Trade[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const userStr = localStorage.getItem("user");

    if (!token || !userStr) {
      navigate("/login");
      return;
    }

    try {
      setUser(JSON.parse(userStr));
    } catch {
      navigate("/login");
      return;
    }

    async function loadData() {
      try {
        const o = await getOverview();
        const open = await getOpenTrades();
        const closed = await getClosedTrades();

        if (
  typeof o === "object" &&
  o !== null &&
  typeof o.total_trades === "number"
) {
  setOverview(o);
} else {
  console.error("Invalid overview payload:", o);
  setOverview(null);
}

        setOpenTrades(Array.isArray(open) ? open : []);
        setClosedTrades(Array.isArray(closed) ? closed : []);
      } catch (err: any) {
        console.error("Dashboard API error:", err);
        if (err?.response?.status === 401) {
          navigate("/login");
        }
      }
    }

    loadData();
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  }

  if (!overview || typeof overview !== "object") {
    return (
      <div className="auth-page">
        <div className="auth-card narrow">Loading dashboard…</div>
      </div>
    );
  }

  return (
    <div className="auth-page">
      <div className="auth-card wide">
        <h2>Trading Dashboard</h2>
        <p className="subheading">
          Welcome{user ? `, ${user.name}` : ""}
        </p>

        {/* KPI SECTION */}
        <div style={{ display: "flex", gap: 16, marginTop: 16 }}>
<Kpi label="Net P&L" value={typeof overview.net_pnl === "number" ? overview.net_pnl : "0"} />
<Kpi label="Win Rate" value={typeof overview.win_rate === "number" ? `${overview.win_rate}%` : "0"} />
<Kpi label="Trades" value={typeof overview.total_trades === "number" ? overview.total_trades : "0"} />

        </div>

        {/* OPEN TRADES */}
        <h3 style={{ marginTop: 32 }}>Open Trades</h3>
        <TradesTable trades={openTrades} />

        {/* CLOSED TRADES */}
        <h3 style={{ marginTop: 32 }}>Closed Trades</h3>
        <TradesTable trades={closedTrades} />

        <div style={{ marginTop: 24 }}>
          <Link to="/" className="btn ghost">
            ← Back to landing
          </Link>
          <button
            className="btn primary"
            style={{ marginLeft: 8 }}
            onClick={handleLogout}
          >
            Log out
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

/* ---------------- SUB COMPONENTS ---------------- */

function Kpi({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="kpi">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
    </div>
  );
}

function TradesTable({ trades }: { trades: Trade[] }) {
  if (!trades.length) {
    return <p className="small-note">No trades</p>;
  }

  return (
    <table className="trades-table">
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Side</th>
          <th>Qty</th>
          <th>Entry</th>
          <th>Exit</th>
          <th>P&amp;L</th>
        </tr>
      </thead>
      <tbody>
        {trades.map((t) => (
          <tr key={t.id}>
            <td>{t.symbol}</td>
            <td>{t.side}</td>
            <td>{t.quantity}</td>
            <td>{t.entry_price}</td>
            <td>{t.exit_price ?? "-"}</td>
            <td>{typeof t.pnl === "number" ? t.pnl : "-"}</td>

          </tr>
        ))}
      </tbody>
    </table>
  );
}
