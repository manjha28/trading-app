import React from 'react';

const Login: React.FC = () => {
  return (
    <div>
      <h2>Login Page</h2>
      <form>
        <label>Email:</label><br />
        <input type="email" name="email" /><br />
        <label>Password:</label><br />
        <input type="password" name="password" /><br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
