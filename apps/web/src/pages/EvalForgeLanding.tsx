import { motion } from "framer-motion";
import { ArrowRight, Gamepad2, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

// Adjusted path to the logo found in public/branding/logo.png
const LOGO_SRC = "/branding/logo.png";

export default function EvalForgeLanding() {
    return (
        <div className="relative min-h-screen overflow-hidden bg-gradient-to-b from-slate-950 via-slate-950 to-slate-900 text-slate-50">
            {/* Background orbs */}
            <div className="pointer-events-none absolute inset-0">
                <div className="absolute -top-24 left-0 h-64 w-64 rounded-full bg-emerald-500/20 blur-3xl" />
                <div className="absolute bottom-0 right-[-4rem] h-72 w-72 rounded-full bg-indigo-500/20 blur-3xl" />
                <div className="absolute inset-x-0 bottom-1/3 h-px bg-gradient-to-r from-transparent via-emerald-400/40 to-transparent" />
            </div>

            {/* Subtle grid overlay */}
            <div className="pointer-events-none absolute inset-0 opacity-[0.08]">
                <div className="h-full w-full bg-[radial-gradient(circle_at_1px_1px,#4b5563_0.5px,transparent_0)] bg-[size:32px_32px]" />
            </div>

            {/* Main content */}
            <div className="relative z-10 flex min-h-screen flex-col">
                {/* Top nav / small badge */}
                <header className="mx-auto flex w-full max-w-5xl items-center justify-between px-4 py-6">
                    <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-[0.2em] text-slate-400">
                        <span className="inline-flex h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(74,222,128,0.8)]" />
                        <span>EvalForge</span>
                    </div>
                    <div className="hidden items-center gap-3 text-xs text-slate-400 sm:flex">
                        <span className="flex items-center gap-1">
                            <Sparkles className="h-3 w-3" />
                            AI Engineer Arcade
                        </span>
                        <span className="h-1 w-1 rounded-full bg-slate-600" />
                        <span>Cloud Run · Postgres · Agents</span>
                    </div>
                </header>

                {/* Hero / center logo */}
                <main className="flex flex-1 items-center justify-center px-4 pb-16 pt-4">
                    <div className="grid w-full max-w-5xl gap-10 md:grid-cols-[minmax(0,3fr)_minmax(0,2fr)] md:items-center">
                        {/* Left: logo + pitch */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, ease: "easeOut" }}
                            className="flex flex-col items-center md:items-start"
                        >
                            {/* Logo with glow */}
                            <div className="relative mb-8 flex items-center justify-center">
                                <div className="absolute h-40 w-40 rounded-full bg-emerald-500/20 blur-2xl md:h-56 md:w-56" />
                                <motion.div
                                    className="relative p-2"
                                    initial={{ scale: 0.9, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    transition={{ duration: 0.5, delay: 0.1 }}
                                >
                                    <img
                                        src={LOGO_SRC}
                                        alt="EvalForge logo"
                                        className="h-20 w-auto md:h-28"
                                    />
                                </motion.div>
                            </div>

                            <motion.h1
                                className="mb-3 text-center text-3xl font-semibold tracking-tight text-slate-50 md:text-left md:text-4xl lg:text-5xl"
                                initial={{ opacity: 0, y: 8 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2, duration: 0.5 }}
                            >
                                The training ground for{" "}
                                <span className="bg-gradient-to-r from-emerald-400 via-cyan-400 to-indigo-400 bg-clip-text text-transparent">
                                    AI engineers
                                </span>
                                .
                            </motion.h1>

                            <motion.p
                                className="mb-6 max-w-xl text-center text-sm text-slate-300 md:text-left md:text-base"
                                initial={{ opacity: 0, y: 8 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.3, duration: 0.5 }}
                            >
                                EvalForge turns real-world ML, infra, and agent work into
                                quests, boss fights, and Legendary trials. Practice hard skills,
                                ship real systems, and let evaluators and agents keep score.
                            </motion.p>

                            <motion.div
                                className="flex flex-col items-center gap-3 md:flex-row md:items-center"
                                initial={{ opacity: 0, y: 6 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.4, duration: 0.4 }}
                            >
                                <Button
                                    size="lg"
                                    className="group w-full gap-2 bg-emerald-500 text-slate-950 hover:bg-emerald-400 md:w-auto"
                                    onClick={() => {
                                        // Navigate to arcade
                                        window.location.href = "/arcade";
                                    }}
                                >
                                    <Gamepad2 className="h-4 w-4" />
                                    Enter the Arcade
                                    <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                                </Button>

                                <Button
                                    size="lg"
                                    variant="outline"
                                    className="w-full border-slate-600 bg-black/40 text-slate-100 hover:bg-slate-900 md:w-auto"
                                    onClick={() => {
                                        window.open("https://github.com/leok974/EvalForge", "_blank");
                                    }}
                                >
                                    Learn how it works
                                </Button>
                            </motion.div>

                            <motion.div
                                className="mt-4 flex items-center gap-2 text-xs text-slate-400"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.7, duration: 0.4 }}
                            >
                                <span className="inline-flex h-1.5 w-1.5 rounded-full bg-emerald-400" />
                                <span>Legendary tracks · Boss rubrics · Cloud Run · Postgres · Agents</span>
                            </motion.div>
                        </motion.div>

                        {/* Right: feature cards */}
                        <motion.div
                            className="space-y-4"
                            initial={{ opacity: 0, x: 30 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.6, ease: "easeOut", delay: 0.2 }}
                        >
                            <Card className="border-slate-700/70 bg-slate-900/60 backdrop-blur">
                                <CardContent className="space-y-2 p-4">
                                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-400">
                                        Worlds & Bosses
                                    </p>
                                    <p className="text-sm text-slate-100">
                                        Explore Python, JS/TS, SQL, Infra, Git, Agents, and ML
                                        as interconnected worlds, each with questlines and
                                        senior-tier Legendary bosses.
                                    </p>
                                </CardContent>
                            </Card>

                            <Card className="border-slate-700/70 bg-slate-900/60 backdrop-blur">
                                <CardContent className="space-y-2 p-4">
                                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-400">
                                        Evaluators & Agents
                                    </p>
                                    <p className="text-sm text-slate-100">
                                        Every boss fight is graded by structured rubrics and LLM
                                        judge agents, giving concrete feedback on architecture,
                                        tradeoffs, and reliability.
                                    </p>
                                </CardContent>
                            </Card>

                            <Card className="border-slate-700/70 bg-slate-900/60 backdrop-blur">
                                <CardContent className="space-y-2 p-4">
                                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-indigo-400">
                                        Practice Gauntlet
                                    </p>
                                    <p className="text-sm text-slate-100">
                                        Spin up daily trials across worlds, track streaks, and
                                        see your growth as an AI engineer over time.
                                    </p>
                                </CardContent>
                            </Card>
                        </motion.div>
                    </div>
                </main>

                {/* Footer */}
                <footer className="relative z-10 border-t border-slate-800/70 bg-black/20">
                    <div className="mx-auto flex w-full max-w-5xl flex-col items-center justify-between gap-3 px-4 py-4 text-xs text-slate-500 md:flex-row">
                        <span>© {new Date().getFullYear()} EvalForge. Forged by Leo Klemet.</span>
                        <div className="flex items-center gap-3">
                            <a
                                href="https://www.leoklemet.com"
                                target="_blank"
                                rel="noreferrer"
                                className="hover:text-slate-300"
                            >
                                Portfolio
                            </a>
                            <span className="h-3 w-px bg-slate-700" />
                            <span className="flex items-center gap-1">
                                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                                Live on Cloud Run
                            </span>
                        </div>
                    </div>
                </footer>
            </div>
        </div>
    );
}
