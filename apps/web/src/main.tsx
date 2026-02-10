import React from "react";
import 'prismjs/themes/prism-tomorrow.css';
import './styles/prism-overrides.css';
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./styles.css";
import { ThemeProvider } from "@/lib/theme";
import { ToastProvider } from "@/lib/toast";

import { ErrorBoundary } from '@/components/ErrorBoundary';

const root = createRoot(document.getElementById("root")!);
root.render(
  <ThemeProvider>
    <ToastProvider>
      <BrowserRouter>
        <ErrorBoundary>
          <App />
        </ErrorBoundary>
      </BrowserRouter>
    </ToastProvider>
  </ThemeProvider>
);
