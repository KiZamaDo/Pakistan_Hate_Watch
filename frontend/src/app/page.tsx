import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-bg-primary overflow-hidden">
      {/* Background pattern - subtle cricket stumps */}
      <div className="absolute inset-0 opacity-[0.03]" style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%2300a651' stroke-width='1'%3E%3Cpath d='M15 5v50M30 5v50M45 5v50M10 8h40'/%3E%3C/g%3E%3C/svg%3E")`,
        backgroundSize: "60px 60px",
      }} />

      {/* Green glow orb behind text */}
      <div className="absolute w-[500px] h-[500px] bg-pak-green/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 text-center px-6 max-w-2xl">
        {/* Flag + Logo */}
        <div className="mb-8">
          <span className="text-6xl md:text-7xl">🇵🇰</span>
        </div>

        {/* Tagline */}
        <h1 className="text-3xl md:text-5xl font-bold text-text-primary leading-tight mb-4">
          Watching Pakistan lose is your{" "}
          <span className="text-pak-green">guilty pleasure</span>?
        </h1>

        <p className="text-xl md:text-2xl text-text-secondary mb-2">
          Well, you are{" "}
          <span className="text-pak-green font-semibold">not alone</span>.
        </p>

        <p className="text-sm text-text-muted mt-4 mb-10 max-w-md mx-auto">
          Live scores, fraud detection on players, collapse probability calculators,
          and a curated shame gallery - all backed by actual statistics.
        </p>

        {/* CTA Button */}
        <Link
          href="/matches"
          className="inline-flex items-center gap-3 px-8 py-4 rounded-xl bg-pak-green text-white font-bold text-lg hover:bg-pak-green/90 transition-all hover:scale-105 active:scale-95 shadow-lg shadow-pak-green/25"
        >
          🎉 Join the Party
        </Link>

        {/* Stats teaser */}
        <div className="mt-12 flex items-center justify-center gap-6 md:gap-10 text-center">
          <div>
            <div className="text-2xl md:text-3xl font-bold font-mono text-pak-green">14+</div>
            <div className="text-[10px] md:text-xs text-text-muted">Recent Defeats<br />Tracked</div>
          </div>
          <div className="h-8 w-px bg-border" />
          <div>
            <div className="text-2xl md:text-3xl font-bold font-mono text-pak-green">12</div>
            <div className="text-[10px] md:text-xs text-text-muted">Players on<br />Fraud Watch</div>
          </div>
          <div className="h-8 w-px bg-border" />
          <div>
            <div className="text-2xl md:text-3xl font-bold font-mono text-pak-green">11</div>
            <div className="text-[10px] md:text-xs text-text-muted">Shame Gallery<br />Videos</div>
          </div>
          <div className="h-8 w-px bg-border" />
          <div>
            <div className="text-2xl md:text-3xl font-bold font-mono text-accent-red">4</div>
            <div className="text-[10px] md:text-xs text-text-muted">Certified<br />Frauds</div>
          </div>
        </div>
      </div>

      {/* Dedication */}
      <div className="absolute bottom-16 text-center px-6">
        <p className="text-xs text-text-secondary italic">
          To <span className="text-pak-green">Wasay bhai</span>, <span className="text-pak-green">Iffi bhai</span> and <span className="text-pak-green">Neem ka Ped</span> - I owe you one 🤝
        </p>
      </div>

      {/* Bottom text */}
      <div className="absolute bottom-4 text-center text-[10px] text-text-muted">
        <p>🏏 Tracking disappointment since 1952</p>
        <p className="mt-1 opacity-60">Created, compiled and designed by <span className="text-pak-green">KiZamaDo</span> (and Claude ;)</p>
      </div>
    </div>
  );
}
