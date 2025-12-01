import { defineConfig } from "vitest/config";
import { loadEnv } from "vite";
import path from "node:path";

export default defineConfig(({ mode }) => {
  // Load env vars (e.g. VITE_PROXY_TARGET)
  const env = loadEnv(mode, process.cwd(), '')

  // Default to localhost:8092 if running outside docker, else use env var
  const apiTarget = env.VITE_PROXY_TARGET || 'http://localhost:8092'

  return {
    root: path.resolve(__dirname),
    build: {
      outDir: "dist",
      emptyOutDir: true
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src")
      }
    },
    server: {
      host: true, // Needed for Docker port mapping
      port: 5173,
      proxy: {
        // Proxy API requests to the Backend Container
        '/api': {
          target: apiTarget,
          changeOrigin: true,
          secure: false,
        },
        '/apps': {
          target: apiTarget,
          changeOrigin: true,
          secure: false,
        },
        // Proxy WebSocket requests too
        '/ws': {
          target: apiTarget.replace('http', 'ws'),
          ws: true,
          changeOrigin: true
        }
      }
    },
    test: {
      environment: "jsdom",
      globals: true
    }
  }
});
