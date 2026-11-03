"use client";

import React, { useState, useEffect } from "react";
import {
  Inbox as InboxIcon,
  Send,
  Sparkles,
  UserPlus,
  CheckCircle2,
  Clock,
  Instagram,
  Linkedin,
  Twitter,
  Globe,
  Bot,
  AlertTriangle,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

const platformIcons: Record<string, any> = {
  instagram: Instagram,
  linkedin: Linkedin,
  twitter: Twitter,
};

const sampleConversations = [
  {
    id: "c1",
    platform: "instagram",
    contact_name: "Marcus Vance",
    contact_username: "@marcus_vance",
    conversation_type: "comment",
    status: "open",
    sentiment: "positive",
    classification: "purchase_intent",
    last_message_at: "10 mins ago",
    messages: [
      {
        id: "m1",
        direction: "inbound",
        sender_type: "contact",
        body: "Hey! Loved your post on executive scaling. How much is the 90-day accelerator and do you have slots open for November?",
        created_at: "10 mins ago",
      },
    ],
  },
  {
    id: "c2",
    platform: "linkedin",
    contact_name: "Elena Rostova",
    contact_username: "Elena Rostova (VP Growth)",
    conversation_type: "dm",
    status: "open",
    sentiment: "neutral",
    classification: "inquiry",
    last_message_at: "1 hour ago",
    messages: [
      {
        id: "m2",
        direction: "inbound",
        sender_type: "contact",
        body: "Do you offer tailored team workshops for B2B tech companies or strictly 1-on-1 coaching?",
        created_at: "1 hour ago",
      },
    ],
  },
  {
    id: "c3",
    platform: "twitter",
    contact_name: "Devon Miller",
    contact_username: "@devon_m",
    conversation_type: "mention",
    status: "replied",
    sentiment: "positive",
    classification: "praise",
    last_message_at: "Yesterday",
    messages: [
      {
        id: "m3",
        direction: "inbound",
        sender_type: "contact",
        body: "Your inbound marketing blueprint is the most practical guide I've read all year. Kudos!",
        created_at: "Yesterday",
      },
    ],
  },
];

export default function UnifiedInboxPage() {
  const [conversations, setConversations] = useState<any[]>(sampleConversations);
  const [selectedConv, setSelectedConv] = useState<any | null>(sampleConversations[0]);
  const [replyText, setReplyText] = useState("");
  const [suggesting, setSuggesting] = useState(false);
  const [suggestion, setSuggestion] = useState<any | null>(null);

  const handleSelect = (conv: any) => {
    setSelectedConv(conv);
    setSuggestion(null);
    setReplyText("");
  };

  const handleSuggestReply = async () => {
    if (!selectedConv) return;
    setSuggesting(true);
    try {
      const res = await api.chatWithAgent(
        `You are the Community Manager. Draft a warm, concise, brand-aligned reply to this customer interaction:\nContact: ${selectedConv.contact_name}\nPlatform: ${selectedConv.platform}\nMessage: "${selectedConv.messages[selectedConv.messages.length - 1]?.body}"\nProvide only the exact reply text ready to send.`,
        { target_agent: "community_manager" }
      );
      setSuggestion({ reply: res.response });
      setReplyText(res.response);
    } catch (err: any) {
      alert(`Community Manager error: ${err.message}. Please configure an AI Provider in Settings.`);
    } finally {
      setSuggesting(false);
    }
  };

  const handleSendReply = (e: React.FormEvent) => {
    e.preventDefault();
    if (!replyText.trim() || !selectedConv) return;

    const newMsg = {
      id: Date.now().toString(),
      direction: "outbound",
      sender_type: "user",
      body: replyText,
      created_at: "Just now",
    };

    const updated = {
      ...selectedConv,
      status: "replied",
      messages: [...selectedConv.messages, newMsg],
    };

    setSelectedConv(updated);
    setConversations((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
    setReplyText("");
    setSuggestion(null);
  };

  const handleCreateLead = async () => {
    if (!selectedConv) return;
    try {
      await api.createLead({
        name: selectedConv.contact_name,
        source: selectedConv.platform,
        status: "new",
        score: selectedConv.classification === "purchase_intent" ? 85 : 50,
        notes: `Captured from inbox interaction: "${selectedConv.messages[0]?.body}"`,
      });
      alert(`Lead for ${selectedConv.contact_name} created successfully in CRM!`);
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-600/20 text-violet-400 border border-violet-500/30">
            <InboxIcon className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Unified Inbox</h1>
            <p className="text-xs text-slate-400">Social conversations, AI suggested replies, and lead detection</p>
          </div>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Left: Conversation List */}
        <div className="w-80 shrink-0 border-r border-slate-800 bg-slate-950/40 p-3 overflow-y-auto space-y-2">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 px-2 py-1">
            Incoming Messages ({conversations.length})
          </div>

          {conversations.map((conv) => {
            const isSelected = selectedConv?.id === conv.id;
            const Icon = platformIcons[conv.platform] || Globe;

            return (
              <div
                key={conv.id}
                onClick={() => handleSelect(conv)}
                className={`cursor-pointer rounded-xl border p-3 transition ${
                  isSelected
                    ? "border-blue-500/50 bg-blue-600/10 shadow-lg shadow-blue-600/10"
                    : "border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5 font-semibold text-xs text-white">
                    <Icon className="h-3 w-3 text-slate-400" />
                    <span>{conv.contact_name}</span>
                  </div>
                  <span className="text-[10px] text-slate-400">{conv.last_message_at}</span>
                </div>

                <p className="mt-1.5 text-xs text-slate-300 line-clamp-2">
                  {conv.messages[conv.messages.length - 1]?.body}
                </p>

                <div className="mt-2.5 flex items-center justify-between border-t border-slate-800/60 pt-2">
                  <span
                    className={`rounded px-1.5 py-0.5 text-[9px] font-semibold uppercase ${
                      conv.classification === "purchase_intent"
                        ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                        : "bg-slate-800 text-slate-400"
                    }`}
                  >
                    {conv.classification?.replace("_", " ")}
                  </span>
                  <span className="text-[10px] text-slate-400 capitalize">{conv.status}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Center: Message Thread */}
        <div className="flex flex-1 flex-col justify-between bg-slate-900/30 overflow-hidden">
          {selectedConv ? (
            <>
              {/* Thread Header */}
              <div className="flex h-14 items-center justify-between border-b border-slate-800 bg-slate-950/60 px-6">
                <div>
                  <h3 className="text-xs font-semibold text-white">{selectedConv.contact_name}</h3>
                  <p className="text-[11px] text-slate-400">{selectedConv.contact_username}</p>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={handleCreateLead}
                    className="flex items-center gap-1.5 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-400 hover:bg-emerald-500/20 transition"
                  >
                    <UserPlus className="h-3.5 w-3.5" />
                    Convert to Lead
                  </button>
                </div>
              </div>

              {/* Message History */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {selectedConv.messages.map((m: any, i: number) => (
                  <div
                    key={i}
                    className={`flex flex-col ${
                      m.direction === "outbound" ? "items-end" : "items-start"
                    }`}
                  >
                    <span className="mb-1 text-[10px] text-slate-400">
                      {m.direction === "outbound" ? "You" : selectedConv.contact_name} &bull; {m.created_at}
                    </span>
                    <div
                      className={`max-w-xl rounded-2xl px-4 py-2.5 text-xs leading-relaxed whitespace-pre-wrap ${
                        m.direction === "outbound"
                          ? "bg-blue-600 text-white rounded-tr-none"
                          : "border border-slate-800 bg-slate-900 text-slate-200 rounded-tl-none"
                      }`}
                    >
                      {m.body}
                    </div>
                  </div>
                ))}
              </div>

              {/* Reply Section */}
              <div className="border-t border-slate-800 bg-slate-950/80 p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-slate-400">Community Manager Assistant</span>
                  <button
                    onClick={handleSuggestReply}
                    disabled={suggesting}
                    className="flex items-center gap-1.5 rounded-lg border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-xs font-semibold text-purple-400 hover:bg-purple-500/20 transition disabled:opacity-50"
                  >
                    <Sparkles className="h-3.5 w-3.5" />
                    {suggesting ? "Thinking..." : "AI Suggest Reply"}
                  </button>
                </div>

                <form onSubmit={handleSendReply} className="flex gap-2">
                  <input
                    type="text"
                    value={replyText}
                    onChange={(e) => setReplyText(e.target.value)}
                    placeholder="Type your response or click 'AI Suggest Reply'..."
                    className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-2 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
                  />
                  <button
                    type="submit"
                    className="flex items-center gap-1.5 rounded-xl bg-blue-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-blue-500"
                  >
                    <Send className="h-3.5 w-3.5" />
                    Send
                  </button>
                </form>
              </div>
            </>
          ) : (
            <div className="flex h-full items-center justify-center text-xs text-slate-400">
              Select a conversation to inspect messages
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
