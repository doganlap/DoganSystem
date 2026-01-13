import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import TenantsPage from './pages/TenantsPage';
import AgentsPage from './pages/AgentsPage';
import MonitoringPage from './pages/MonitoringPage';
import ERPNextPage from './pages/ERPNextPage';
import SubscriptionsPage from './pages/SubscriptionsPage';
import HomePage from './pages/HomePage';

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  const { i18n } = useTranslation();
  const [currentTenantId, setCurrentTenantId] = useState('default');

  // Update HTML dir attribute when language changes
  React.useEffect(() => {
    document.documentElement.dir = i18n.language === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = i18n.language;
  }, [i18n.language]);

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />

          {/* Protected routes with layout */}
          <Route
            path="/app/*"
            element={
              <Layout currentTenantId={currentTenantId} setCurrentTenantId={setCurrentTenantId}>
                <Routes>
                  <Route path="dashboard" element={<Dashboard tenantId={currentTenantId} />} />
                  <Route path="tenants" element={<TenantsPage />} />
                  <Route path="agents" element={<AgentsPage tenantId={currentTenantId} />} />
                  <Route path="monitoring" element={<MonitoringPage />} />
                  <Route path="erpnext" element={<ERPNextPage tenantId={currentTenantId} />} />
                  <Route path="subscriptions" element={<SubscriptionsPage tenantId={currentTenantId} />} />
                  <Route path="*" element={<Navigate to="/app/dashboard" replace />} />
                </Routes>
              </Layout>
            }
          />

          {/* Fallback route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
