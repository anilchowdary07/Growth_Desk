"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("gd_access_token");
    if (token) {
      router.push("/director");
    } else {
      router.push("/login");
    }
  }, [router]);

  return (
    <div className="flex h-screen items-center justify-center bg-slate-950 text-white">
      <div className="flex flex-col items-center gap-4">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
        <p className="text-sm text-slate-400">Loading AI GrowthDesk command center...</p>
      </div>
    </div>
  );
}
