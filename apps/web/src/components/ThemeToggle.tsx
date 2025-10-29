import React from "react";
import { useTheme } from "@/lib/theme";

export const ThemeToggle: React.FC = () => {
  const { theme, toggle } = useTheme();
  return (
    <button className="btn btn-ghost" aria-label="Toggle theme" onClick={toggle}>
      {theme === "dark" ? "🌙 Dark" : "☀️ Light"}
    </button>
  );
};
