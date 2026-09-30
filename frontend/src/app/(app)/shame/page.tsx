"use client";

import { useEffect, useState } from "react";
import { getShameVideos } from "@/lib/api";
import {
  Video,
  AlertTriangle,
  Calendar,
  Eye,
  Tag,
  Filter,
  Trophy,
} from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

const categoryLabels: Record<string, { label: string; emoji: string }> = {
  collapse: { label: "Collapse", emoji: "💀" },
  choke: { label: "Choke", emoji: "😰" },
  "upset-loss": { label: "Upset Loss", emoji: "😱" },
  "bowling-disaster": { label: "Bowling Disaster", emoji: "🎳" },
  "fielding-horror": { label: "Fielding Horror", emoji: "🧈" },
  "captaincy-blunder": { label: "Captaincy Blunder", emoji: "🤦" },
  "tournament-exit": { label: "Tournament Exit", emoji: "🚪" },
  "all-time-low": { label: "All-Time Low", emoji: "📉" },
};

export default function ShamePage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [playingId, setPlayingId] = useState<string | null>(null);

  useEffect(() => {
    getShameVideos()
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-6xl">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="rounded-xl bg-bg-card border border-border aspect-video animate-pulse" />
        ))}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="rounded-xl bg-bg-card border border-border p-12 text-center max-w-6xl">
        <AlertTriangle className="h-8 w-8 text-accent-orange mx-auto mb-3" />
        <p className="text-sm text-text-muted">
          Backend not running. Start it with: cd backend && uvicorn app.main:app --reload
        </p>
      </div>
    );
  }

  const videos = data.videos || [];
  const categories = data.categories || [];
  const hallOfShame = data.hall_of_shame_top3 || [];

  const filteredVideos = selectedCategory
    ? videos.filter((v: any) => v.category === selectedCategory)
    : videos;

  return (
    <div className="max-w-6xl space-y-6">
      {/* Hall of Shame Top 3 */}
      <section>
        <h2 className="text-base font-bold mb-4 flex items-center gap-2">
          <Trophy className="h-5 w-5 text-accent-yellow" />
          Hall of Shame - Top 3
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {hallOfShame.map((v: any, i: number) => (
            <div
              key={v.id}
              className={`rounded-xl border p-4 ${
                i === 0
                  ? "bg-accent-red/20 border-accent-red/30"
                  : "bg-bg-card border-border"
              }`}
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl font-bold font-mono text-accent-red">
                  #{i + 1}
                </span>
                <span className="text-lg">{v.opponent_flag}</span>
              </div>
              <h3 className="text-sm font-bold text-text-primary line-clamp-2">
                {v.title}
              </h3>
              <div className="flex items-center gap-2 mt-2 text-xs text-text-muted">
                <span>Shame: {v.shame_rating}/10</span>
                <span>•</span>
                <span>{v.date}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setSelectedCategory("")}
          className={`text-xs px-3 py-1.5 rounded-full transition-all ${
            !selectedCategory
              ? "bg-pak-green-dim text-pak-green border-pak-green/30"
              : "bg-bg-card text-text-muted hover:text-text-secondary border border-border"
          }`}
        >
          All ({videos.length})
        </button>
        {categories.map((cat: string) => {
          const catInfo = categoryLabels[cat] || { label: cat, emoji: "🏏" };
          const count = videos.filter((v: any) => v.category === cat).length;
          return (
            <button
              key={cat}
              onClick={() =>
                setSelectedCategory(selectedCategory === cat ? "" : cat)
              }
              className={`text-xs px-3 py-1.5 rounded-full transition-all ${
                selectedCategory === cat
                  ? "bg-pak-green-dim text-pak-green border-pak-green/30"
                  : "bg-bg-card text-text-muted hover:text-text-secondary border border-border"
              }`}
            >
              {catInfo.emoji} {catInfo.label} ({count})
            </button>
          );
        })}
      </div>

      {/* Video Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredVideos.map((video: any) => (
          <VideoCard
            key={video.id}
            video={video}
            isPlaying={playingId === video.id}
            onPlay={() => setPlayingId(playingId === video.id ? null : video.id)}
          />
        ))}
      </div>
    </div>
  );
}

function VideoCard({
  video,
  isPlaying,
  onPlay,
}: {
  video: any;
  isPlaying: boolean;
  onPlay: () => void;
}) {
  const catInfo = categoryLabels[video.category] || {
    label: video.category,
    emoji: "🏏",
  };

  return (
    <div className="rounded-xl bg-bg-card border border-border overflow-hidden group">
      {/* Thumbnail / Player */}
      <div className="relative aspect-video bg-bg-secondary">
        {isPlaying ? (
          <iframe
            src={`https://www.youtube.com/embed/${video.youtube_id}?autoplay=1`}
            className="absolute inset-0 w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            title={video.title}
          />
        ) : (
          <button
            onClick={onPlay}
            className="absolute inset-0 w-full h-full flex items-center justify-center"
          >
            <img
              src={`https://img.youtube.com/vi/${video.youtube_id}/hqdefault.jpg`}
              alt={video.title}
              className="absolute inset-0 w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-black/40 group-hover:bg-black/20 transition-all" />
            <div className="relative z-10 h-14 w-14 rounded-full bg-accent-red/90 flex items-center justify-center group-hover:scale-110 transition-transform">
              <Video className="h-6 w-6 text-white ml-1" />
            </div>
            {/* Shame Rating Badge */}
            <div className="absolute top-3 right-3 z-10 bg-black/70 rounded-full px-2 py-1 text-xs font-bold text-accent-red">
              SHAME {video.shame_rating}/10
            </div>
          </button>
        )}
      </div>

      {/* Info */}
      <div className="p-4">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-lg">{video.opponent_flag}</span>
          <span
            className="text-xs bg-accent-red/20 text-accent-red px-2 py-0.5 rounded-full"
          >
            {catInfo.emoji} {catInfo.label}
          </span>
          <span className="text-xs bg-bg-secondary text-text-muted px-2 py-0.5 rounded-full">
            {video.format}
          </span>
        </div>
        <h3 className="text-sm font-bold text-text-primary mb-1 line-clamp-2">
          {video.title}
        </h3>
        <p className="text-xs text-text-secondary mb-3 line-clamp-2">
          {video.description}
        </p>
        <div className="flex flex-wrap items-center gap-3 text-xs text-text-muted">
          <span className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            {video.date}
          </span>
          <span className="flex items-center gap-1">
            <Eye className="h-3 w-3" />
            {video.view_count}
          </span>
        </div>
        {video.tags && (
          <div className="flex flex-wrap gap-1 mt-2">
            {video.tags.slice(0, 4).map((tag: string) => (
              <span
                key={tag}
                className="text-[10px] bg-bg-secondary text-text-muted px-1.5 py-0.5 rounded"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
