import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";
import { ThemeProvider } from "@/lib/theme";
import { ToastProvider } from "@/lib/toast";

const root = createRoot(document.getElementById("root")!);
root.render(
  <ThemeProvider>
    <ToastProvider>
      <App />
    </ToastProvider>
  </ThemeProvider>
);
