import express from "express";
import cors from "cors";

export const createServer = () => {
  const app = express();

  app.use(cors());
  app.use(express.json());

  // health check
  app.get("/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  return app;
};
