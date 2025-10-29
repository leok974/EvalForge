import React from "react";
import { createRoot } from "react-dom/client";
import DevUI from "./pages/DevUI";
import "./styles.css";

const root = createRoot(document.getElementById("root")!);
root.render(<DevUI />);
