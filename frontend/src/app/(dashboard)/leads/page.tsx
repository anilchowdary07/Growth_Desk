"use client";

import React, { useState, useEffect } from "react";
import {
  Users,
  Plus,
  Search,
  Star,
  CheckCircle2,
  Mail,
  Phone,
  Building,
  Filter,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

const defaultLeads = [
  {
    id: "l1",
    name: "Marcus Vance",
    email: "marcus@vancecapital.io",
    company: "Vance Capital",
    source: "Instagram",
    status: "qualified",
    score: 92,
    notes: "Inquired about 90-day accelerator. High buying intent, executive scale.",
    created_at: "2026-11-02",
  },
  {
    id: "l2",
    name: "Elena Rostova",
    email: "elena@saasflow.com",
    company: "SaaSFlow",
    source: "LinkedIn",
    status: "new",
    score: 84,
    notes: "Requested tailored workshop for 15-person marketing team.",
    created_at: "2026-11-03",
  },
  {
    id: "l3",
    name: "Alex Thornton",
    email: "alex@thorntonagency.co",
    company: "Thornton Media",
    source: "Website",
    status: "contacted",
    score: 75,
    notes: "Downloaded the 30-Day Inbound Playbook.",
    created_at: "2026-11-01",
  },
];

export default function LeadsCRMPage() {
  const [leads, setLeads] = useState<any[]>(defaultLeads);
  const [loading, setLoading] = useState(false);
  const [isAdding, setIsAdding] = useState(false);

  // Form states
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [company, setCompany] = useState("");
  const [source, setSource] = useState("manual");
  const [score, setScore] = useState(70);
  const [notes, setNotes] = useState("");

  const handleAddLead = async (e: React.FormEvent) => {
    e.preventDefault();
    const newLead = {
      id: Date.now().toString(),
      name,
      email,
      company,
      source,
      score,
      status: "new",
      notes,
      created_at: new Date().toISOString(),
    };
    setLeads([newLead, ...leads]);
    setIsAdding(false);
    setName("");
    setEmail("");
    setCompany("");
    setNotes("");
  };

  return (
    <div className="flex h-full flex-col">
      {/* Page Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-600/20 text-amber-400 border border-amber-500/30">
            <Users className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Leads & CRM</h1>
            <p className="text-xs text-slate-400">Captured prospects, buyer intent scores, and nurturing pipeline</p>
          </div>
        </div>

        <button
          onClick={() => setIsAdding(true)}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-3.5 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500"
        >
          <Plus className="h-4 w-4" />
          Add Lead
        </button>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-4 gap-4 border-b border-slate-800 bg-slate-950/40 p-6">
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <span className="text-[11px] font-semibold uppercase text-slate-400">Total Leads</span>
          <p className="mt-1 text-2xl font-bold text-white">{leads.length}</p>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <span className="text-[11px] font-semibold uppercase text-slate-400">High Intent (80+)</span>
          <p className="mt-1 text-2xl font-bold text-emerald-400">
            {leads.filter((l) => l.score >= 80).length}
          </p>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <span className="text-[11px] font-semibold uppercase text-slate-400">Qualified</span>
          <p className="mt-1 text-2xl font-bold text-blue-400">
            {leads.filter((l) => l.status === "qualified").length}
          </p>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <span className="text-[11px] font-semibold uppercase text-slate-400">Avg Lead Score</span>
          <p className="mt-1 text-2xl font-bold text-amber-400">83 / 100</p>
        </div>
      </div>

      {/* Leads Table */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 shadow-xl overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead className="border-b border-slate-800 bg-slate-950/80 text-slate-400 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Contact</th>
                <th className="py-3 px-4">Source</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Intent Score</th>
                <th className="py-3 px-4">Notes</th>
                <th className="py-3 px-4">Captured</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-slate-800/40 transition">
                  <td className="py-3.5 px-4">
                    <p className="font-semibold text-white">{lead.name}</p>
                    <p className="text-[11px] text-slate-400">{lead.email || lead.company}</p>
                  </td>
                  <td className="py-3.5 px-4 capitalize text-slate-300">{lead.source}</td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`rounded px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${
                        lead.status === "qualified"
                          ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                          : lead.status === "contacted"
                          ? "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                          : "bg-slate-800 text-slate-400"
                      }`}
                    >
                      {lead.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-1.5 font-bold text-amber-400">
                      <Star className="h-3.5 w-3.5 fill-amber-400" />
                      <span>{lead.score}</span>
                    </div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-300 max-w-xs truncate">{lead.notes}</td>
                  <td className="py-3.5 px-4 text-slate-400">{formatDate(lead.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Lead Modal */}
      {isAdding && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <h2 className="text-base font-semibold text-white">Add Qualified Lead</h2>
            <p className="mt-1 text-xs text-slate-400">Enter prospective buyer information into the CRM</p>

            <form onSubmit={handleAddLead} className="mt-5 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300">Full Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Marcus Vance"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Email Address</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="marcus@vancecapital.io"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300">Company</label>
                  <input
                    type="text"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    placeholder="Vance Capital"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300">Intent Score (0-100)</label>
                  <input
                    type="number"
                    min={0}
                    max={100}
                    value={score}
                    onChange={(e) => setScore(parseInt(e.target.value) || 50)}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Qualification Notes</label>
                <textarea
                  rows={2}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Interested in the 90-day accelerator, requested pricing..."
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="mt-6 flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsAdding(false)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-500"
                >
                  Save Lead
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
