/**
 * Scoreboard component for displaying Judge grading results
 */
import React from "react";

export interface GradeData {
  coverage: number;
  correctness: number;
  clarity: number;
  comment: string;
}

export function Scoreboard({ grade }: { grade?: GradeData }) {
  if (!grade) {
    return (
      <div className="text-sm text-muted-foreground italic">
        Submit code to Judge to see your rubric scores here.
      </div>
    );
  }

  const item = (key: string, value: number) => (
    <div className="flex items-center justify-between rounded-md border px-3 py-2" key={key}>
      <span className="text-sm capitalize">{key}</span>
      <span className="font-mono font-semibold">{value}/5</span>
    </div>
  );

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-3 gap-2">
        {item("coverage", grade.coverage)}
        {item("correctness", grade.correctness)}
        {item("clarity", grade.clarity)}
      </div>
      <p className="text-sm text-muted-foreground">{grade.comment}</p>
    </div>
  );
}
