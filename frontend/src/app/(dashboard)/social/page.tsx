"use client";

import React, { useState, useEffect } from "react";
import {
  Share2,
  CheckCircle2,
  Plus,
  AlertCircle,
  ExternalLink,
  Trash2,
  Instagram,
  Linkedin,
  Twitter,
  Youtube,
  Facebook,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

const platformList = [
  {
    id: "instagram",
    name: "Instagram",
    desc: "Feed posts, carousels, reels, and comment automations",
    icon: Instagram,
    color: "from-pink-500 to-rose-600",
  },
  {
    id: "linkedin",
    name: "LinkedIn",
    desc: "Company pages, personal profiles, articles, and thought leadership",
    icon: Linkedin,
    color: "from-blue-600 to-cyan-600",
  },
  {
    id: "twitter",
    name: "X (Twitter)",
    desc: "Viral threads, high-engagement tweets, and audience replies",
    icon: Twitter,
    color: "from-slate-700 to-slate-900",
  },
  {
    id: "youtube",
    name: "YouTube",
    desc: "Video titles, descriptions, community posts, and Shorts workflows",
    icon: Youtube,
    color: "from-red-600 to-rose-700",
  },
  {
    id: "facebook",
    name: "Facebook",
    desc: "Pages, groups, video distribution, and Messenger interactions",
    icon: Facebook,
    color: "from-blue-600 to-indigo-700",
  },
];

export default function SocialAccountsPage() {
  const [accounts, setAccounts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [connectModal, setConnectModal] = useState<any | null>(null);
  const [tokenInput, setTokenInput] = useState("");
  const [usernameInput, setUsernameInput] = useState("");
  const [connecting, setConnecting] = useState(false);

  const loadAccounts = async () => {
    setLoading(true);
    try {
      const data = await api.getSocialAccounts();
      setAccounts(data);
    } catch {
      // fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  const handleConnect = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!connectModal) return;
    setConnecting(true);

    try {
      await api.connectSocialAccount({
        platform: connectModal.id,
        access_token: tokenInput || "mock-oauth-token-dev-mode",
        username: usernameInput || `@brand_${connectModal.id}`,
      });
      setConnectModal(null);
      setTokenInput("");
      setUsernameInput("");
      await loadAccounts();
    } catch (err: any) {
      alert(err.message);
    } finally {
      setConnecting(false);
    }
  };

  const handleDisconnect = async (id: string) => {
    if (!confirm("Are you sure you want to disconnect this social channel?")) return;
    try {
      await api.request(`/social/accounts/${id}`, { method: "DELETE" });
      await loadAccounts();
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Page Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-600/20 text-cyan-400 border border-cyan-500/30">
            <Share2 className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Social Channels</h1>
            <p className="text-xs text-slate-400">Connect and manage authorized publishing destinations</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/40">
        <div className="mx-auto max-w-4xl space-y-6">
          {/* Connected Accounts */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h2 className="text-sm font-semibold text-white">Connected Channels ({accounts.length})</h2>
            <p className="mt-1 text-xs text-slate-400">
              Active accounts configured for automated posting and unified inbox monitoring.
            </p>

            <div className="mt-4 space-y-3">
              {accounts.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-800 p-6 text-center bg-slate-950/40">
                  <AlertCircle className="mx-auto h-6 w-6 text-slate-600" />
                  <p className="mt-2 text-xs font-medium text-slate-300">No channels connected yet</p>
                  <p className="mt-1 text-[11px] text-slate-400">
                    Connect your brand accounts below to enable one-click publishing and comment tracking.
                  </p>
                </div>
              ) : (
                accounts.map((acc) => (
                  <div
                    key={acc.id}
                    className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 p-4"
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-800 text-white font-bold uppercase">
                        {acc.platform.charAt(0)}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="text-xs font-semibold text-white">{acc.display_name}</p>
                          <span className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium">
                            <CheckCircle2 className="h-3 w-3" />
                            Connected
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-400">
                          {acc.username} &bull; Synced {formatDate(acc.last_synced_at)}
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={() => handleDisconnect(acc.id)}
                      className="text-slate-500 transition hover:text-rose-400 p-2"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Available Channels */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h2 className="text-sm font-semibold text-white">Available Channels</h2>
            <p className="mt-1 text-xs text-slate-400">
              Select a channel to configure OAuth credentials or developer access tokens.
            </p>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              {platformList.map((platform) => {
                const isConnected = accounts.some((a) => a.platform === platform.id);
                const Icon = platform.icon;

                return (
                  <div
                    key={platform.id}
                    className="flex flex-col justify-between rounded-xl border border-slate-800 bg-slate-950/60 p-4 transition hover:border-slate-700"
                  >
                    <div>
                      <div className="flex items-center justify-between">
                        <div
                          className={`flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-tr ${platform.color} text-white shadow-md`}
                        >
                          <Icon className="h-4 w-4" />
                        </div>
                        {isConnected && (
                          <span className="rounded bg-emerald-500/20 px-2 py-0.5 text-[10px] font-semibold text-emerald-400 border border-emerald-500/30">
                            Active
                          </span>
                        )}
                      </div>
                      <h3 className="mt-3 text-xs font-semibold text-white">{platform.name}</h3>
                      <p className="mt-1 text-[11px] text-slate-400">{platform.desc}</p>
                    </div>

                    <div className="mt-4 border-t border-slate-800/80 pt-3">
                      <button
                        onClick={() => setConnectModal(platform)}
                        className={`w-full rounded-lg py-2 text-xs font-semibold transition ${
                          isConnected
                            ? "border border-slate-700 bg-slate-900 text-slate-300 hover:bg-slate-800"
                            : "bg-blue-600 text-white shadow-md shadow-blue-500/20 hover:bg-blue-500"
                        }`}
                      >
                        {isConnected ? "Update Connection" : `Connect ${platform.name}`}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Connection Modal */}
      {connectModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <h2 className="text-base font-semibold text-white">Connect {connectModal.name}</h2>
            <p className="mt-1 text-xs text-slate-400">
              Provide your channel username and API access token or OAuth credentials.
            </p>

            <form onSubmit={handleConnect} className="mt-5 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300">Username / Handle</label>
                <input
                  type="text"
                  required
                  value={usernameInput}
                  onChange={(e) => setUsernameInput(e.target.value)}
                  placeholder="@yourbrand"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">
                  Access Token / API Secret
                </label>
                <input
                  type="password"
                  value={tokenInput}
                  onChange={(e) => setTokenInput(e.target.value)}
                  placeholder="Paste OAuth token or leave blank for dev sandbox"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="mt-6 flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setConnectModal(null)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-xs font-medium text-slate-300 transition hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={connecting}
                  className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500 disabled:opacity-50"
                >
                  {connecting ? "Connecting..." : "Confirm & Save"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

