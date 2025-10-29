import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  return (
    <div>
      <h1>Welcome to Trading App</h1>
      <Link to="/login">Login</Link> | <Link to="/signup">Signup</Link>
    </div>
  );
};

export default LandingPage;