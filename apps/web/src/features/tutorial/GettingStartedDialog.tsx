import * as React from "react";
import { Compass, Hammer, Cpu, Swords } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

type GettingStartedDialogProps = {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onStartStarterQuest: () => void;
};

export function GettingStartedDialog({
    open,
    onOpenChange,
    onStartStarterQuest,
}: GettingStartedDialogProps) {
    const handleClose = () => {
        onOpenChange(false);
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-3xl border-slate-800 bg-slate-950/95 text-slate-50">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2 text-xl md:text-2xl">
                        <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400">
                            ⚔️
                        </span>
                        Welcome to EvalForge
                    </DialogTitle>
                    <DialogDescription className="mt-2 text-sm text-slate-300">
                        A quick tour of the UI, so you know where to start and how to find quests
                        and boss fights.
                    </DialogDescription>
                </DialogHeader>

                <div className="mt-4 grid gap-4 md:grid-cols-2">
                    <Card className="border-slate-800 bg-slate-900/70">
                        <CardContent className="space-y-2 p-4">
                            <div className="flex items-center gap-2">
                                <Compass className="h-4 w-4 text-emerald-400" />
                                <p className="text-sm font-semibold text-slate-100">Orion – Worlds</p>
                            </div>
                            <p className="text-xs text-slate-300">
                                Orion is your world map. Choose a discipline (Python, ML, Infra, Git,
                                Agents, UI, etc.) and see its ladder of tracks and bosses. Use this
                                view to decide which world you want to focus on.
                            </p>
                            <Badge
                                variant="outline"
                                className="border-emerald-500/50 bg-emerald-500/10 text-[10px] uppercase tracking-[0.16em]"
                            >
                                Start here to pick a world
                            </Badge>
                        </CardContent>
                    </Card>

                    <Card className="border-slate-800 bg-slate-900/70">
                        <CardContent className="space-y-2 p-4">
                            <div className="flex items-center gap-2">
                                <Hammer className="h-4 w-4 text-cyan-400" />
                                <p className="text-sm font-semibold text-slate-100">
                                    Workshop – Quests & Bosses
                                </p>
                            </div>
                            <p className="text-xs text-slate-300">
                                The Workshop is where you actually play: you run quests, fight bosses,
                                and see structured feedback. When you click a node on a ladder, it
                                opens here with the quest text, acceptance criteria, and submit tools.
                            </p>
                            <Badge
                                variant="outline"
                                className="border-cyan-500/50 bg-cyan-500/10 text-[10px] uppercase tracking-[0.16em]"
                            >
                                This is your main arena
                            </Badge>
                        </CardContent>
                    </Card>

                    <Card className="border-slate-800 bg-slate-900/70">
                        <CardContent className="space-y-2 p-4">
                            <div className="flex items-center gap-2">
                                <Swords className="h-4 w-4 text-indigo-400" />
                                <p className="text-sm font-semibold text-slate-100">
                                    Practice Gauntlet – Daily Trials
                                </p>
                            </div>
                            <p className="text-xs text-slate-300">
                                The Gauntlet serves you a daily mix of quests and boss rematches across
                                worlds. Use it when you want a focused “training session” without
                                choosing manually.
                            </p>
                            <Badge
                                variant="outline"
                                className="border-indigo-500/50 bg-indigo-500/10 text-[10px] uppercase tracking-[0.16em]"
                            >
                                Great for warmups & streaks
                            </Badge>
                        </CardContent>
                    </Card>

                    <Card className="border-slate-800 bg-slate-900/70">
                        <CardContent className="space-y-2 p-4">
                            <div className="flex items-center gap-2">
                                <Cpu className="h-4 w-4 text-amber-400" />
                                <p className="text-sm font-semibold text-slate-100">
                                    Cyberdeck – Agents & Evaluators
                                </p>
                            </div>
                            <p className="text-xs text-slate-300">
                                The Cyberdeck is your lab for judge prompts, ZERO runs, and QA tools.
                                It’s where you peek under the hood of the evaluators and tune how bosses
                                score your work.
                            </p>
                            <Badge
                                variant="outline"
                                className="border-amber-500/50 bg-amber-500/10 text-[10px] uppercase tracking-[0.16em]"
                            >
                                Advanced: tweak the evaluators
                            </Badge>
                        </CardContent>
                    </Card>
                </div>

                <div className="mt-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                    <div className="text-xs text-slate-400">
                        <p className="font-mono uppercase tracking-[0.18em] text-emerald-400">
                            First step
                        </p>
                        <p className="mt-1">
                            We recommend starting with the Python world and your first unlocked quest.
                        </p>
                    </div>
                    <div className="flex flex-col gap-2 md:flex-row">
                        <Button
                            variant="outline"
                            size="sm"
                            className="border-slate-700 bg-slate-900 text-slate-200 hover:bg-slate-800"
                            onClick={handleClose}
                        >
                            Explore on my own
                        </Button>
                        <Button
                            size="sm"
                            className="bg-emerald-500 text-slate-950 hover:bg-emerald-400"
                            onClick={onStartStarterQuest}
                        >
                            Start your first quest
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
}
