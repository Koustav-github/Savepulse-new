"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Header from "@/components/Header";
import BottomNav from "@/components/BottomNav";

export default function UserLogin() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const res = await fetch("http://localhost:3001/user/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include", // send/receive cookies
                body: JSON.stringify({ email }),
            });

            const data = await res.json();

            if (res.ok) {
                router.push("/User");
            } else {
                setError(data.message ?? "Login failed. Please try again.");
            }
        } catch {
            setError("Unable to connect to server. Check your connection.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="flex min-h-screen flex-col bg-slate-950">
            <Header />

            <main className="mx-auto w-full max-w-md flex-1 px-4 pt-6 pb-24">

                {/* Hero */}
                <section className="rounded-3xl bg-gradient-to-br from-red-600 to-red-500 p-6 text-white shadow-lg">
                    <p className="text-sm uppercase tracking-widest opacity-80 font-medium">User</p>
                    <h1 className="mt-1 text-3xl font-extrabold">Welcome Back</h1>
                    <p className="mt-1 text-sm opacity-90">
                        Sign in with your registered email to access emergency services.
                    </p>
                </section>

                {/* Login Form */}
                <form
                    onSubmit={handleSubmit}
                    className="mt-6 space-y-5 rounded-3xl bg-slate-900 p-6 shadow-lg border border-slate-800"
                >
                    {/* Error Banner */}
                    {error && (
                        <div className="rounded-xl bg-red-600/10 border border-red-600/30 px-4 py-3 text-sm text-red-400">
                            {error}
                        </div>
                    )}

                    {/* Email */}
                    <div>
                        <label className="text-sm font-medium text-slate-300">
                            Email Address
                        </label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            autoComplete="email"
                            className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-white placeholder-slate-500 outline-none transition focus:border-red-500 focus:ring-1 focus:ring-red-500"
                            placeholder="you@email.com"
                        />
                    </div>

                    {/* Info Note */}
                    <p className="text-xs text-slate-500">
                        💡 We use email-based sign-in — no password needed. Your account
                        is tied to the email you registered with.
                    </p>

                    {/* Submit */}
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full rounded-xl bg-red-600 py-3.5 text-sm font-bold text-white shadow-lg shadow-red-600/20 transition-all duration-200 hover:bg-red-500 active:scale-95 ${loading ? "cursor-not-allowed opacity-60" : ""
                            }`}
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-2">
                                <svg
                                    className="h-4 w-4 animate-spin"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                >
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                                </svg>
                                Signing in…
                            </span>
                        ) : (
                            "Log In"
                        )}
                    </button>

                    {/* Switch to Signup */}
                    <p className="text-center text-sm text-slate-500">
                        New to SavePulse?{" "}
                        <button
                            type="button"
                            onClick={() => router.push("/userSignup")}
                            className="font-semibold text-red-500 hover:text-red-400 transition-colors"
                        >
                            Create an account
                        </button>
                    </p>
                </form>
            </main>

            <BottomNav />
        </div>
    );
}
