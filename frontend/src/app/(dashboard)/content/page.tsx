"use client";

import React, { useState, useEffect } from "react";
import {
  PenTool,
  Plus,
  Sparkles,
  CheckCircle2,
  Trash2,
  Copy,
  Check,
  Instagram,
  Linkedin,
  Twitter,
  Youtube,
  Globe,
  Filter,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

const contentTypes = [
  { id: "all", label: "All Formats" },
  { id: "social_post", label: "Social Post" },
  { id: "blog", label: "Blog Article" },
  { id: "script", label: "Video Script" },
  { id: "ad_copy", label: "Ad Copy" },
  { id: "carousel", label: "Carousel Breakdown" },
];

const platformIcons: Record<string, any> = {
  instagram: Instagram,
  linkedin: Linkedin,
  twitter: Twitter,
  youtube: Youtube,
};

export default function ContentStudioPage() {
  const [contentList, setContentList] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedType, setSelectedType] = useState("all");
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Generate modal
  const [isGenerating, setIsGenerating] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [genType, setGenType] = useState("social_post");
  const [genPlatform, setGenPlatform] = useState("linkedin");
  const [guidelines, setGuidelines] = useState("");
  const [genLoading, setGenLoading] = useState(false);

  const loadContent = async () => {
    setLoading(true);
    try {
      const data = await api.getContentItems(
        selectedType !== "all" ? { content_type: selectedType } : undefined
      );
      setContentList(data);
    } catch {
      // fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadContent();
  }, [selectedType]);

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleApprove = async (id: string) => {
    try {
      await api.approveContent(id);
      await loadContent();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this content piece?")) return;
    try {
      await api.deleteContent(id);
      setContentList((prev) => prev.filter((c) => c.id !== id));
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenLoading(true);
    try {
      await api.generateContent({
        prompt,
        content_type: genType,
        platform: genPlatform,
        additional_guidelines: guidelines || undefined,
      });
      setIsGenerating(false);
      setPrompt("");
      setGuidelines("");
      await loadContent();
    } catch (err: any) {
      alert(`Generation failed: ${err.message}. Verify that an AI provider is active.`);
    } finally {
      setGenLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Page Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30">
            <PenTool className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Content Studio</h1>
            <p className="text-xs text-slate-400">High-converting multi-platform copy production</p>
          </div>
        </div>

        <button
          onClick={() => setIsGenerating(true)}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-3.5 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500"
        >
          <Sparkles className="h-4 w-4" />
          Generate with AI
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between border-b border-slate-800 bg-slate-950/40 px-6 py-2.5">
        <div className="flex items-center gap-1">
          {contentTypes.map((type) => (
            <button
              key={type.id}
              onClick={() => setSelectedType(type.id)}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                selectedType === type.id
                  ? "bg-slate-800 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {type.label}
            </button>
          ))}
        </div>
        <span className="text-xs text-slate-400">{contentList.length} assets produced</span>
      </div>

      {/* Content Grid */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        {loading ? (
          <div className="p-12 text-center text-xs text-slate-400">Loading content pieces...</div>
        ) : contentList.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-800 p-12 text-center bg-slate-950/40">
            <PenTool className="mx-auto h-8 w-8 text-slate-600" />
            <p className="mt-3 text-xs font-medium text-slate-300">No content items generated yet</p>
            <p className="mt-1 text-[11px] text-slate-400">
              Click &ldquo;Generate with AI&rdquo; to produce posts, blogs, or scripts grounded in your Brand Brain.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {contentList.map((item) => {
              const IconComp = item.platform ? platformIcons[item.platform.toLowerCase()] || Globe : Globe;
              const isApproved = item.status === "approved";

              return (
                <div
                  key={item.id}
                  className="flex flex-col justify-between rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg transition hover:border-slate-700"
                >
                  <div>
                    {/* Header tags */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1.5 rounded-md bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-slate-300">
                        <IconComp className="h-3 w-3" />
                        <span className="capitalize">{item.platform || "Multi-Channel"}</span>
                      </div>
                      <span
                        className={`rounded px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${
                          isApproved
                            ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                            : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                        }`}
                      >
                        {item.status}
                      </span>
                    </div>

                    <h3 className="mt-3 text-xs font-bold text-white line-clamp-1">{item.title}</h3>
                    <p className="mt-2 text-xs leading-relaxed text-slate-300 whitespace-pre-wrap line-clamp-6 bg-slate-950/60 p-3 rounded-lg border border-slate-800/60">
                      {item.body}
                    </p>
                  </div>

                  {/* Actions Footer */}
                  <div className="mt-4 flex items-center justify-between border-t border-slate-800/80 pt-3 text-xs">
                    <span className="text-[10px] text-slate-400">{formatDate(item.created_at)}</span>

                    <div className="flex items-center gap-1.5">
                      <button
                        onClick={() => handleCopy(item.id, item.body || "")}
                        title="Copy to clipboard"
                        className="rounded p-1.5 text-slate-400 transition hover:bg-slate-800 hover:text-white"
                      >
                        {copiedId === item.id ? (
                          <Check className="h-3.5 w-3.5 text-emerald-400" />
                        ) : (
                          <Copy className="h-3.5 w-3.5" />
                        )}
                      </button>

                      {!isApproved && (
                        <button
                          onClick={() => handleApprove(item.id)}
                          className="flex items-center gap-1 rounded bg-emerald-600/20 px-2 py-1 text-[11px] font-medium text-emerald-400 border border-emerald-500/30 hover:bg-emerald-600 hover:text-white transition"
                        >
                          <CheckCircle2 className="h-3 w-3" />
                          Approve
                        </button>
                      )}

                      <button
                        onClick={() => handleDelete(item.id)}
                        title="Delete"
                        className="rounded p-1.5 text-slate-500 transition hover:bg-slate-800 hover:text-rose-400"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Generate Content Modal */}
      {isGenerating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <div className="flex items-center gap-2 text-blue-400">
              <Sparkles className="h-5 w-5" />
              <h2 className="text-lg font-semibold text-white">Generate with Content Creator</h2>
            </div>
            <p className="mt-1 text-xs text-slate-400">
              The Content Creator agent will write copy aligned with your Brand Brain and target platform.
            </p>

            <form onSubmit={handleGenerate} className="mt-5 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300">Format</label>
                  <select
                    value={genType}
                    onChange={(e) => setGenType(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                  >
                    <option value="social_post">Social Media Post</option>
                    <option value="blog">SEO Blog Article</option>
                    <option value="script">Reel / Video Script</option>
                    <option value="ad_copy">Direct-Response Ad Copy</option>
                    <option value="carousel">Carousel Slide Deck</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300">Platform</label>
                  <select
                    value={genPlatform}
                    onChange={(e) => setGenPlatform(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                  >
                    <option value="linkedin">LinkedIn</option>
                    <option value="instagram">Instagram</option>
                    <option value="twitter">X (Twitter)</option>
                    <option value="youtube">YouTube</option>
                    <option value="facebook">Facebook</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Prompt / Theme</label>
                <textarea
                  rows={3}
                  required
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="e.g. 5 costly mistakes founders make when trying to scale organic inbound marketing..."
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">
                  Specific Hook or Call to Action (Optional)
                </label>
                <input
                  type="text"
                  value={guidelines}
                  onChange={(e) => setGuidelines(e.target.value)}
                  placeholder="End with: 'Comment SCALE for our free 14-page blueprint'"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="mt-6 flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsGenerating(false)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-xs font-medium text-slate-300 transition hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={genLoading}
                  className="rounded-lg bg-blue-600 px-5 py-2 text-xs font-semibold text-white shadow-md shadow-blue-500/20 transition hover:bg-blue-500 disabled:opacity-50"
                >
                  {genLoading ? "Writing..." : "Generate Content"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

