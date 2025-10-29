import React, { createContext, useContext, useEffect, useState } from "react";

type Theme = "light" | "dark";
type Ctx = { theme: Theme; setTheme: (t: Theme) => void; toggle: () => void; };

const ThemeCtx = createContext<Ctx | null>(null);

function getInitial(): Theme {
  if (typeof window === "undefined") return "dark";
  const stored = localStorage.getItem("evalforge:theme") as Theme | null;
  if (stored) return stored;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export const ThemeProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>(getInitial());
  useEffect(() => {
    const html = document.documentElement;
    if (theme === "dark") html.classList.add("dark"); else html.classList.remove("dark");
    localStorage.setItem("evalforge:theme", theme);
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);
  return (
    <ThemeCtx.Provider value={{ theme, setTheme, toggle: () => setTheme(p => p === "dark" ? "light" : "dark") }}>
      {children}
    </ThemeCtx.Provider>
  );
};

export function useTheme() {
  const ctx = useContext(ThemeCtx);
  if (!ctx) throw new Error("ThemeProvider missing");
  return ctx;
}
