"use client";

import { useRouter } from "next/navigation";
import Header from "@/components/Header";

export default function LoginSelection() {
    const router = useRouter();

    return (
        <div className="flex min-h-screen flex-col bg-slate-950">
            <Header />

            <main className="mx-auto flex w-full max-w-md flex-1 flex-col gap-6 px-4 pb-24 pt-6">

                {/* Hero */}
                <section className="rounded-3xl bg-gradient-to-br from-red-600 to-red-500 p-6 text-white shadow-lg">
                    <p className="text-sm font-medium uppercase tracking-widest opacity-80">
                        Welcome Back
                    </p>
                    <h1 className="mt-1 text-3xl font-extrabold">Log In</h1>
                    <p className="mt-1 text-sm opacity-90">
                        Select your account type to continue.
                    </p>
                </section>

                {/* Selection Cards */}
                <section className="flex flex-col gap-4">

                    {/* User Login */}
                    <button
                        onClick={() => router.push("/userLogin")}
                        className="group flex items-center gap-4 rounded-2xl border border-slate-800 bg-slate-900 p-5 text-left shadow-md transition-all duration-200 hover:border-red-600/50 hover:shadow-red-900/20 hover:shadow-lg active:scale-[0.98]"
                    >
                        <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-red-600/15 text-2xl ring-1 ring-red-600/30 transition-colors group-hover:bg-red-600/25">
                            👤
                        </div>
                        <div>
                            <h2 className="font-bold text-white">Log In as User</h2>
                            <p className="mt-0.5 text-sm text-slate-400">
                                Access your emergency profile and request ambulances.
                            </p>
                        </div>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="ml-auto h-5 w-5 shrink-0 text-slate-600 transition-colors group-hover:text-red-500"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth={2}
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                        </svg>
                    </button>

                    {/* Hospital Login */}
                    <button
                        onClick={() => router.push("/hospitalLogin")}
                        className="group flex items-center gap-4 rounded-2xl border border-slate-800 bg-slate-900 p-5 text-left shadow-md transition-all duration-200 hover:border-red-600/50 hover:shadow-red-900/20 hover:shadow-lg active:scale-[0.98]"
                    >
                        <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-red-600/15 text-2xl ring-1 ring-red-600/30 transition-colors group-hover:bg-red-600/25">
                            🏥
                        </div>
                        <div>
                            <h2 className="font-bold text-white">Log In as Hospital</h2>
                            <p className="mt-0.5 text-sm text-slate-400">
                                Manage incoming emergency dispatch requests.
                            </p>
                        </div>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="ml-auto h-5 w-5 shrink-0 text-slate-600 transition-colors group-hover:text-red-500"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth={2}
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                        </svg>
                    </button>
                </section>

                {/* Don't have an account */}
                <p className="text-center text-sm text-slate-500">
                    Don&apos;t have an account?{" "}
                    <button
                        onClick={() => router.push("/signup")}
                        className="font-semibold text-red-500 hover:text-red-400 transition-colors"
                    >
                        Sign Up
                    </button>
                </p>
            </main>
        </div>
    );
}
