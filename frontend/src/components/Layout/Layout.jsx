import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = ({ children, currentTenantId, setCurrentTenantId }) => {
  const { i18n } = useTranslation();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const isRTL = i18n.language === 'ar';

  return (
    <div className={`flex h-screen bg-gray-100 ${isRTL ? 'rtl' : 'ltr'}`}>
      {/* Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        isRTL={isRTL}
      />

      {/* Main Content */}
      <div className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ${
        sidebarOpen ? (isRTL ? 'mr-64' : 'ml-64') : (isRTL ? 'mr-16' : 'ml-16')
      }`}>
        {/* Header */}
        <Header
          currentTenantId={currentTenantId}
          setCurrentTenantId={setCurrentTenantId}
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
          isRTL={isRTL}
        />

        {/* Page Content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
