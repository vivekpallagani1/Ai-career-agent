import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6 space-y-6">
        <div className="text-xl font-bold text-sky-400">AI Career Agent</div>

        <nav className="space-y-2">
          {['Dashboard', 'Jobs', 'Resume', 'Applications', 'Career', 'Analytics'].map((item) => (
            <a
              key={item}
              href={`/${item.toLowerCase()}`}
              className="block px-4 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              {item}
            </a>
          ))}
        </nav>

        <div className="border-t border-slate-800 pt-4 mt-auto">
          <div className="text-xs text-slate-500">{user?.email}</div>
          <button
            onClick={() => {
              useAuthStore.getState().logout();
              window.location.href = '/';
            }}
            className="mt-3 w-full rounded-lg bg-slate-800 px-3 py-2 text-sm font-semibold text-slate-300 hover:text-white hover:bg-slate-700 transition"
          >
            Logout
          </button>
        </div>
      </aside>

      <main className="flex-1 bg-slate-950 p-8">
        <div className="max-w-6xl">{children}</div>
      </main>
    </div>
  );
}
