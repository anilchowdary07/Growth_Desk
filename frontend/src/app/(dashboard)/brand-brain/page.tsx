"use client";

import React, { useState, useEffect } from "react";
import {
  Brain,
  Save,
  FileText,
  Trash2,
  Search,
  Plus,
  ShieldAlert,
  Sparkles,
  Palette,
  CheckCircle2,
} from "lucide-react";
import { api } from "@/lib/api";

export default function BrandBrainPage() {
  const [activeTab, setActiveTab] = useState<"profile" | "documents" | "query">("profile");
  const [profile, setProfile] = useState<any>({
    company_name: "",
    industry: "",
    description: "",
    target_audience: "",
    brand_voice: "Modern, authoritative, and direct",
    tone_keywords: ["innovative", "approachable", "action-oriented"],
    website: "",
    products_services: "",
    competitors: ["Competitor A", "Competitor B"],
    restricted_topics: ["No unrealistic income claims", "No medical guarantees"],
  });
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // New Document modal
  const [docTitle, setDocTitle] = useState("");
  const [docContent, setDocContent] = useState("");
  const [isAddingDoc, setIsAddingDoc] = useState(false);

  // Query Brain test
  const [queryInput, setQueryInput] = useState("");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState(false);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const p = await api.getBrandProfile();
        if (p) setProfile(p);
        const docs = await api.getBrandDocuments();
        setDocuments(docs);
      } catch {
        // fallback
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const updated = await api.saveBrandProfile(profile);
      setProfile(updated);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleAddDocument = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.addBrandDocument({
        title: docTitle,
        content: docContent,
        doc_type: "text",
      });
      setDocTitle("");
      setDocContent("");
      setIsAddingDoc(false);
      const docs = await api.getBrandDocuments();
      setDocuments(docs);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDeleteDoc = async (id: string) => {
    if (!confirm("Are you sure you want to remove this document from Brand Brain?")) return;
    try {
      await api.deleteBrandDocument(id);
      setDocuments((prev) => prev.filter((d) => d.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!queryInput.trim()) return;
    setQueryLoading(true);
    try {
      const res = await api.queryBrand(queryInput);
      setQueryResult(res);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setQueryLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Page Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
            <Brain className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Brand Brain Knowledge Base</h1>
            <p className="text-xs text-slate-400">Central context and voice guidelines accessed by all AI agents</p>
          </div>
        </div>

        {/* Tab navigation */}
        <div className="flex rounded-lg border border-slate-800 bg-slate-900/60 p-1">
          <button
            onClick={() => setActiveTab("profile")}
            className={`rounded-md px-3 py-1 text-xs font-medium transition ${
              activeTab === "profile" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
            }`}
          >
            Brand Profile
          </button>
          <button
            onClick={() => setActiveTab("documents")}
            className={`rounded-md px-3 py-1 text-xs font-medium transition ${
              activeTab === "documents" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
            }`}
          >
            Knowledge Documents ({documents.length})
          </button>
          <button
            onClick={() => setActiveTab("query")}
            className={`rounded-md px-3 py-1 text-xs font-medium transition ${
              activeTab === "query" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
            }`}
          >
            Query RAG Index
          </button>
        </div>
      </div>

      {/* Main Body */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/40">
        <div className="mx-auto max-w-4xl">
          {/* TAB 1: Brand Profile Form */}
          {activeTab === "profile" && (
            <form onSubmit={handleSaveProfile} className="space-y-6">
              {savedSuccess && (
                <div className="flex items-center gap-2 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-3.5 text-xs font-medium text-emerald-400">
                  <CheckCircle2 className="h-4 w-4" />
                  Brand Brain synchronized! All 10 specialist agents will now use these guidelines.
                </div>
              )}

              {/* Core Company Info */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <h2 className="text-sm font-semibold text-white">Company Identity & Positioning</h2>
                <div className="mt-4 grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300">Company / Brand Name</label>
                    <input
                      type="text"
                      required
                      value={profile.company_name || ""}
                      onChange={(e) => setProfile({ ...profile, company_name: e.target.value })}
                      placeholder="GrowthCo"
                      className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-300">Industry / Domain</label>
                    <input
                      type="text"
                      value={profile.industry || ""}
                      onChange={(e) => setProfile({ ...profile, industry: e.target.value })}
                      placeholder="B2B SaaS / Fitness & Wellness"
                      className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="mt-4">
                  <label className="block text-xs font-medium text-slate-300">Company Overview</label>
                  <textarea
                    rows={3}
                    value={profile.description || ""}
                    onChange={(e) => setProfile({ ...profile, description: e.target.value })}
                    placeholder="We provide executive coaching programs that help corporate founders scale to 8 figures without burnout..."
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div className="mt-4">
                  <label className="block text-xs font-medium text-slate-300">Core Products & Offers</label>
                  <textarea
                    rows={2}
                    value={profile.products_services || ""}
                    onChange={(e) => setProfile({ ...profile, products_services: e.target.value })}
                    placeholder="Flagship 90-day accelerator ($5,000), 1-on-1 intensive VIP days ($2,500)..."
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              {/* Brand Voice & Tone */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <h2 className="text-sm font-semibold text-white">Brand Voice & Vocabulary</h2>
                <div className="mt-4">
                  <label className="block text-xs font-medium text-slate-300">Voice Guidelines</label>
                  <input
                    type="text"
                    value={profile.brand_voice || ""}
                    onChange={(e) => setProfile({ ...profile, brand_voice: e.target.value })}
                    placeholder="Punchy, authoritative, highly empathetic, zero corporate jargon"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div className="mt-4">
                  <label className="block text-xs font-medium text-slate-300">
                    Tone Keywords (comma-separated)
                  </label>
                  <input
                    type="text"
                    value={Array.isArray(profile.tone_keywords) ? profile.tone_keywords.join(", ") : ""}
                    onChange={(e) =>
                      setProfile({
                        ...profile,
                        tone_keywords: e.target.value.split(",").map((s) => s.trim()),
                      })
                    }
                    placeholder="visionary, direct, trustworthy, tactical"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              {/* Compliance & Prohibited Topics */}
              <div className="rounded-2xl border border-rose-500/20 bg-slate-900/80 p-6 shadow-xl">
                <div className="flex items-center gap-2 text-rose-400">
                  <ShieldAlert className="h-4 w-4" />
                  <h2 className="text-sm font-semibold">Strict Guardrails & Restricted Claims</h2>
                </div>
                <p className="mt-1 text-xs text-slate-400">
                  AI agents will be strictly instructed never to make these statements or use these forbidden claims.
                </p>

                <div className="mt-4">
                  <textarea
                    rows={2}
                    value={Array.isArray(profile.restricted_topics) ? profile.restricted_topics.join("\n") : ""}
                    onChange={(e) =>
                      setProfile({
                        ...profile,
                        restricted_topics: e.target.value.split("\n").filter((s) => s.trim().length > 0),
                      })
                    }
                    placeholder="No unrealistic income promises (e.g., 'guaranteed 10k/month')&#10;No unverified health guarantees&#10;Never mention competitor trademarked formulas"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-rose-500 focus:outline-none"
                  />
                </div>
              </div>

              {/* Submit button */}
              <div className="flex justify-end">
                <button
                  type="submit"
                  className="flex items-center gap-2 rounded-xl bg-blue-600 px-6 py-2.5 text-xs font-semibold text-white shadow-lg shadow-blue-500/20 transition hover:bg-blue-500"
                >
                  <Save className="h-4 w-4" />
                  Save & Sync Brand Brain
                </button>
              </div>
            </form>
          )}

          {/* TAB 2: Documents */}
          {activeTab === "documents" && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-sm font-semibold text-white">Reference Knowledge Documents</h2>
                  <p className="text-xs text-slate-400">
                    Product guides, customer case studies, FAQs, and competitor teardowns
                  </p>
                </div>
                <button
                  onClick={() => setIsAddingDoc(true)}
                  className="flex items-center gap-1.5 rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-blue-500"
                >
                  <Plus className="h-4 w-4" />
                  Add Document
                </button>
              </div>

              {documents.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-slate-800 p-8 text-center bg-slate-950/40">
                  <FileText className="mx-auto h-8 w-8 text-slate-600" />
                  <p className="mt-2 text-xs font-medium text-slate-300">No documents uploaded yet</p>
                  <p className="mt-1 text-[11px] text-slate-400">
                    Add product specifications, FAQs, or founder stories to ground your AI agents.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {documents.map((doc) => (
                    <div
                      key={doc.id}
                      className="rounded-xl border border-slate-800 bg-slate-900/80 p-4 shadow-md flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-start justify-between">
                          <h3 className="text-xs font-semibold text-white line-clamp-1">{doc.title}</h3>
                          <button
                            onClick={() => handleDeleteDoc(doc.id)}
                            className="text-slate-500 transition hover:text-red-400"
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </div>
                        <p className="mt-2 text-[11px] text-slate-400 line-clamp-3">
                          {doc.content || "No content preview available."}
                        </p>
                      </div>

                      <div className="mt-3 flex items-center justify-between text-[10px] text-slate-400 border-t border-slate-800/60 pt-2">
                        <span className="uppercase">{doc.doc_type}</span>
                        <span>RAG Indexed</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 3: Query RAG Index */}
          {activeTab === "query" && (
            <div className="space-y-6">
              <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
                <h2 className="text-sm font-semibold text-white">Test Brand Brain Retrieval (RAG)</h2>
                <p className="mt-1 text-xs text-slate-400">
                  Verify how your marketing agents search and retrieve brand knowledge before answering.
                </p>

                <form onSubmit={handleQuery} className="mt-4 flex gap-2">
                  <input
                    type="text"
                    value={queryInput}
                    onChange={(e) => setQueryInput(e.target.value)}
                    placeholder="e.g. 'What is our refund policy?' or 'What are our primary value props?'"
                    className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                  <button
                    type="submit"
                    disabled={queryLoading}
                    className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-blue-500 disabled:opacity-50"
                  >
                    {queryLoading ? "Searching..." : "Retrieve"}
                  </button>
                </form>

                {queryResult && (
                  <div className="mt-6 space-y-4 border-t border-slate-800 pt-4">
                    <div className="text-xs font-semibold text-blue-400">Compiled Brand Context:</div>
                    <pre className="rounded-lg bg-slate-950 p-4 text-[11px] text-slate-300 overflow-x-auto whitespace-pre-wrap">
                      {queryResult.context}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Add Document Modal */}
      {isAddingDoc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <h2 className="text-lg font-semibold text-white">Add Reference Document</h2>
            <p className="mt-1 text-xs text-slate-400">
              Paste knowledge, FAQs, product specs, or customer testimonials into the Brand Brain.
            </p>

            <form onSubmit={handleAddDocument} className="mt-5 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300">Document Title</label>
                <input
                  type="text"
                  required
                  value={docTitle}
                  onChange={(e) => setDocTitle(e.target.value)}
                  placeholder="Master Product FAQs & Objections"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Content / Text</label>
                <textarea
                  rows={6}
                  required
                  value={docContent}
                  onChange={(e) => setDocContent(e.target.value)}
                  placeholder="Q: What happens if a client doesn't get results?&#10;A: We offer a 100% satisfaction guarantee within 14 days..."
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="mt-6 flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsAddingDoc(false)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-xs font-medium text-slate-300 transition hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-blue-500"
                >
                  Index into Brand Brain
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
