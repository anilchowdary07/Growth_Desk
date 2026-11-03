"use client";

import React, { useState, useEffect } from "react";
import {
  Megaphone,
  Plus,
  Sparkles,
  Target,
  Calendar,
  DollarSign,
  TrendingUp,
  CheckCircle2,
  Clock,
  ArrowRight,
  Filter,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCampaign, setSelectedCampaign] = useState<any | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [planningId, setPlanningId] = useState<string | null>(null);

  // Form states
  const [title, setTitle] = useState("");
  const [objective, setObjective] = useState("");
  const [audience, setAudience] = useState("");
  const [budget, setBudget] = useState("1000");

  const loadCampaigns = async () => {
    setLoading(true);
    try {
      const data = await api.getCampaigns();
      setCampaigns(data);
      if (data.length > 0 && !selectedCampaign) {
        setSelectedCampaign(data[0]);
      }
    } catch {
      // fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCampaigns();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const newCamp = await api.createCampaign({
        title,
        objective,
        target_audience: audience,
        budget: parseFloat(budget) || 1000,
      });
      setTitle("");
      setObjective("");
      setAudience("");
      setIsCreating(false);
      await loadCampaigns();
      setSelectedCampaign(newCamp);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleGeneratePlan = async (campId: string) => {
    setPlanningId(campId);
    try {
      const updated = await api.planCampaign(campId);
      setSelectedCampaign(updated);
      await loadCampaigns();
    } catch (err: any) {
      alert(`AI Planning error: ${err.message}. Please ensure an AI Provider key is configured under Settings.`);
    } finally {
      setPlanningId(null);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Page Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30">
            <Megaphone className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Campaign Management</h1>
            <p className="text-xs text-slate-400">Autonomous multi-channel marketing campaigns</p>
          </div>
        </div>

        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-3.5 py-2 text-xs font-medium text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500"
        >
          <Plus className="h-4 w-4" />
          New Campaign
        </button>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Campaigns List (Left) */}
        <div className="w-80 shrink-0 border-r border-slate-800 bg-slate-950/40 p-4 overflow-y-auto space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 px-1">
            Active Campaigns ({campaigns.length})
          </div>

          {loading ? (
            <div className="p-8 text-center text-xs text-slate-400">Loading campaigns...</div>
          ) : campaigns.length === 0 ? (
            <div className="rounded-xl border border-dashed border-slate-800 p-6 text-center">
              <Megaphone className="mx-auto h-8 w-8 text-slate-600" />
              <p className="mt-2 text-xs font-medium text-slate-300">No campaigns yet</p>
              <p className="mt-1 text-[11px] text-slate-400">
                Create a campaign to let the AI workforce plan and execute.
              </p>
            </div>
          ) : (
            campaigns.map((camp) => {
              const isSelected = selectedCampaign?.id === camp.id;
              return (
                <div
                  key={camp.id}
                  onClick={() => setSelectedCampaign(camp)}
                  className={`cursor-pointer rounded-xl border p-3.5 transition ${
                    isSelected
                      ? "border-blue-500/50 bg-blue-600/10 shadow-lg shadow-blue-600/10"
                      : "border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-slate-300">
                      {camp.status}
                    </span>
                    <span className="text-[11px] text-slate-400">{formatDate(camp.created_at)}</span>
                  </div>
                  <h3 className="mt-2 text-xs font-semibold text-white line-clamp-1">{camp.title}</h3>
                  <p className="mt-1 text-[11px] text-slate-400 line-clamp-2">{camp.objective}</p>

                  <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-800/60 pt-2">
                    <span>{camp.tasks?.length || 0} tasks</span>
                    <span>Budget: ${camp.budget || 0}</span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Campaign Detail (Right) */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
          {selectedCampaign ? (
            <div className="max-w-4xl space-y-6">
              {/* Campaign Header Card */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="rounded-md bg-blue-500/20 px-2.5 py-0.5 text-xs font-semibold text-blue-400 border border-blue-500/30">
                        {selectedCampaign.status.toUpperCase()}
                      </span>
                      <span className="text-xs text-slate-400">
                        Created {formatDate(selectedCampaign.created_at)}
                      </span>
                    </div>
                    <h2 className="mt-2 text-xl font-bold text-white">{selectedCampaign.title}</h2>
                  </div>

                  {!selectedCampaign.strategy && (
                    <button
                      onClick={() => handleGeneratePlan(selectedCampaign.id)}
                      disabled={planningId === selectedCampaign.id}
                      className="flex items-center gap-2 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-lg shadow-blue-500/20 transition hover:from-blue-500 hover:to-indigo-500 disabled:opacity-50"
                    >
                      <Sparkles className="h-4 w-4" />
                      {planningId === selectedCampaign.id ? "Synthesizing Plan..." : "Generate AI Strategy"}
                    </button>
                  )}
                </div>

                <div className="mt-6 rounded-xl border border-slate-800/80 bg-slate-950/60 p-4">
                  <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Primary Objective
                  </div>
                  <p className="mt-1 text-sm text-slate-200">{selectedCampaign.objective}</p>
                </div>

                <div className="mt-4 grid grid-cols-3 gap-4">
                  <div className="rounded-lg border border-slate-800 bg-slate-950/40 p-3">
                    <span className="text-[11px] text-slate-400">Target Audience</span>
                    <p className="mt-0.5 text-xs font-medium text-white truncate">
                      {selectedCampaign.target_audience || "Broad Consumer/B2B"}
                    </p>
                  </div>
                  <div className="rounded-lg border border-slate-800 bg-slate-950/40 p-3">
                    <span className="text-[11px] text-slate-400">Allocated Budget</span>
                    <p className="mt-0.5 text-xs font-medium text-white">
                      ${selectedCampaign.budget || 0}
                    </p>
                  </div>
                  <div className="rounded-lg border border-slate-800 bg-slate-950/40 p-3">
                    <span className="text-[11px] text-slate-400">Target Leads / KPIs</span>
                    <p className="mt-0.5 text-xs font-medium text-emerald-400">
                      {selectedCampaign.kpi_targets?.leads || 50} Qualified Leads
                    </p>
                  </div>
                </div>
              </div>

              {/* AI Strategy Breakdown */}
              {selectedCampaign.strategy && (
                <div className="rounded-2xl border border-blue-500/20 bg-slate-900/90 p-6 shadow-xl">
                  <div className="flex items-center gap-2 text-sm font-semibold text-blue-400">
                    <Sparkles className="h-4 w-4" />
                    AI Marketing Director Strategic Architecture
                  </div>
                  <div className="mt-4 text-xs leading-relaxed text-slate-300 whitespace-pre-wrap border-t border-slate-800 pt-4">
                    {selectedCampaign.strategy.summary}
                  </div>
                </div>
              )}

              {/* Execution Pipeline Tasks */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold text-white">Specialist Execution Pipeline</h3>
                  <span className="text-xs text-slate-400">
                    {selectedCampaign.tasks?.length || 0} Delegated Tasks
                  </span>
                </div>

                <div className="mt-4 space-y-2.5">
                  {selectedCampaign.tasks?.length === 0 ? (
                    <p className="text-xs text-slate-400 py-4 text-center">
                      Click &ldquo;Generate AI Strategy&rdquo; to automatically delegate tasks to specialist agents.
                    </p>
                  ) : (
                    selectedCampaign.tasks?.map((task: any) => (
                      <div
                        key={task.id}
                        className="flex items-center justify-between rounded-xl border border-slate-800/80 bg-slate-950/50 p-3.5"
                      >
                        <div className="flex items-center gap-3">
                          <CheckCircle2
                            className={`h-4 w-4 ${
                              task.status === "completed" ? "text-emerald-400" : "text-slate-600"
                            }`}
                          />
                          <div>
                            <p className="text-xs font-medium text-white">{task.title}</p>
                            <p className="text-[10px] text-slate-400">
                              Assigned to: <span className="text-blue-400">{task.assigned_agent}</span>
                            </p>
                          </div>
                        </div>

                        <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold uppercase text-slate-400">
                          {task.status}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="flex h-full items-center justify-center text-xs text-slate-400">
              Select or create a campaign to view the marketing roadmap
            </div>
          )}
        </div>
      </div>

      {/* New Campaign Modal */}
      {isCreating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <h2 className="text-lg font-semibold text-white">Launch New Campaign Objective</h2>
            <p className="mt-1 text-xs text-slate-400">
              Describe your goal. The AI Marketing Director will design the complete strategy and tasks.
            </p>

            <form onSubmit={handleCreate} className="mt-5 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300">Campaign Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Q4 Fitness Coaching Lead Engine"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">
                  Marketing Objective (Natural Language)
                </label>
                <textarea
                  rows={3}
                  required
                  value={objective}
                  onChange={(e) => setObjective(e.target.value)}
                  placeholder="Promote my new fitness coaching programme and generate 100 qualified leads over the next 30 days."
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300">Target Audience</label>
                  <input
                    type="text"
                    value={audience}
                    onChange={(e) => setAudience(e.target.value)}
                    placeholder="Busy executives, ages 30-50"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300">Budget ($)</label>
                  <input
                    type="number"
                    value={budget}
                    onChange={(e) => setBudget(e.target.value)}
                    placeholder="1000"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="mt-6 flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsCreating(false)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-xs font-medium text-slate-300 transition hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500"
                >
                  Create & Delegate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

