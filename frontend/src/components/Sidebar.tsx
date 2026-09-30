"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Skull,
  Calculator,
  AlertTriangle,
  BarChart3,
  UserX,
  Video,
  Home,
  Menu,
  X,
} from "lucide-react";
import { useState } from "react";

const navItems = [
  { href: "/matches", label: "Matches", icon: Home, description: "Live, Recent & Upcoming" },
  { href: "/misery", label: "Misery Dashboard", icon: BarChart3, description: "Stats of despair" },
  { href: "/fraud", label: "Fraud Watch", icon: UserX, description: "Player report cards" },
  { href: "/shame", label: "Shame Gallery", icon: Video, description: "Hall of infamy" },
  { href: "/collapse", label: "Collapse Alerts", icon: AlertTriangle, description: "Meltdown projections" },
];

export function Sidebar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setMobileOpen(!mobileOpen)}
        className="fixed top-4 left-4 z-50 rounded-lg bg-bg-card p-2 lg:hidden border border-border"
        aria-label="Toggle navigation"
      >
        {mobileOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/60 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-40 h-full w-64 bg-bg-secondary border-r border-border flex flex-col transition-transform duration-300
          ${mobileOpen ? "translate-x-0" : "-translate-x-full"} lg:translate-x-0`}
      >
        {/* Logo */}
        <div className="p-6 border-b border-border">
          <Link href="/" className="flex items-center gap-3" onClick={() => setMobileOpen(false)}>
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-pak-green-dim border border-pak-green/30">
              <Skull className="h-6 w-6 text-pak-green" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-text-primary leading-tight">
                🇵🇰 PAK CRICKET
              </h1>
              <p className="text-xs font-semibold text-pak-green">
                HATE WATCH
              </p>
            </div>
          </Link>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = pathname === item.href ||
              (item.href !== "/matches" && pathname.startsWith(item.href));
            const isMatchesHome = item.href === "/matches" && pathname === "/matches";
            const active = isActive || isMatchesHome;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className={`flex items-center gap-3 rounded-lg px-3 py-2.5 transition-all group
                  ${
                    active
                      ? "bg-pak-green-dim text-pak-green border border-pak-green/20"
                      : "text-text-secondary hover:bg-bg-card hover:text-text-primary border border-transparent"
                  }`}
              >
                <Icon
                  size={18}
                  className={active ? "text-pak-green" : "text-text-muted group-hover:text-text-secondary"}
                />
                <div>
                  <div className="text-sm font-medium">{item.label}</div>
                  <div className="text-xs text-text-muted">{item.description}</div>
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-border">
          <div className="rounded-lg bg-pak-dark-dim border border-pak-dark/30 p-3">
            <p className="text-xs text-text-muted italic">
              &ldquo;Pakistan cricket: where hope goes to die and stats go to cry.&rdquo;
            </p>
            <p className="mt-2 text-xs text-pak-green font-mono">
              🏏 Tracking since 1952
            </p>
            <p className="mt-1 text-[9px] text-text-muted/60">
              Created, compiled and designed by <span className="text-pak-green/80">KiZamaDo</span> (and Claude ;)
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}
