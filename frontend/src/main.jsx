import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './index.css';

import { useAuthStore } from './store/auth';
import AppLayout from './layouts/AppLayout';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import JobsPage from './pages/JobsPage';

const queryClient = new QueryClient();

function App() {
  const { isAuthenticated, loadFromStorage } = useAuthStore();

  useEffect(() => {
    loadFromStorage();
  }, []);

  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route
            path="/dashboard"
            element={
              isAuthenticated ? (
                <AppLayout>
                  <Dashboard />
                </AppLayout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          <Route
            path="/jobs"
            element={
              isAuthenticated ? (
                <AppLayout>
                  <JobsPage />
                </AppLayout>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          <Route path="/" element={<Navigate to={isAuthenticated ? '/dashboard' : '/login'} replace />} />
        </Routes>
      </QueryClientProvider>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
