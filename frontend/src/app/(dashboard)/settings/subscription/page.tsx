"use client";

import React, { useState, useEffect } from "react";
import {
  CreditCard,
  CheckCircle2,
  Sparkles,
  Zap,
  Shield,
  Layers,
} from "lucide-react";
import { api } from "@/lib/api";

const availablePlans = [
  {
    id: "starter",
    name: "Starter Workforce",
    price: "$49",
    period: "per month",
    description: "Ideal for single brands, independent creators, and early-stage ventures.",
    features: [
      "1 Business Workspace",
      "AI Marketing Director Coordinator",
      "Brand Brain Knowledge System",
      "Content Studio (Social, Blog, Scripts)",
      "Multi-Channel Publishing Calendar",
      "Unified Social Inbox",
      "Bring Your Own Key (BYOK)",
    ],
    limits: { workspaces: 1, campaigns: 3, posts: 60 },
  },
  {
    id: "professional",
    name: "Growth Department",
    price: "$149",
    period: "per month",
    popular: true,
    description: "For fast-scaling companies requiring full autonomous agent coordination.",
    features: [
      "3 Workspaces",
      "Full Suite of 10 Specialist Agents",
      "Autonomous Campaign Planning & Tasks",
      "Lead Generation & CRM Scoring",
      "Market Research & Competitor Tracking",
      "Analytics & ROAS Diagnosis",
      "Priority Background Execution",
    ],
    limits: { workspaces: 3, campaigns: 20, posts: 300 },
  },
  {
    id: "agency",
    name: "Agency Command Center",
    price: "$399",
    period: "per month",
    description: "Multi-client management with dedicated Brand Brains and approval workflows.",
    features: [
      "25 Isolated Client Workspaces",
      "All 10 Specialized Agents per Client",
      "Client Approval Portal (White-label Ready)",
      "Team Member Permissions & Roles",
      "Event-Driven Automation Triggers",
      "Weekly Client Performance Reports",
      "Razorpay Multi-Tenant Billing",
    ],
    limits: { workspaces: 25, campaigns: 100, posts: 2000 },
  },
];

export default function SubscriptionSettingsPage() {
  const [currentPlan, setCurrentPlan] = useState("starter");
  const [upgrading, setUpgrading] = useState(false);

  const handleUpgrade = async (planId: string) => {
    if (planId === currentPlan) return;
    setUpgrading(true);
    try {
      await api.upgradePlan(planId);
      setCurrentPlan(planId);
      alert(`Upgraded to ${planId.toUpperCase()} plan successfully! Razorpay recurring billing active.`);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setUpgrading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30">
            <CreditCard className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Subscription & SaaS Licensing</h1>
            <p className="text-xs text-slate-400">Commercial tiers, entitlement enforcement, and Razorpay billing</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        <div className="mx-auto max-w-5xl space-y-8">
          {/* Active Status Banner */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl flex items-center justify-between">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                Current Active Subscription
              </span>
              <div className="mt-1 flex items-center gap-2">
                <h2 className="text-xl font-bold text-white capitalize">{currentPlan} Plan</h2>
                <span className="rounded-md bg-emerald-500/20 px-2 py-0.5 text-xs font-semibold text-emerald-400 border border-emerald-500/30">
                  Active Licence
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-400">
                BYOK Mode: You pay model providers directly for LLM tokens. SaaS licence covers platform infrastructure and autonomous multi-agent coordination.
              </p>
            </div>
          </div>

          {/* Plan Comparison Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {availablePlans.map((plan) => {
              const isCurrent = plan.id === currentPlan;

              return (
                <div
                  key={plan.id}
                  className={`flex flex-col justify-between rounded-2xl border p-6 shadow-xl transition relative ${
                    plan.popular
                      ? "border-blue-500 bg-gradient-to-b from-blue-950/30 to-slate-900/90 shadow-blue-500/10"
                      : "border-slate-800 bg-slate-900/80"
                  }`}
                >
                  {plan.popular && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-blue-600 px-3 py-0.5 text-[10px] font-bold uppercase tracking-wider text-white shadow-md">
                      Most Popular
                    </div>
                  )}

                  <div>
                    <h3 className="text-base font-bold text-white">{plan.name}</h3>
                    <p className="mt-1 text-xs text-slate-400 min-h-[32px]">{plan.description}</p>

                    <div className="mt-4 flex items-baseline gap-1">
                      <span className="text-3xl font-extrabold text-white">{plan.price}</span>
                      <span className="text-xs text-slate-400">{plan.period}</span>
                    </div>

                    <div className="mt-6 space-y-2.5 border-t border-slate-800 pt-5">
                      {plan.features.map((feat, i) => (
                        <div key={i} className="flex items-center gap-2 text-xs text-slate-300">
                          <CheckCircle2 className="h-4 w-4 shrink-0 text-blue-400" />
                          <span>{feat}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mt-8 border-t border-slate-800 pt-5">
                    <button
                      onClick={() => handleUpgrade(plan.id)}
                      disabled={isCurrent || upgrading}
                      className={`w-full rounded-xl py-2.5 text-xs font-semibold transition ${
                        isCurrent
                          ? "border border-slate-700 bg-slate-800/80 text-slate-400 cursor-default"
                          : plan.popular
                          ? "bg-blue-600 text-white hover:bg-blue-500 shadow-lg shadow-blue-500/20"
                          : "border border-slate-700 bg-slate-800 text-white hover:bg-slate-700"
                      }`}
                    >
                      {isCurrent ? "Current Plan" : `Upgrade to ${plan.name}`}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
