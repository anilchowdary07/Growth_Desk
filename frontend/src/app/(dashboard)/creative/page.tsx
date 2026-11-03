"use client";

import React, { useState } from "react";
import {
  Palette,
  Sparkles,
  Copy,
  Check,
  Image as ImageIcon,
  Sliders,
  Download,
} from "lucide-react";
import { api } from "@/lib/api";

const sampleCreatives = [
  {
    id: "1",
    title: "Executive Solopreneur Burnout Breakdown",
    format: "1:1 Square (Instagram / LinkedIn)",
    style: "Minimalist High-Contrast SaaS Graphic",
    prompt:
      "A cinematic, ultra-clean isometric visual showing a laptop surrounded by glowing neon analytics charts, dark slate background #0F172A with electric blue accents #3B82F6, high aesthetic typography, 8k resolution, octane render, modern design aesthetic --ar 1:1",
    aspect: "1:1",
  },
  {
    id: "2",
    title: "YouTube Thumbnail: 0 to 100k Monthly Organic Leads",
    format: "16:9 Landscape (YouTube)",
    style: "Hyper-Curiosity YouTube Thumbnail",
    prompt:
      "High-contrast YouTube thumbnail background, split view between red declining revenue graph on left and neon green parabolic growth curve on right, dramatic studio lighting, depth of field, vibrant colors, 4k --ar 16:9",
    aspect: "16:9",
  },
  {
    id: "3",
    title: "Story / Reel Cover: The 3 Secret Inbound Funnels",
    format: "9:16 Vertical (Reels / TikTok)",
    style: "Modern Editorial Minimalist Poster",
    prompt:
      "Vertical 9:16 poster composition, deep navy blue background, sleek geometric 3D glass pillars refracting light, clean modern layout, luxury design studio feel --ar 9:16",
    aspect: "9:16",
  },
];

export default function CreativeStudioPage() {
  const [creatives, setCreatives] = useState(sampleCreatives);
  const [conceptPrompt, setConceptPrompt] = useState("");
  const [style, setStyle] = useState("Minimalist Modern SaaS");
  const [aspect, setAspect] = useState("1:1");
  const [generating, setGenerating] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!conceptPrompt.trim()) return;
    setGenerating(true);

    try {
      const res = await api.chatWithAgent(
        `Generate a production-ready AI image generator prompt and design brief for this creative concept:\nConcept: ${conceptPrompt}\nPreferred Style: ${style}\nAspect Ratio: ${aspect}\nEnsure it follows Brand Brain visual standards and includes exact lighting, composition, and engine flags.`,
        { target_agent: "creative_director" }
      );

      const newCreative = {
        id: Date.now().toString(),
        title: conceptPrompt,
        format: `${aspect} Format`,
        style: style,
        prompt: res.response,
        aspect: aspect,
      };

      setCreatives([newCreative, ...creatives]);
      setConceptPrompt("");
    } catch (err: any) {
      alert(`Creative Director error: ${err.message}. Ensure an AI Provider key is configured.`);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Page Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-600/20 text-pink-400 border border-pink-500/30">
            <Palette className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Creative Studio</h1>
            <p className="text-xs text-slate-400">Visual design concepts, AI image prompts, and ad creative briefs</p>
          </div>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Form: Concept Generator */}
        <div className="w-96 shrink-0 border-r border-slate-800 bg-slate-950/40 p-6 overflow-y-auto">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Generate Creative Brief
          </h2>

          <form onSubmit={handleGenerate} className="mt-4 space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-300">Creative Concept / Topic</label>
              <textarea
                rows={4}
                required
                value={conceptPrompt}
                onChange={(e) => setConceptPrompt(e.target.value)}
                placeholder="e.g. Visualizing an AI marketing department running 24/7 on autopilot with sleek glowing monitors and graphs..."
                className="mt-1.5 w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300">Visual Style</label>
              <select
                value={style}
                onChange={(e) => setStyle(e.target.value)}
                className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-900/90 px-3.5 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
              >
                <option value="Minimalist Modern SaaS">Minimalist Modern SaaS</option>
                <option value="Hyper-Realistic Editorial Photography">Hyper-Realistic Editorial Photography</option>
                <option value="Cinematic Isometric 3D Render">Cinematic Isometric 3D Render</option>
                <option value="Vibrant High-Contrast YouTube Style">Vibrant High-Contrast YouTube Style</option>
                <option value="Luxury Glassmorphism & Abstract">Luxury Glassmorphism & Abstract</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300">Format & Aspect Ratio</label>
              <div className="mt-1.5 grid grid-cols-3 gap-2">
                {[
                  { id: "1:1", label: "Square (1:1)" },
                  { id: "16:9", label: "Banner (16:9)" },
                  { id: "9:16", label: "Story (9:16)" },
                ].map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => setAspect(item.id)}
                    className={`rounded-lg border py-2 text-center text-xs font-medium transition ${
                      aspect === item.id
                        ? "border-blue-500 bg-blue-600/20 text-blue-400"
                        : "border-slate-800 bg-slate-900/60 text-slate-400 hover:text-white"
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            <button
              type="submit"
              disabled={generating || !conceptPrompt.trim()}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 py-2.5 text-xs font-semibold text-white shadow-lg shadow-blue-500/20 transition hover:bg-blue-500 disabled:opacity-50"
            >
              <Sparkles className="h-4 w-4" />
              {generating ? "Crafting Brief..." : "Synthesize Visual Brief"}
            </button>
          </form>
        </div>

        {/* Right Gallery: Creative Briefs */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
          <div className="max-w-4xl space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-white">Production Visual Prompts & Assets</h2>
              <span className="text-xs text-slate-400">{creatives.length} Concepts Generated</span>
            </div>

            <div className="space-y-4">
              {creatives.map((c) => (
                <div
                  key={c.id}
                  className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg transition hover:border-slate-700"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] font-semibold text-slate-300">
                          {c.format}
                        </span>
                        <span className="rounded bg-pink-500/10 px-2 py-0.5 text-[10px] font-semibold text-pink-400 border border-pink-500/20">
                          {c.style}
                        </span>
                      </div>
                      <h3 className="mt-2 text-sm font-semibold text-white">{c.title}</h3>
                    </div>

                    <button
                      onClick={() => handleCopy(c.id, c.prompt)}
                      className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800 px-2.5 py-1 text-xs text-slate-300 transition hover:bg-slate-700 hover:text-white"
                    >
                      {copiedId === c.id ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-emerald-400" />
                          <span className="text-emerald-400">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="h-3.5 w-3.5" />
                          <span>Copy Prompt</span>
                        </>
                      )}
                    </button>
                  </div>

                  <div className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-4">
                    <p className="text-xs leading-relaxed text-slate-300 whitespace-pre-wrap font-mono">
                      {c.prompt}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

