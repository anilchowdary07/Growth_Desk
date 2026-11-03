"use client";

import React, { useState, useEffect } from "react";
import {
  Calendar as CalendarIcon,
  ChevronLeft,
  ChevronRight,
  Plus,
  Clock,
  Instagram,
  Linkedin,
  Twitter,
  Youtube,
  Globe,
  CheckCircle2,
} from "lucide-react";
import { api } from "@/lib/api";

const platformIcons: Record<string, any> = {
  instagram: Instagram,
  linkedin: Linkedin,
  twitter: Twitter,
  youtube: Youtube,
};

export default function CalendarPage() {
  const [scheduledPosts, setScheduledPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentMonth, setCurrentMonth] = useState("November 2026");

  // Sample calendar days
  const days = Array.from({ length: 30 }, (_, i) => i + 1);

  useEffect(() => {
    async function loadCalendar() {
      setLoading(true);
      try {
        const posts = await api.getCalendar();
        setScheduledPosts(posts);
      } catch {
        // fallback
      } finally {
        setLoading(false);
      }
    }
    loadCalendar();
  }, []);

  return (
    <div className="flex h-full flex-col">
      {/* Page Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-600/20 text-emerald-400 border border-emerald-500/30">
            <CalendarIcon className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Publishing Calendar</h1>
            <p className="text-xs text-slate-400">Autonomous scheduling engine & multi-channel distribution</p>
          </div>
        </div>

        {/* Month selector */}
        <div className="flex items-center gap-2">
          <div className="flex items-center rounded-lg border border-slate-800 bg-slate-900/60 p-1">
            <button className="rounded p-1 text-slate-400 hover:text-white">
              <ChevronLeft className="h-4 w-4" />
            </button>
            <span className="px-3 text-xs font-semibold text-white">{currentMonth}</span>
            <button className="rounded p-1 text-slate-400 hover:text-white">
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        <div className="rounded-2xl border border-slate-800 bg-slate-950/80 shadow-2xl overflow-hidden">
          {/* Day of week headers */}
          <div className="grid grid-cols-7 border-b border-slate-800 bg-slate-900/90 text-center text-xs font-semibold uppercase tracking-wider text-slate-400 py-3">
            <div>Mon</div>
            <div>Tue</div>
            <div>Wed</div>
            <div>Thu</div>
            <div>Fri</div>
            <div>Sat</div>
            <div>Sun</div>
          </div>

          {/* Calendar cell matrix */}
          <div className="grid grid-cols-7 divide-x divide-y divide-slate-800/80">
            {days.map((day) => {
              // Simulated posts for days 3, 5, 8, 12, 17, 22
              const hasPost = [3, 5, 8, 12, 17, 22].includes(day);
              const postDetails = hasPost
                ? {
                    platform: day % 2 === 0 ? "linkedin" : "instagram",
                    title: day % 2 === 0 ? "B2B Framework: 5 Inbound Hooks" : "Executive Routine Carousel",
                    time: "10:30 AM",
                    status: day < 15 ? "published" : "scheduled",
                  }
                : null;

              const Icon = postDetails?.platform ? platformIcons[postDetails.platform] || Globe : Globe;

              return (
                <div
                  key={day}
                  className="min-h-[110px] p-2.5 transition hover:bg-slate-900/50 flex flex-col justify-between"
                >
                  <div className="flex items-center justify-between">
                    <span
                      className={`text-xs font-semibold ${
                        day === 3 ? "flex h-5 w-5 items-center justify-center rounded-full bg-blue-600 text-white" : "text-slate-400"
                      }`}
                    >
                      {day}
                    </span>
                    {day === 3 && (
                      <span className="text-[10px] font-medium text-blue-400">Today</span>
                    )}
                  </div>

                  {postDetails && (
                    <div
                      className={`mt-2 rounded-lg p-2 text-[10px] border transition ${
                        postDetails.status === "published"
                          ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-300"
                          : "border-blue-500/20 bg-blue-500/10 text-blue-300"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1 font-semibold capitalize">
                          <Icon className="h-3 w-3" />
                          <span>{postDetails.platform}</span>
                        </div>
                        <span className="text-[9px] opacity-80">{postDetails.time}</span>
                      </div>
                      <p className="mt-1 line-clamp-1 font-medium text-white">{postDetails.title}</p>
                    </div>
                  )}

                  <div />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
