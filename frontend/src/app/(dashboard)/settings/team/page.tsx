"use client";

import React, { useState, useEffect } from "react";
import {
  Layers,
  UserPlus,
  Shield,
  CheckCircle2,
  Trash2,
  Plus,
} from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function TeamSettingsPage() {
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [members, setMembers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Invite modal
  const [isInviting, setIsInviting] = useState(false);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("editor");

  // New Workspace modal
  const [isCreatingWs, setIsCreatingWs] = useState(false);
  const [newWsName, setNewWsName] = useState("");
  const [newWsDesc, setNewWsDesc] = useState("");

  const loadData = async () => {
    setLoading(true);
    try {
      const wsList = await api.getWorkspaces();
      setWorkspaces(wsList);
      if (wsList.length > 0) {
        const currentWsId = api.getWorkspaceId() || wsList[0].id;
        const m = await api.getWorkspaceMembers(currentWsId);
        setMembers(m);
      }
    } catch {
      // fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    const currentWsId = api.getWorkspaceId();
    if (!currentWsId) return;

    try {
      await api.request(`/workspaces/${currentWsId}/members`, {
        method: "POST",
        body: JSON.stringify({ email: inviteEmail, role: inviteRole }),
      });
      setIsInviting(false);
      setInviteEmail("");
      await loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createWorkspace(newWsName, newWsDesc);
      setIsCreatingWs(false);
      setNewWsName("");
      setNewWsDesc("");
      await loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950/80 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
            <Layers className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Team & Workspaces</h1>
            <p className="text-xs text-slate-400">Multi-tenant client accounts, role-based access, and invitations</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsCreatingWs(true)}
            className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white hover:bg-slate-700 transition"
          >
            <Plus className="h-4 w-4" />
            New Client Workspace
          </button>
          <button
            onClick={() => setIsInviting(true)}
            className="flex items-center gap-1.5 rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-blue-500 transition shadow-md shadow-blue-500/20"
          >
            <UserPlus className="h-4 w-4" />
            Invite Member
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 bg-slate-900/30">
        <div className="mx-auto max-w-4xl space-y-6">
          {/* Workspaces list */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h2 className="text-sm font-semibold text-white">Client Workspaces ({workspaces.length})</h2>
            <p className="mt-1 text-xs text-slate-400">
              Each workspace features an isolated Brand Brain, separate social integrations, and dedicated agent memory.
            </p>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              {workspaces.map((ws) => (
                <div
                  key={ws.id}
                  className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 transition hover:border-slate-700"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-xs font-semibold text-white">{ws.name}</h3>
                      <p className="mt-1 text-[11px] text-slate-400">
                        {ws.description || "Production marketing workspace"}
                      </p>
                    </div>
                    <span className="rounded bg-blue-500/20 px-2 py-0.5 text-[9px] font-semibold text-blue-400 border border-blue-500/30">
                      Active
                    </span>
                  </div>
                  <div className="mt-3 flex items-center justify-between text-[10px] text-slate-400 border-t border-slate-800/60 pt-2">
                    <span>Slug: /{ws.slug}</span>
                    <span>Created {formatDate(ws.created_at)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Members list */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-xl">
            <h2 className="text-sm font-semibold text-white">Workspace Members ({members.length})</h2>
            <div className="mt-4 divide-y divide-slate-800/80">
              {members.map((member) => (
                <div key={member.id} className="flex items-center justify-between py-3">
                  <div>
                    <p className="text-xs font-semibold text-white">
                      {member.user_name || "Team Member"}
                    </p>
                    <p className="text-[11px] text-slate-400">{member.user_email || "Member"}</p>
                  </div>

                  <span className="rounded bg-slate-800 px-2.5 py-1 text-xs font-semibold text-slate-300 capitalize">
                    {member.role}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Invite Member Modal */}
      {isInviting && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <h2 className="text-base font-semibold text-white">Invite Team Member</h2>
            <p className="mt-1 text-xs text-slate-400">Grant access to this marketing workspace.</p>

            <form onSubmit={handleInvite} className="mt-5 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300">Email Address</label>
                <input
                  type="email"
                  required
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  placeholder="colleague@agency.com"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Workspace Role</label>
                <select
                  value={inviteRole}
                  onChange={(e) => setInviteRole(e.target.value)}
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                >
                  <option value="admin">Admin (Full Control)</option>
                  <option value="editor">Editor (Create, Edit & Approve)</option>
                  <option value="viewer">Viewer (Read-only)</option>
                </select>
              </div>

              <div className="mt-6 flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsInviting(false)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-500"
                >
                  Send Invite
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* New Workspace Modal */}
      {isCreatingWs && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
            <h2 className="text-base font-semibold text-white">Create Client Workspace</h2>
            <p className="mt-1 text-xs text-slate-400">Separate data isolation for multi-client agency operations.</p>

            <form onSubmit={handleCreateWorkspace} className="mt-5 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300">Client / Workspace Name</label>
                <input
                  type="text"
                  required
                  value={newWsName}
                  onChange={(e) => setNewWsName(e.target.value)}
                  placeholder="Acme Corp Marketing"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300">Description</label>
                <input
                  type="text"
                  value={newWsDesc}
                  onChange={(e) => setNewWsDesc(e.target.value)}
                  placeholder="Inbound lead gen and social engine"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="mt-6 flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsCreatingWs(false)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-500"
                >
                  Create Workspace
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
