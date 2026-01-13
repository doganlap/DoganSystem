import React from 'react';
import { useTranslation } from 'react-i18next';
import { Bell, Globe, Menu } from 'lucide-react';
import { useSystemStatus } from '../../hooks/useApi';

const Header = ({ currentTenantId, setCurrentTenantId, onMenuClick, isRTL }) => {
  const { t, i18n } = useTranslation();
  const { data: systemStatus } = useSystemStatus();

  const toggleLanguage = () => {
    const newLang = i18n.language === 'ar' ? 'en' : 'ar';
    i18n.changeLanguage(newLang);
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 h-16 flex items-center justify-between px-6">
      {/* Left Section */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors lg:hidden"
        >
          <Menu size={20} />
        </button>

        {/* Tenant Selector */}
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-gray-700">
            {t('currentTenant', 'المستأجر الحالي')}:
          </label>
          <select
            value={currentTenantId}
            onChange={(e) => setCurrentTenantId(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="default">Default Tenant</option>
            {/* More tenants will be loaded dynamically */}
          </select>
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        {/* System Status */}
        {systemStatus?.data && (
          <div className="flex items-center gap-2 px-3 py-1 bg-green-50 text-green-700 rounded-lg text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span>{t('systemOnline', 'النظام متصل')}</span>
          </div>
        )}

        {/* Language Toggle */}
        <button
          onClick={toggleLanguage}
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          title={t('changeLanguage', 'تغيير اللغة')}
        >
          <Globe size={20} className="text-gray-600" />
          <span className="ml-1 text-sm font-medium text-gray-700">
            {i18n.language === 'ar' ? 'EN' : 'AR'}
          </span>
        </button>

        {/* Notifications */}
        <button
          className="p-2 rounded-lg hover:bg-gray-100 transition-colors relative"
          title={t('notifications', 'الإشعارات')}
        >
          <Bell size={20} className="text-gray-600" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>

        {/* User Menu */}
        <div className="flex items-center gap-2 px-3 py-1 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
          <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white font-semibold">
            A
          </div>
          <span className="text-sm font-medium text-gray-700">Admin</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
