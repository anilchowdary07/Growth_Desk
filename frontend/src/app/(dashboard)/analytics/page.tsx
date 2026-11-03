"use client";

import React, { useState, useEffect } from "react";
import {
  BarChart3,
  TrendingUp,
  Users,
  Eye,
  FileCheck,
  Sparkles,
  ArrowUpRight,
  Lightbulb,
} from "lucide-react";
import { api } from "@/lib/api";

export default function AnalyticsDashboardPage() {
  const [analytics, setAnalytics] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const data = await api.getAnalytics();
        setAnalytics(data);
      } catch {
        // fallback
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30">
            <BarChart3 className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Marketing Analytics & Growth Loop</h1>
            <p className="text-xs text-slate-400">Autonomous campaign analysis, audience reach, and AI recommendations</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-1.5 text-xs font-medium text-slate-300">
            Last 30 Days
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30 space-y-6">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-semibold uppercase tracking-wider">Total Reach</span>
              <Eye className="h-4 w-4 text-blue-400" />
            </div>
            <p className="mt-2 text-2xl font-bold text-white">
              {analytics?.total_reach?.value || "24.8K"}
            </p>
            <div className="mt-2 flex items-center gap-1 text-[11px] text-emerald-400">
              <ArrowUpRight className="h-3 w-3" />
              <span>+14.2% from last cycle</span>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-semibold uppercase tracking-wider">Engagement Rate</span>
              <TrendingUp className="h-4 w-4 text-purple-400" />
            </div>
            <p className="mt-2 text-2xl font-bold text-white">
              {analytics?.engagement_rate?.value || "4.6%"}
            </p>
            <div className="mt-2 flex items-center gap-1 text-[11px] text-emerald-400">
              <ArrowUpRight className="h-3 w-3" />
              <span>+0.8% organic lift</span>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-semibold uppercase tracking-wider">Qualified Leads</span>
              <Users className="h-4 w-4 text-emerald-400" />
            </div>
            <p className="mt-2 text-2xl font-bold text-emerald-400">
              {analytics?.new_leads?.value || 35}
            </p>
            <div className="mt-2 flex items-center gap-1 text-[11px] text-emerald-400">
              <ArrowUpRight className="h-3 w-3" />
              <span>+25.0% conversion rate</span>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-semibold uppercase tracking-wider">Assets Produced</span>
              <FileCheck className="h-4 w-4 text-amber-400" />
            </div>
            <p className="mt-2 text-2xl font-bold text-white">
              {analytics?.content_published?.value || 18}
            </p>
            <div className="mt-2 flex items-center gap-1 text-[11px] text-slate-400">
              <span>Across 5 active channels</span>
            </div>
          </div>
        </div>

        {/* AI Recommendations Panel */}
        <div className="rounded-2xl border border-indigo-500/20 bg-gradient-to-br from-slate-900/90 to-indigo-950/40 p-6 shadow-xl">
          <div className="flex items-center gap-2 text-indigo-400">
            <Sparkles className="h-5 w-5" />
            <h2 className="text-sm font-semibold">Growth Analyst Optimization Recommendations</h2>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Synthesized from historical campaign performance and platform response rates.
          </p>

          <div className="mt-4 space-y-2.5">
            {(
              analytics?.growth_recommendations || [
                "Publishing LinkedIn authority carousels on Tuesday and Thursday mornings yields 3x higher comment engagement.",
                "Short-form video scripts focusing on customer objection-handling generate the highest qualified lead conversion.",
                "Review Brand Brain prohibited claims to ensure recent promotional angles remain 100% compliant.",
              ]
            ).map((rec: string, i: number) => (
              <div
                key={i}
                className="flex items-start gap-2.5 rounded-xl border border-slate-800/80 bg-slate-950/50 p-3 text-xs text-slate-300"
              >
                <Lightbulb className="h-4 w-4 shrink-0 text-amber-400 mt-0.5" />
                <span>{rec}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Leads By Channel & Engagement Trends */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Qualified Leads by Channel Source
            </h3>
            <div className="mt-4 space-y-3">
              {(
                analytics?.leads_by_source || [
                  { source: "Instagram", count: 18 },
                  { source: "LinkedIn", count: 12 },
                  { source: "Website", count: 5 },
                ]
              ).map((src: any) => (
                <div key={src.source}>
                  <div className="flex justify-between text-xs font-medium text-slate-300 mb-1">
                    <span>{src.source}</span>
                    <span>{src.count} leads</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                    <div
                      className="h-full bg-blue-500 rounded-full"
                      style={{ width: `${Math.min(src.count * 5, 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Weekly Engagement Volume
            </h3>
            <div className="mt-4 flex items-end justify-between gap-2 h-36 pt-4">
              {[320, 450, 390, 610, 580, 740, 690].map((val, idx) => {
                const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
                const heightPct = Math.round((val / 750) * 100);
                return (
                  <div key={idx} className="flex flex-1 flex-col items-center gap-1.5 h-full justify-end">
                    <div
                      className="w-full rounded-t-lg bg-blue-600/70 hover:bg-blue-500 transition"
                      style={{ height: `${heightPct}%` }}
                    />
                    <span className="text-[10px] text-slate-400">{days[idx]}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

