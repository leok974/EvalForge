import React from "react";
import { createRoot } from "react-dom/client";
import DevUI from "./pages/DevUI";
import "./styles.css";
import { ThemeProvider } from "@/lib/theme";
import { ToastProvider } from "@/lib/toast";

const root = createRoot(document.getElementById("root")!);
root.render(
  <ThemeProvider>
    <ToastProvider>
      <DevUI />
    </ToastProvider>
  </ThemeProvider>
);
