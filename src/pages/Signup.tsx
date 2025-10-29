import React from 'react';

const Signup: React.FC = () => {
  return (
    <div>
      <h2>Signup Page</h2>
      <form>
        <label>Email:</label><br />
        <input type="email" name="email" /><br />
        <label>Password:</label><br />
        <input type="password" name="password" /><br />
        <button type="submit">Signup</button>
      </form>
    </div>
  );
};

export default Signup;