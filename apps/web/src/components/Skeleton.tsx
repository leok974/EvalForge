import React from "react";

export const Skeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div className={["animate-pulse rounded-md bg-border/50", className].join(" ")} />
);

export const ScoreboardSkeleton: React.FC = () => (
  <div className="space-y-3">
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
      <Skeleton className="h-10" />
      <Skeleton className="h-10" />
      <Skeleton className="h-10" />
    </div>
    <Skeleton className="h-4 w-2/3" />
  </div>
);
