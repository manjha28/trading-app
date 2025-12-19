import api from "./client";

export const getOpenTrades = async () => {
  const res = await api.get("/api/trades/open");
  return res.data;
};

export const getClosedTrades = async () => {
  const res = await api.get("/api/trades/closed");
  return res.data;
};
