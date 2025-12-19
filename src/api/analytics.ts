import api from "./client";

export const getOverview = async () => {
  const res = await api.get("/api/analytics/overview");
  return res.data;
};

export const getEquityCurve = async () => {
  const res = await api.get("/api/analytics/equity-curve");
  return res.data;
};
