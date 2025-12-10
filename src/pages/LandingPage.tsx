import React from "react";
import { Link } from "react-router-dom";
import { startGoogleLogin } from "../api/auth";
import "./auth.css";

const Landing: React.FC = () => {
  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-left">
          <h1 className="brand">TradeTrack</h1>
          <p className="tagline">
            Your trading journal, automated. Connect brokers, review your edge,
            stop repeating the same dumb mistakes.
          </p>

          <div className="cta-buttons">
            <Link to="/signup" className="btn primary">
              Get started – it&apos;s free
            </Link>
            <Link to="/login" className="btn ghost">
              I already have an account
            </Link>
          </div>

          <div className="divider">
            <span>or</span>
          </div>

          <button className="btn google" onClick={startGoogleLogin}>
            <img
              src="https://www.svgrepo.com/show/475656/google-color.svg"
              alt="Google"
              className="google-icon"
            />
            Continue with Google
          </button>

          <p className="small-note">
            No spam. No tips. Just clean stats and honest journaling.
          </p>
        </div>

        <div className="auth-right">
          <div className="fake-dashboard-card">
            <h3>Today&apos;s P&amp;L</h3>
            <p className="pnl-positive">+ ₹ 7,850.00</p>
            <div className="mini-stats">
              <div>
                <span>Win rate</span>
                <strong>62%</strong>
              </div>
              <div>
                <span>Trades</span>
                <strong>14</strong>
              </div>
              <div>
                <span>RR</span>
                <strong>1.8R</strong>
              </div>
            </div>
            <p className="tiny-text">
              Preview only – live data will come from your brokers.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
