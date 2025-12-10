import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Update if using a different port or deployed backend
  headers: {
    'Content-Type': 'application/json',
  },
});

export default instance;