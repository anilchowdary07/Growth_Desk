import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI GrowthDesk — Autonomous AI Marketing Workforce",
  description: "An autonomous AI marketing department that researches, plans, creates, executes, and optimizes marketing campaigns.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        {children}
      </body>
    </html>
  );
}
