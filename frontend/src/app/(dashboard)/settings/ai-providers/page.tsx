"use client";

import React, { useState, useEffect } from "react";
import {
  KeyRound,
  Plus,
  CheckCircle2,
  AlertCircle,
  Trash2,
  RefreshCw,
  ShieldCheck,
  ExternalLink,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function AIProvidersSettingsPage() {
  const [providers, setProviders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [testingId, setTestingId] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<any | null>(null);

  // Add provider form
  const [isAdding, setIsAdding] = useState(false);
  const [providerType, setProviderType] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [defaultModel, setDefaultModel] = useState("gpt-4o");
  const [submitting, setSubmitting] = useState(false);

  const loadProviders = async () => {
    setLoading(true);
    try {
      const data = await api.getProviders();
      setProviders(data);
    } catch {
      // fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProviders();
  }, []);

  const handleTest = async (id: string) => {
    setTestingId(id);
    setTestResult(null);
    try {
      const res = await api.testProvider(id);
      setTestResult(res);
      await loadProviders();
    } catch (err: any) {
      setTestResult({ success: false, message: err.message });
    } finally {
      setTestingId(null);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to remove this provider key?")) return;
    try {
      await api.deleteProvider(id);
      await loadProviders();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.addProvider({
        provider_type: providerType,
        api_key: apiKey,
        display_name: displayName || undefined,
        default_model: defaultModel,
      });
      setIsAdding(false);
      setApiKey("");
      setDisplayName("");
      await loadProviders();
    } catch (err: any) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30">
            <KeyRound className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">AI Providers (BYOK)</h1>
            <p className="text-xs text-slate-400">Bring Your Own Key model — configure OpenAI, Anthropic, or Gemini</p>
          </div>
        </div>

        <button
          onClick={() => setIsAdding(true)}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-3.5 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500"
        >
          <Plus className="h-4 w-4" />
          Add Provider Key
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        <div className="mx-auto max-w-4xl space-y-6">
          {/* Security Notice */}
          <div className="rounded-xl border border-blue-500/20 bg-blue-500/10 p-4 flex items-start gap-3 text-xs text-blue-300">
            <ShieldCheck className="h-5 w-5 shrink-0 text-blue-400 mt-0.5" />
            <div>
              <p className="font-semibold text-white">Zero-Knowledge Server-Side Fernet Encryption</p>
              <p className="mt-1 text-slate-300 leading-relaxed">
                Your API keys are encrypted at rest using military-grade cryptography. Keys are never transmitted back to the browser or stored in logs. You pay the AI provider directly for your usage; our SaaS infrastructure orchestrates your workforce.
              </p>
            </div>
          </div>

          {/* Test Result Alert */}
          {testResult && (
            <div
              className={`rounded-xl border p-4 text-xs font-medium ${
                testResult.success
                  ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
                  : "border-rose-500/30 bg-rose-500/10 text-rose-300"
              }`}
            >
              <div className="flex items-center gap-2 font-semibold">
                {testResult.success ? <CheckCircle2 className="h-4 w-4" /> : <AlertCircle className="h-4 w-4" />}
                {testResult.success ? "Connection Verified!" : "Connection Failed"}
              </div>
              <p className="mt-1 text-[11px] opacity-90">{testResult.message}</p>
            </div>
          )}

          {/* Active Providers List */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h2 className="text-sm font-semibold text-white">Configured Providers ({providers.length})</h2>
            <p className="mt-1 text-xs text-slate-400">
              Active LLM engines available to your marketing workforce.
            </p>

            <div className="mt-4 space-y-3">
              {providers.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-800 p-8 text-center bg-slate-950/40">
                  <KeyRound className="mx-auto h-8 w-8 text-slate-600" />
                  <p className="mt-2 text-xs font-semibold text-white">No AI providers configured</p>
                  <p className="mt-1 text-[11px] text-slate-400">
                    Add your OpenAI, Gemini, or Claude API key above to activate your marketing department.
                  </p>
                </div>
              ) : (
                providers.map((prov) => (
                  <div
                    key={prov.id}
                    className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 p-4"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-xs text-white">{prov.display_name}</span>
                        {prov.is_default && (
                          <span className="rounded bg-blue-500/20 px-2 py-0.5 text-[10px] font-semibold text-blue-400 border border-blue-500/30">
                            Primary Engine
                          </span>
                        )}
                        <span className="text-[11px] text-slate-400 font-mono">
                          Model: {prov.default_model || "Default"}
                        </span>
                      </div>
                      <p className="mt-1 text-[11px] text-slate-400">
                        Type: <span className="uppercase text-slate-300 font-semibold">{prov.provider_type}</span> &bull; Last verified:{" "}
                        {prov.last_verified_at ? formatDate(prov.last_verified_at) : "Pending test"}
                      </p>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleTest(prov.id)}
                        disabled={testingId === prov.id}
                        className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-slate-300 hover:bg-slate-700 transition disabled:opacity-50"
                      >
                        <RefreshCw className={`h-3 w-3 ${testingId === prov.id ? "animate-spin" : ""}`} />
                        {testingId === prov.id ? "Testing..." : "Test Connection"}
                      </button>
                      <button
                        onClick={() => handleDelete(prov.id)}
                        className="p-1.5 text-slate-500 hover:text-rose-400 transition"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Add Provider Modal */}
      {isAdding && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <h2 className="text-base font-semibold text-white">Add AI Provider Key (BYOK)</h2>
            <p className="mt-1 text-xs text-slate-400">
              Provide your API key. It will be encrypted immediately and never shown again.
            </p>

            <form onSubmit={handleAdd} className="mt-5 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300">AI Provider</label>
                <select
                  value={providerType}
                  onChange={(e) => {
                    const p = e.target.value;
                    setProviderType(p);
                    if (p === "openai") setDefaultModel("gpt-4o");
                    else if (p === "gemini") setDefaultModel("gemini-2.0-flash");
                    else if (p === "anthropic") setDefaultModel("claude-sonnet-4-20250514");
                  }}
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                >
                  <option value="openai">OpenAI (GPT-4o, GPT-4o-mini, o1)</option>
                  <option value="gemini">Google Gemini (Gemini 2.0 Flash, 2.5 Pro)</option>
                  <option value="anthropic">Anthropic Claude (Claude 3.5 Sonnet, Haiku)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">API Key</label>
                <input
                  type="password"
                  required
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Display Label</label>
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="Company OpenAI Key"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Default Model</label>
                <input
                  type="text"
                  value={defaultModel}
                  onChange={(e) => setDefaultModel(e.target.value)}
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none font-mono"
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
                  disabled={submitting}
                  className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-500"
                >
                  {submitting ? "Encrypting & Storing..." : "Save Provider"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
