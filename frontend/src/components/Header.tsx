"use client";

import { usePathname } from "next/navigation";

const pageTitles: Record<string, { title: string; subtitle: string }> = {
  "/matches": { title: "Pakistan Matches", subtitle: "Live scores, recent results & upcoming fixtures" },
  "/misery": { title: "Misery Dashboard", subtitle: "The numbers that tell the whole painful story" },
  "/fraud": { title: "Fraud Watch", subtitle: "Player performance fraud detection — who is actually delivering?" },
  "/shame": { title: "Shame Gallery", subtitle: "YouTube hall of fame for Pakistan cricket's memorable defeats" },
  "/collapse": { title: "Collapse Alerts", subtitle: "Detecting and projecting Pakistan batting collapses" },
};

export function Header() {
  const pathname = usePathname();

  // Match detail pages
  const isMatchDetail = pathname.startsWith("/match/");
  const page = isMatchDetail
    ? { title: "Match Scorecard", subtitle: "Live scorecard, commentary & hate watch analysis" }
    : pageTitles[pathname] || pageTitles["/matches"];

  return (
    <header className="sticky top-0 z-20 bg-bg-primary/80 backdrop-blur-md border-b border-border">
      <div className="flex items-center justify-between px-4 md:px-6 lg:px-8 py-4">
        <div className="ml-12 lg:ml-0">
          <h1 className="text-lg md:text-xl font-bold text-text-primary flex items-center gap-2">
            {page.title}
          </h1>
          <p className="text-sm text-text-muted mt-0.5">{page.subtitle}</p>
        </div>
        <div className="hidden md:flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-full bg-pak-green-dim border border-pak-green/20 px-3 py-1.5">
            <span className="h-2 w-2 rounded-full bg-pak-green animate-live" />
            <span className="text-xs font-medium text-pak-green">HATE WATCH ACTIVE</span>
          </div>
        </div>
      </div>
    </header>
  );
}
