"use client";

import { useRouter } from "next/navigation";

export default function LandingPage() {
  const router = useRouter();

  return (
    <div className="flex min-h-screen flex-col items-center justify-between bg-slate-950 px-6 pb-12 pt-12">

      {/* Top Logo */}
      <div className="flex items-center gap-3 self-start">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-600 text-xl">
          🚑
        </div>
        <span className="text-xl font-extrabold tracking-tight text-white">
          Save<span className="text-red-500">Pulse</span>
        </span>
      </div>

      {/* Center Content */}
      <div className="flex w-full max-w-sm flex-col items-center gap-8">

        {/* Hero Card */}
        <section className="w-full rounded-3xl bg-gradient-to-br from-red-600 to-red-500 p-8 text-center text-white shadow-2xl shadow-red-900/40">
          <p className="text-[11px] font-semibold uppercase tracking-[0.2em] opacity-80">
            Emergency Service
          </p>
          <h1 className="mt-2 text-4xl font-extrabold tracking-tight">SavePulse</h1>
          <p className="mt-2 text-sm opacity-90 leading-relaxed">
            Fast ambulance dispatch &amp; intelligent hospital matching.
          </p>
        </section>

        {/* Emergency Ready Badge */}
        <div className="relative flex h-32 w-32 items-center justify-center">
          <div className="absolute inset-0 rounded-full bg-red-600/20 blur-2xl" />
          <div className="relative flex h-28 w-28 flex-col items-center justify-center rounded-full bg-red-600 shadow-lg shadow-red-600/50">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-9 w-9 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.8}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"
              />
            </svg>
            <span className="mt-1 text-[9px] font-bold uppercase tracking-widest text-white/90">
              Emergency Ready
            </span>
          </div>
        </div>

        <p className="text-center text-sm text-slate-400 leading-relaxed max-w-xs">
          Your life-saving companion is just a tap away. Professional medical
          assistance available 24/7.
        </p>

        {/* CTA Buttons */}
        <div className="flex w-full flex-col gap-3">
          <button
            onClick={() => router.push("/signup")}
            className="w-full rounded-2xl bg-red-600 py-4 text-base font-bold text-white shadow-lg shadow-red-600/30 transition-all duration-200 hover:bg-red-500 active:scale-95"
          >
            Sign Up
          </button>
          <button
            onClick={() => router.push("/login")}
            className="w-full rounded-2xl border border-slate-700 bg-slate-900 py-4 text-base font-bold text-white transition-all duration-200 hover:bg-slate-800 active:scale-95"
          >
            Log In
          </button>
        </div>
      </div>

      {/* Bottom Spacer */}
      <div />
    </div>
  );
}