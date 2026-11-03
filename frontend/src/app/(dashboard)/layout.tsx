"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Brain,
  Calendar,
  CheckSquare,
  ChevronDown,
  Inbox,
  Layers,
  LayoutDashboard,
  LogOut,
  Megaphone,
  Palette,
  PenTool,
  Settings,
  Share2,
  Sparkles,
  Users,
  Zap,
  BarChart3,
  Bot,
  KeyRound,
  CreditCard,
} from "lucide-react";
import { api } from "@/lib/api";

const navigation = [
  {
    category: "CORE WORKFORCE",
    items: [
      { name: "Overview", href: "/analytics", icon: LayoutDashboard },
      { name: "AI Marketing Director", href: "/director", icon: Bot, badge: "Orchestrator" },
      { name: "Campaigns", href: "/campaigns", icon: Megaphone },
    ],
  },
  {
    category: "CREATIVE & CONTENT",
    items: [
      { name: "Brand Brain", href: "/brand-brain", icon: Brain, badge: "RAG" },
      { name: "Content Studio", href: "/content", icon: PenTool },
      { name: "Creative Studio", href: "/creative", icon: Palette },
      { name: "Publishing Calendar", href: "/calendar", icon: Calendar },
    ],
  },
  {
    category: "CHANNELS & ENGAGEMENT",
    items: [
      { name: "Social Channels", href: "/social", icon: Share2 },
      { name: "Unified Inbox", href: "/inbox", icon: Inbox },
      { name: "Leads & CRM", href: "/leads", icon: Users },
    ],
  },
  {
    category: "GOVERNANCE & SCALE",
    items: [
      { name: "Approval Center", href: "/approvals", icon: CheckSquare },
      { name: "Automation Rules", href: "/automation", icon: Zap },
    ],
  },
  {
    category: "SETTINGS (BYOK)",
    items: [
      { name: "AI Providers (BYOK)", href: "/settings/ai-providers", icon: KeyRound },
      { name: "Subscription & Limits", href: "/settings/subscription", icon: CreditCard },
      { name: "Team & Workspaces", href: "/settings/team", icon: Layers },
    ],
  },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [currentWs, setCurrentWs] = useState<any>(null);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    async function loadInitialData() {
      try {
        const u = await api.getMe();
        setUser(u);
        const wsList = await api.getWorkspaces();
        setWorkspaces(wsList);
        if (wsList.length > 0) {
          const savedId = api.getWorkspaceId();
          const found = wsList.find((w: any) => w.id === savedId) || wsList[0];
          setCurrentWs(found);
          api.setWorkspace(found.id);
        }
      } catch (err) {
        router.push("/login");
      }
    }
    loadInitialData();
  }, [router]);

  const handleLogout = () => {
    api.setToken(null);
    api.setWorkspace(null);
    router.push("/login");
  };

  const handleSwitchWorkspace = (ws: any) => {
    setCurrentWs(ws);
    api.setWorkspace(ws.id);
    window.location.reload();
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-950 text-slate-100">
      {/* Sidebar */}
      <aside className="flex w-64 flex-col border-r border-slate-800/80 bg-slate-950/90 backdrop-blur-xl">
        {/* Brand Header */}
        <div className="flex h-16 items-center justify-between border-b border-slate-800/80 px-4">
          <Link href="/director" className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 text-white shadow-md shadow-blue-500/20">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center gap-1.5 font-bold tracking-tight text-white">
                GrowthDesk
                <span className="rounded bg-blue-500/20 px-1.5 py-0.5 text-[10px] font-semibold text-blue-400">
                  AI
                </span>
              </div>
              <div className="text-[11px] text-slate-400">Marketing Workforce</div>
            </div>
          </Link>
        </div>

        {/* Workspace Selector */}
        <div className="border-b border-slate-800/80 p-3">
          <div className="group relative">
            <button className="flex w-full items-center justify-between rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-2 text-left text-xs text-slate-300 transition hover:border-slate-700 hover:bg-slate-900">
              <div className="truncate">
                <span className="text-[10px] uppercase tracking-wider text-slate-500">Workspace</span>
                <p className="truncate font-medium text-white">{currentWs?.name || "Main Workspace"}</p>
              </div>
              <ChevronDown className="h-4 w-4 text-slate-400" />
            </button>
            {workspaces.length > 1 && (
              <div className="absolute left-0 top-full z-50 mt-1 hidden w-full rounded-lg border border-slate-800 bg-slate-900 p-1 shadow-xl group-hover:block">
                {workspaces.map((ws) => (
                  <button
                    key={ws.id}
                    onClick={() => handleSwitchWorkspace(ws)}
                    className={`flex w-full items-center px-3 py-2 text-left text-xs rounded-md transition ${
                      ws.id === currentWs?.id
                        ? "bg-blue-600 text-white"
                        : "text-slate-300 hover:bg-slate-800"
                    }`}
                  >
                    {ws.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Navigation items */}
        <div className="flex-1 overflow-y-auto px-3 py-4">
          <div className="space-y-6">
            {navigation.map((section) => (
              <div key={section.category}>
                <div className="px-2 pb-1.5 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                  {section.category}
                </div>
                <div className="space-y-0.5">
                  {section.items.map((item) => {
                    const active = pathname === item.href;
                    return (
                      <Link
                        key={item.name}
                        href={item.href}
                        className={`group flex items-center justify-between rounded-lg px-2.5 py-2 text-xs font-medium transition ${
                          active
                            ? "bg-blue-600/15 text-blue-400 border border-blue-500/20"
                            : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                        }`}
                      >
                        <div className="flex items-center gap-2.5">
                          <item.icon
                            className={`h-4 w-4 ${
                              active ? "text-blue-400" : "text-slate-400 group-hover:text-slate-300"
                            }`}
                          />
                          <span>{item.name}</span>
                        </div>
                        {item.badge && (
                          <span className="rounded bg-slate-800/80 px-1.5 py-0.5 text-[9px] font-semibold text-slate-400">
                            {item.badge}
                          </span>
                        )}
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* User Footer */}
        <div className="border-t border-slate-800/80 p-3">
          <div className="flex items-center justify-between rounded-lg bg-slate-900/40 p-2">
            <div className="flex items-center gap-2.5 truncate">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 text-xs font-semibold text-white">
                {user?.full_name?.charAt(0) || "U"}
              </div>
              <div className="truncate">
                <p className="truncate text-xs font-medium text-white">{user?.full_name || "Account"}</p>
                <p className="truncate text-[10px] text-slate-400">{user?.email || ""}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="rounded p-1.5 text-slate-400 transition hover:bg-slate-800 hover:text-red-400"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex flex-1 flex-col overflow-y-auto bg-slate-900/50">
        {children}
      </main>
    </div>
  );
}
