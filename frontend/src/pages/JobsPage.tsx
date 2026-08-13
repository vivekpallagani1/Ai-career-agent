import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';

export default function JobsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLocation, setFilterLocation] = useState('');

  const { data: jobs = [], isLoading } = useQuery({
    queryKey: ['jobs', searchTerm, filterLocation],
    queryFn: async () => {
      if (searchTerm || filterLocation) {
        return api.searchJobs(searchTerm, undefined, filterLocation);
      }
      return api.getJobs();
    },
  });

  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-4xl font-bold mb-6">Job Discovery</h1>

        <div className="grid gap-4 grid-cols-1 md:grid-cols-3 mb-8">
          <input
            type="text"
            placeholder="Search by role..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
          <input
            type="text"
            placeholder="Filter by location..."
            value={filterLocation}
            onChange={(e) => setFilterLocation(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
          <select className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white focus:outline-none focus:border-sky-500">
            <option>Sort by Best Match</option>
            <option>Sort by Newest</option>
            <option>Sort by Salary</option>
          </select>
        </div>
      </section>

      {isLoading && <div className="text-center text-slate-400">Loading jobs...</div>}

      <section className="grid gap-4 grid-cols-1 md:grid-cols-2">
        {jobs && jobs.length > 0 ? (
          jobs.map((job: any) => (
            <div key={job.id} className="rounded-2xl border border-slate-700 bg-slate-800 p-6 hover:border-sky-500 transition">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-bold text-white">{job.title}</h3>
                  <p className="text-sm text-slate-300 mt-1">{job.company}</p>
                </div>
                <span className="inline-block rounded-full bg-sky-500/20 text-sky-300 px-3 py-1 text-xs font-semibold">
                  New
                </span>
              </div>

              <div className="space-y-2 text-sm text-slate-400 mb-4">
                <p>📍 {job.location || 'Remote'}</p>
                {job.salary_min && job.salary_max && (
                  <p>💰 ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}</p>
                )}
                <p>{job.employment_type || 'Full-time'}</p>
              </div>

              <div className="flex gap-2 mb-6">
                {job.fraud_score < 30 && (
                  <span className="inline-block rounded-full bg-emerald-500/20 text-emerald-300 px-3 py-1 text-xs font-semibold">
                    Low Risk
                  </span>
                )}
                {job.fraud_score >= 30 && job.fraud_score < 70 && (
                  <span className="inline-block rounded-full bg-yellow-500/20 text-yellow-300 px-3 py-1 text-xs font-semibold">
                    Medium Risk
                  </span>
                )}
                {job.fraud_score >= 70 && (
                  <span className="inline-block rounded-full bg-red-500/20 text-red-300 px-3 py-1 text-xs font-semibold">
                    High Risk
                  </span>
                )}
              </div>

              <button className="w-full rounded-lg bg-sky-500 px-4 py-2 font-semibold text-slate-950 hover:bg-sky-600 transition">
                View Details & Match
              </button>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center text-slate-400 py-12">
            {searchTerm || filterLocation ? 'No jobs found matching your filters.' : 'No jobs available yet.'}
          </div>
        )}
      </section>
    </div>
  );
}
