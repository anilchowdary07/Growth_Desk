"use client";

import React, { useState } from "react";
import {
  Zap,
  Plus,
  Play,
  Pause,
  CheckCircle2,
  ArrowRight,
  Webhook,
  Sliders,
  Layers,
} from "lucide-react";

const initialRules = [
  {
    id: "r1",
    name: "Auto-Capture Purchase Intent to CRM",
    trigger: "Incoming comment or DM contains buying intent (score >= 80)",
    action: "Automatically create qualified lead and notify growth director",
    enabled: true,
  },
  {
    id: "r2",
    name: "Campaign Approval Post Queueing",
    trigger: "Campaign strategy approved by human director",
    action: "Generate and queue all multi-platform content assets in review state",
    enabled: true,
  },
  {
    id: "r3",
    name: "Weekly AI Growth Optimization Audit",
    trigger: "Every Sunday at 23:59 UTC",
    action: "Growth Analyst audits KPIs and synthesizes 3 prioritized strategic experiments",
    enabled: true,
  },
  {
    id: "r4",
    name: "Emergency Escalation on Complaint Detection",
    trigger: "Negative sentiment or customer complaint detected",
    action: "Pause automated replies immediately and route to human support inbox",
    enabled: true,
  },
];

export default function AutomationPage() {
  const [rules, setRules] = useState(initialRules);

  const toggleRule = (id: string) => {
    setRules((prev) =>
      prev.map((r) => (r.id === id ? { ...r, enabled: !r.enabled } : r))
    );
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-600/20 text-amber-400 border border-amber-500/30">
            <Zap className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Event-Driven Automation Rules</h1>
            <p className="text-xs text-slate-400">Autonomous workflow triggers and integrations</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        <div className="mx-auto max-w-4xl space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h2 className="text-sm font-semibold text-white">Active Automation Recipes ({rules.length})</h2>
            <p className="mt-1 text-xs text-slate-400">
              Trigger actions across specialist agents, CRM lead ingestion, and publishing channels.
            </p>

            <div className="mt-5 space-y-3">
              {rules.map((rule) => (
                <div
                  key={rule.id}
                  className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 transition hover:border-slate-700"
                >
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-semibold text-white">{rule.name}</h3>
                    <button
                      onClick={() => toggleRule(rule.id)}
                      className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-[11px] font-semibold transition ${
                        rule.enabled
                          ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                          : "bg-slate-800 text-slate-400"
                      }`}
                    >
                      {rule.enabled ? (
                        <>
                          <CheckCircle2 className="h-3 w-3" />
                          <span>Active</span>
                        </>
                      ) : (
                        <span>Paused</span>
                      )}
                    </button>
                  </div>

                  <div className="mt-3 flex items-center gap-2 text-xs text-slate-300">
                    <span className="font-semibold text-blue-400">WHEN</span>
                    <span className="rounded bg-slate-900 px-2 py-0.5 text-slate-300 border border-slate-800">
                      {rule.trigger}
                    </span>
                    <ArrowRight className="h-3.5 w-3.5 text-slate-500" />
                    <span className="font-semibold text-emerald-400">THEN</span>
                    <span className="rounded bg-slate-900 px-2 py-0.5 text-slate-300 border border-slate-800">
                      {rule.action}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Webhook & External Integrations */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <div className="flex items-center gap-2 text-white">
              <Webhook className="h-4 w-4 text-blue-400" />
              <h2 className="text-sm font-semibold">External Webhook & Middleware Integrations</h2>
            </div>
            <p className="mt-1 text-xs text-slate-400">
              Connect external tools via webhooks, n8n, Zapier, Make, and WhatsApp Business API.
            </p>

            <div className="mt-4 grid grid-cols-3 gap-3">
              {[
                { name: "n8n Workflow Engine", status: "Ready" },
                { name: "Make / Integromat", status: "Ready" },
                { name: "Custom HTTP Webhook", status: "Active" },
              ].map((item, i) => (
                <div key={i} className="rounded-xl border border-slate-800 bg-slate-950/60 p-3.5">
                  <p className="text-xs font-semibold text-white">{item.name}</p>
                  <span className="mt-1 inline-block text-[10px] text-emerald-400 font-medium">
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
