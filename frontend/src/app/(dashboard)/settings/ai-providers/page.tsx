"use client";

import React, { useState, useEffect } from "react";
import {
  KeyRound,
  Plus,
  CheckCircle2,
  AlertCircle,
  Trash2,
  RefreshCw,
  Cpu,
  ExternalLink,
  ShieldCheck,
  Radio,
  Sparkles,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

interface ProviderPreset {
  id: string;
  name: string;
  defaultModel: string;
  keyPrefix: string;
  baseUrl?: string;
  badge: string;
  docsUrl: string;
}

const PRESETS: ProviderPreset[] = [
  {
    id: "auto",
    name: "⚡ Auto-Detect Any Key",
    defaultModel: "Auto-selected based on key",
    keyPrefix: "Any key format",
    badge: "Smart Router",
    docsUrl: "https://openrouter.ai",
  },
  {
    id: "gemini",
    name: "Google Gemini",
    defaultModel: "gemini-2.0-flash",
    keyPrefix: "AIza...",
    badge: "Free Tier Available",
    docsUrl: "https://aistudio.google.com/app/apikey",
  },
  {
    id: "openai",
    name: "OpenAI",
    defaultModel: "gpt-4o",
    keyPrefix: "sk-...",
    badge: "Industry Standard",
    docsUrl: "https://platform.openai.com/api-keys",
  },
  {
    id: "anthropic",
    name: "Anthropic Claude",
    defaultModel: "claude-3-5-sonnet-20241022",
    keyPrefix: "sk-ant-...",
    badge: "Reasoning & Copy",
    docsUrl: "https://console.anthropic.com/settings/keys",
  },
  {
    id: "openrouter",
    name: "OpenRouter",
    defaultModel: "meta-llama/llama-3.3-70b-instruct",
    keyPrefix: "sk-or-...",
    badge: "300+ Models / 1 Key",
    docsUrl: "https://openrouter.ai/keys",
  },
  {
    id: "deepseek",
    name: "DeepSeek",
    defaultModel: "deepseek-chat",
    keyPrefix: "sk-... / dsk-...",
    badge: "High Performance",
    docsUrl: "https://platform.deepseek.com/api_keys",
  },
  {
    id: "groq",
    name: "Groq (LPU)",
    defaultModel: "llama-3.3-70b-versatile",
    keyPrefix: "gsk_...",
    badge: "Instant Speed",
    docsUrl: "https://console.groq.com/keys",
  },
  {
    id: "mistral",
    name: "Mistral AI",
    defaultModel: "mistral-large-latest",
    keyPrefix: "mistral-... / ms-...",
    badge: "European Sovereign",
    docsUrl: "https://console.mistral.ai/api-keys",
  },
  {
    id: "perplexity",
    name: "Perplexity",
    defaultModel: "sonar-pro",
    keyPrefix: "pplx-...",
    badge: "Search Grounded",
    docsUrl: "https://www.perplexity.ai/settings/api",
  },
  {
    id: "together",
    name: "Together AI",
    defaultModel: "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    keyPrefix: "Alphanumeric",
    badge: "Open Source Hub",
    docsUrl: "https://api.together.ai/settings/api-keys",
  },
  {
    id: "xai",
    name: "xAI (Grok)",
    defaultModel: "grok-2-latest",
    keyPrefix: "xai-...",
    badge: "Real-time X Access",
    docsUrl: "https://console.x.ai/",
  },
  {
    id: "custom",
    name: "Custom / Local (Ollama, vLLM)",
    defaultModel: "default",
    keyPrefix: "Any local key",
    baseUrl: "http://localhost:11434/v1",
    badge: "Self-Hosted",
    docsUrl: "https://ollama.ai",
  },
];

export default function AIProvidersSettingsPage() {
  const [providers, setProviders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [testingId, setTestingId] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<any | null>(null);

  // Add provider form
  const [isAdding, setIsAdding] = useState(false);
  const [providerType, setProviderType] = useState("auto");
  const [apiKey, setApiKey] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [defaultModel, setDefaultModel] = useState("");
  const [baseUrl, setBaseUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [testingRaw, setTestingRaw] = useState(false);
  const [rawTestNotice, setRawTestNotice] = useState<{ success: boolean; message: string } | null>(null);

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

  const detectKeyType = (val: string): { type: string; name: string } => {
    const k = val.trim();
    if (k.startsWith("AIza")) return { type: "gemini", name: "Google Gemini" };
    if (k.startsWith("sk-ant-")) return { type: "anthropic", name: "Anthropic Claude" };
    if (k.startsWith("sk-or-")) return { type: "openrouter", name: "OpenRouter" };
    if (k.startsWith("gsk_")) return { type: "groq", name: "Groq" };
    if (k.startsWith("pplx-")) return { type: "perplexity", name: "Perplexity" };
    if (k.startsWith("xai-")) return { type: "xai", name: "xAI (Grok)" };
    if (k.startsWith("dsk-")) return { type: "deepseek", name: "DeepSeek" };
    if (k.startsWith("mistral-") || k.startsWith("ms-")) return { type: "mistral", name: "Mistral AI" };
    if (k.startsWith("sk-")) return { type: "openai", name: "OpenAI or Compatible" };
    if (k.length > 5) return { type: "custom", name: "Custom / Local Endpoint" };
    return { type: "unknown", name: "Unknown" };
  };

  const handleKeyChange = (val: string) => {
    setApiKey(val);
    setRawTestNotice(null);
    const detected = detectKeyType(val);

    if (providerType === "auto" && detected.type !== "unknown") {
      const preset = PRESETS.find((p) => p.id === detected.type);
      if (preset && preset.defaultModel && !preset.defaultModel.includes("Auto")) {
        setDefaultModel(preset.defaultModel);
      }
    }
  };

  const selectPreset = (preset: ProviderPreset) => {
    setProviderType(preset.id);
    setRawTestNotice(null);
    if (preset.id !== "auto") {
      setDefaultModel(preset.defaultModel);
      setDisplayName(preset.name);
      if (preset.baseUrl) {
        setBaseUrl(preset.baseUrl);
      } else {
        setBaseUrl("");
      }
    } else {
      setDefaultModel("");
      setDisplayName("");
      setBaseUrl("");
    }
  };

  const handleTestKeyBeforeSave = async () => {
    if (!apiKey.trim()) {
      alert("Please enter an API key first.");
      return;
    }
    setTestingRaw(true);
    setRawTestNotice(null);
    try {
      const res = await api.testRawKey({
        provider_type: providerType,
        api_key: apiKey.trim(),
        default_model: defaultModel.trim() || undefined,
        base_url: baseUrl.trim() || undefined,
      });
      setRawTestNotice({
        success: res.success,
        message: res.message,
      });
    } catch (err: any) {
      setRawTestNotice({
        success: false,
        message: err.message || "Failed to test connection",
      });
    } finally {
      setTestingRaw(false);
    }
  };

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
        api_key: apiKey.trim(),
        display_name: displayName.trim() || undefined,
        default_model: defaultModel.trim() || undefined,
        base_url: baseUrl.trim() || undefined,
      });
      setIsAdding(false);
      setApiKey("");
      setDisplayName("");
      setDefaultModel("");
      setBaseUrl("");
      setRawTestNotice(null);
      await loadProviders();
    } catch (err: any) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const currentDetection = detectKeyType(apiKey);

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30">
            <KeyRound className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Universal AI Providers (BYOK)</h1>
            <p className="text-xs text-slate-400">
              Bring Your Own Key: Works with any provider, any model, and any custom endpoint
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsAdding(true)}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-3.5 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500"
        >
          <Plus className="h-4 w-4" />
          Connect Any API Key
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        <div className="mx-auto max-w-5xl space-y-6">
          {/* Universal Compatibility Banner */}
          <div className="rounded-2xl border border-blue-500/20 bg-gradient-to-r from-blue-950/40 via-indigo-950/20 to-slate-900/40 p-5 shadow-lg">
            <div className="flex items-start gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-500/20 text-blue-400 border border-blue-500/30">
                <Cpu className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h2 className="text-sm font-semibold text-white">Universal Bring Your Own Key (BYOK) Engine</h2>
                  <span className="rounded bg-emerald-500/20 px-2 py-0.5 text-[10px] font-semibold text-emerald-400 border border-emerald-500/30">
                    Zero Lock-In
                  </span>
                </div>
                <p className="mt-1.5 text-xs text-slate-300 leading-relaxed">
                  GrowthDesk is completely provider-agnostic. You can connect <strong>ANY</strong> API key you hold: Google Gemini, OpenAI, Anthropic Claude, OpenRouter, DeepSeek, Groq, Mistral, Perplexity, Together AI, xAI (Grok), or local/private LLMs (Ollama, vLLM). All credentials are protected with server-side Fernet encryption and never exposed in frontend responses.
                </p>

                <div className="mt-3 flex flex-wrap gap-2">
                  {PRESETS.filter((p) => p.id !== "auto").map((p) => (
                    <span
                      key={p.id}
                      className="rounded-lg border border-slate-800 bg-slate-950/60 px-2.5 py-1 text-[11px] font-medium text-slate-400"
                    >
                      {p.name}
                    </span>
                  ))}
                </div>
              </div>
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
                {testResult.success ? "Connection Verified!" : "Connection Notice"}
              </div>
              <p className="mt-1 text-[11px] opacity-90">{testResult.message}</p>
            </div>
          )}

          {/* Active Providers List */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-semibold text-white">Connected Providers & Keys ({providers.length})</h2>
                <p className="mt-1 text-xs text-slate-400">
                  Active model engines driving your autonomous AI marketing workforce.
                </p>
              </div>
              <button
                onClick={() => setIsAdding(true)}
                className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white hover:bg-slate-700 transition"
              >
                <Plus className="h-3.5 w-3.5" />
                Add Key
              </button>
            </div>

            <div className="mt-4 space-y-3">
              {providers.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-800 p-8 text-center bg-slate-950/40">
                  <KeyRound className="mx-auto h-8 w-8 text-slate-600" />
                  <p className="mt-2 text-xs font-semibold text-white">No custom API keys connected yet</p>
                  <p className="mt-1 text-[11px] text-slate-400 max-w-md mx-auto">
                    The platform will operate in safe preview mode using the built-in Strategy Engine. Paste any provider API key to immediately switch your agents to live model generation!
                  </p>
                  <button
                    onClick={() => setIsAdding(true)}
                    className="mt-4 rounded-lg bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-blue-500 transition"
                  >
                    Paste an API Key
                  </button>
                </div>
              ) : (
                providers.map((prov) => (
                  <div
                    key={prov.id}
                    className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/60 p-4 hover:border-slate-700 transition"
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
                        {prov.base_url && (
                          <span className="text-[10px] text-slate-500 font-mono">
                            Endpoint: {prov.base_url}
                          </span>
                        )}
                      </div>
                      <p className="mt-1 text-[11px] text-slate-400">
                        Provider: <span className="uppercase text-slate-300 font-semibold">{prov.provider_type}</span> &bull; Status:{" "}
                        {prov.last_verified_at ? (
                          <span className="text-emerald-400 font-medium">
                            Verified ({formatDate(prov.last_verified_at)})
                          </span>
                        ) : (
                          <span className="text-amber-400 font-medium">Ready to test</span>
                        )}
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
                        title="Delete key"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Quick Setup Guide: Where to get API Keys */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Where to get API Keys
            </h3>
            <div className="mt-3 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {PRESETS.filter((p) => p.id !== "auto").map((p) => (
                <a
                  key={p.id}
                  href={p.docsUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-between rounded-xl border border-slate-800/80 bg-slate-950/50 p-3 hover:border-slate-700 hover:bg-slate-900 transition group"
                >
                  <div>
                    <p className="text-xs font-semibold text-white group-hover:text-blue-400 transition">
                      {p.name}
                    </p>
                    <p className="text-[10px] text-slate-400">{p.badge}</p>
                  </div>
                  <ExternalLink className="h-3.5 w-3.5 text-slate-500 group-hover:text-slate-300" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Add / Connect Provider Modal */}
      {isAdding && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto">
          <div className="w-full max-w-xl rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl my-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-semibold text-white">Connect Any AI Key (BYOK)</h2>
                <p className="mt-0.5 text-xs text-slate-400">
                  Select a provider or choose Auto-Detect. Paste your key and test before saving.
                </p>
              </div>
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <Sparkles className="h-4 w-4" />
              </div>
            </div>

            {/* Provider Preset Chips */}
            <div className="mt-4">
              <label className="block text-[11px] font-medium text-slate-400 mb-1.5">
                Quick Select Provider Preset
              </label>
              <div className="grid grid-cols-3 gap-1.5 sm:grid-cols-4">
                {PRESETS.map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => selectPreset(p)}
                    className={`rounded-lg border px-2 py-1.5 text-left text-[11px] font-medium transition ${
                      providerType === p.id
                        ? "border-blue-500 bg-blue-500/20 text-white"
                        : "border-slate-800 bg-slate-950/60 text-slate-400 hover:border-slate-700 hover:text-slate-200"
                    }`}
                  >
                    <div className="truncate">{p.name.replace("⚡ ", "")}</div>
                  </button>
                ))}
              </div>
            </div>

            <form onSubmit={handleAdd} className="mt-4 space-y-4">
              {/* API Key Input */}
              <div>
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-medium text-slate-300">API Key</label>
                  {apiKey && currentDetection.type !== "unknown" && (
                    <span className="text-[10px] font-semibold text-blue-400">
                      Detected format: {currentDetection.name}
                    </span>
                  )}
                </div>
                <input
                  type="password"
                  required
                  value={apiKey}
                  onChange={(e) => handleKeyChange(e.target.value)}
                  placeholder="Paste any API key (e.g. sk-..., AIzaSy..., gsk_..., or local token)"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none font-mono"
                />
              </div>

              {/* Endpoint Base URL (shown for Custom or editable) */}
              {(providerType === "custom" || baseUrl) && (
                <div>
                  <label className="block text-xs font-medium text-slate-300">
                    Custom Base URL / Endpoint
                  </label>
                  <input
                    type="text"
                    value={baseUrl}
                    onChange={(e) => setBaseUrl(e.target.value)}
                    placeholder="http://localhost:11434/v1"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none font-mono"
                  />
                  <p className="mt-1 text-[10px] text-slate-500">
                    Works with Ollama, LM Studio, vLLM, LiteLLM, or any OpenAI-compatible API host.
                  </p>
                </div>
              )}

              {/* Display Name & Model */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300">Display Name</label>
                  <input
                    type="text"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    placeholder="e.g. Production GPT-4o"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300">Default Model ID</label>
                  <input
                    type="text"
                    value={defaultModel}
                    onChange={(e) => setDefaultModel(e.target.value)}
                    placeholder="e.g. gpt-4o, gemini-2.0-flash"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none font-mono"
                  />
                </div>
              </div>

              {/* Instant Test Raw Key feedback */}
              {rawTestNotice && (
                <div
                  className={`rounded-xl border p-3 text-xs ${
                    rawTestNotice.success
                      ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
                      : "border-amber-500/30 bg-amber-500/10 text-amber-300"
                  }`}
                >
                  <div className="flex items-center gap-1.5 font-semibold">
                    {rawTestNotice.success ? (
                      <CheckCircle2 className="h-3.5 w-3.5" />
                    ) : (
                      <AlertCircle className="h-3.5 w-3.5" />
                    )}
                    {rawTestNotice.success ? "Key Connected!" : "Key Notice"}
                  </div>
                  <p className="mt-1 text-[11px] opacity-90">{rawTestNotice.message}</p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="mt-6 flex items-center justify-between pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={handleTestKeyBeforeSave}
                  disabled={testingRaw || !apiKey.trim()}
                  className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-700 transition disabled:opacity-50"
                >
                  <RefreshCw className={`h-3 w-3 ${testingRaw ? "animate-spin" : ""}`} />
                  {testingRaw ? "Verifying Key..." : "Test Connection Now"}
                </button>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setIsAdding(false)}
                    className="rounded-lg border border-slate-700 px-3.5 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting || !apiKey.trim()}
                    className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-500 disabled:opacity-50 shadow-md shadow-blue-500/20"
                  >
                    {submitting ? "Encrypting & Saving..." : "Save & Activate Key"}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
