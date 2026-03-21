import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/auth": "http://localhost:8000",
      "/groups": "http://localhost:8000",
      "/workouts": "http://localhost:8000",
      "/leaderboard": "http://localhost:8000",
      "/reactions": "http://localhost:8000",
      "/health": "http://localhost:8000",
    },
  },
});
