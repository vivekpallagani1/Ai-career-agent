import React from 'react';
import { useAuthStore } from '../store/auth';

export default function Dashboard() {
  const { user } = useAuthStore();

  return (
    <div className="space-y-8">
      <section className="space-y-4">
        <div className="flex justify-between items-center">
          <h1 className="text-4xl font-bold">Dashboard</h1>
        </div>
        <p className="text-slate-400">Welcome back, {user?.name || 'Career Seeker'}!</p>
      </section>

      <section className="grid gap-6 grid-cols-1 md:grid-cols-5">
        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
          <div className="text-sm text-slate-400">Career Readiness</div>
          <div className="mt-4 flex items-center justify-between">
            <div className="text-3xl font-bold text-white">86%</div>
            <div className="w-16 h-16 rounded-full bg-gradient-to-b from-sky-500 to-cyan-500 flex items-center justify-center text-sm font-bold text-slate-950">
              86%
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
          <div className="text-sm text-slate-400">Profile Completeness</div>
          <div className="mt-4 text-3xl font-bold text-white">72%</div>
        </div>

        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
          <div className="text-sm text-slate-400">New Jobs</div>
          <div className="mt-4 text-3xl font-bold text-white">24</div>
        </div>

        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
          <div className="text-sm text-slate-400">High Match Jobs</div>
          <div className="mt-4 text-3xl font-bold text-emerald-400">18</div>
        </div>

        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
          <div className="text-sm text-slate-400">Applications</div>
          <div className="mt-4 text-3xl font-bold text-white">12</div>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Recommended Jobs</h2>
        <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="rounded-2xl border border-slate-700 bg-slate-800 p-5 hover:border-sky-500 transition">
              <h3 className="font-bold text-lg text-white">Senior Engineer</h3>
              <p className="text-sm text-slate-300 mt-1">TechCorp Inc.</p>
              <p className="text-xs text-slate-400 mt-2">San Francisco, CA</p>
              <div className="flex gap-2 mt-4">
                <span className="inline-block rounded-full bg-emerald-500/20 text-emerald-300 px-3 py-1 text-xs font-semibold">
                  92% Match
                </span>
                <span className="inline-block rounded-full bg-emerald-500/20 text-emerald-300 px-3 py-1 text-xs font-semibold">
                  Low Risk
                </span>
              </div>
              <button className="mt-4 w-full rounded-lg bg-sky-500 px-4 py-2 font-semibold text-slate-950 hover:bg-sky-600">
                View Details
              </button>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Recent Activity</h2>
        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6 space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="border-b border-slate-700 pb-4 last:border-b-0">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-white font-medium">Viewed Senior Engineer role at TechCorp</p>
                  <p className="text-xs text-slate-400 mt-1">2 hours ago</p>
                </div>
                <span className="text-xs bg-slate-700 px-2 py-1 rounded text-slate-300">Viewed</span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
