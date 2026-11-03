"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Bot,
  Send,
  Sparkles,
  TrendingUp,
  Target,
  FileText,
  UserCheck,
  CheckCircle2,
  RefreshCw,
  Lightbulb,
} from "lucide-react";
import { api } from "@/lib/api";

const specialistOptions = [
  { id: "director", name: "AI Marketing Director", role: "Workforce Coordinator" },
  { id: "research", name: "Market Research Specialist", role: "Trends & Competitors" },
  { id: "brand_strategist", name: "Brand Strategist", role: "Voice & Guidelines" },
  { id: "content_creator", name: "Content Creator", role: "High-Converting Copy" },
  { id: "creative_director", name: "Creative Director", role: "Visuals & Prompts" },
  { id: "social_manager", name: "Social Media Manager", role: "Publishing & Timing" },
  { id: "community_manager", name: "Community Manager", role: "Customer Replies" },
  { id: "lead_agent", name: "Lead Generation Specialist", role: "Qualification & Scoring" },
  { id: "advertising_agent", name: "Advertising Specialist", role: "Paid Campaigns & ROAS" },
  { id: "seo_agent", name: "SEO & Growth Strategist", role: "Search & GEO Engine Visibility" },
  { id: "growth_analyst", name: "Growth Analyst", role: "Data & KPI Recommendations" },
];

const samplePrompts = [
  "Promote my new fitness coaching program and generate 100 qualified leads over the next 30 days.",
  "Audit our brand positioning against top competitors and suggest a differentiated value hook.",
  "Design a 14-day Instagram and LinkedIn campaign for our upcoming B2B software launch.",
  "Identify content gaps in our niche and outline 3 high-intent SEO articles that rank on Perplexity & Google.",
];

export default function DirectorPage() {
  const [messages, setMessages] = useState<
    Array<{ role: "user" | "assistant"; content: string; agent?: string; time?: string }>
  >([
    {
      role: "assistant",
      agent: "AI Marketing Director",
      time: "Just now",
      content:
        "👋 Welcome! I am your **AI Marketing Director**. I lead your autonomous marketing workforce—coordinating research, copy, creative concepts, social scheduling, lead qualification, and performance optimization.\n\nDescribe your business objective or choose a prompt below to get started.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState("director");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (messageText?: string) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = {
      role: "user" as const,
      content: textToSend,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // Build conversation history for context
      const history = messages.slice(-6).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await api.chatWithAgent(textToSend, {
        target_agent: selectedAgent,
        conversation_history: history,
      });

      const assistantMsg = {
        role: "assistant" as const,
        content: res.response,
        agent: specialistOptions.find((s) => s.id === res.agent_name)?.name || "Marketing Specialist",
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          agent: "System Notice",
          content: `⚠️ Note: ${err.message}. If you have not yet added an API key, please visit **Settings → AI Providers (BYOK)** to connect OpenAI, Google Gemini, or Anthropic Claude.`,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Top Header */}
      <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30">
            <Bot className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">AI Marketing Director</h1>
            <p className="text-xs text-slate-400">Autonomous workforce coordinator & strategic planner</p>
          </div>
        </div>

        {/* Specialist Selector */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Direct query to:</span>
          <select
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-1.5 text-xs font-medium text-slate-200 focus:border-blue-500 focus:outline-none"
          >
            {specialistOptions.map((spec) => (
              <option key={spec.id} value={spec.id}>
                {spec.name} ({spec.role})
              </option>
            ))}
          </select>
        </div>
      </header>

      {/* Message Feed */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}
          >
            <div className="mb-1 flex items-center gap-2 text-[11px] text-slate-400">
              {m.role === "assistant" && (
                <span className="inline-flex items-center gap-1 rounded bg-blue-500/10 px-2 py-0.5 font-medium text-blue-400 border border-blue-500/20">
                  <Sparkles className="h-3 w-3" />
                  {m.agent}
                </span>
              )}
              <span>{m.time}</span>
            </div>

            <div
              className={`max-w-2xl rounded-2xl px-5 py-3.5 text-sm leading-relaxed whitespace-pre-wrap ${
                m.role === "user"
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-600/20 rounded-tr-none"
                  : "border border-slate-800 bg-slate-900/90 text-slate-200 shadow-md rounded-tl-none"
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex flex-col items-start">
            <div className="mb-1 flex items-center gap-1.5 text-[11px] text-slate-400">
              <span className="inline-flex items-center gap-1 rounded bg-blue-500/10 px-2 py-0.5 font-medium text-blue-400 border border-blue-500/20">
                <RefreshCw className="h-3 w-3 animate-spin" />
                {specialistOptions.find((s) => s.id === selectedAgent)?.name} analyzing...
              </span>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-md rounded-tl-none">
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 animate-bounce rounded-full bg-blue-500" />
                <div className="h-2 w-2 animate-bounce rounded-full bg-blue-400 [animation-delay:0.2s]" />
                <div className="h-2 w-2 animate-bounce rounded-full bg-blue-300 [animation-delay:0.4s]" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompts (if chat is fresh) */}
      {messages.length <= 3 && (
        <div className="px-6 pb-2">
          <div className="mb-2 flex items-center gap-1.5 text-xs font-medium text-slate-400">
            <Lightbulb className="h-3.5 w-3.5 text-amber-400" />
            Suggested Objectives:
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {samplePrompts.map((prompt, i) => (
              <button
                key={i}
                onClick={() => handleSend(prompt)}
                className="rounded-lg border border-slate-800 bg-slate-900/40 p-2.5 text-left text-xs text-slate-300 transition hover:border-slate-700 hover:bg-slate-900 hover:text-white"
              >
                &ldquo;{prompt}&rdquo;
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Message Input Box */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/90">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="relative flex items-center"
        >
          <textarea
            rows={2}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Instruct the Marketing Director (e.g., 'Plan a 30-day lead generation campaign for my new offering')..."
            className="w-full resize-none rounded-xl border border-slate-700 bg-slate-900/90 py-3 pl-4 pr-14 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-2.5 flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white shadow-md transition hover:bg-blue-500 disabled:opacity-40"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
        <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400 px-1">
          <span>Connected: BYOK Enterprise Engine</span>
          <span>Press Enter to send, Shift+Enter for newline</span>
        </div>
      </div>
    </div>
  );
}
