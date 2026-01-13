import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  LayoutDashboard,
  Building2,
  Users,
  Activity,
  Server,
  CreditCard,
  Menu,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';

const Sidebar = ({ isOpen, onToggle, isRTL }) => {
  const { t } = useTranslation();
  const location = useLocation();

  const menuItems = [
    {
      path: '/app/dashboard',
      icon: LayoutDashboard,
      label: t('dashboard', 'لوحة التحكم'),
      labelEn: 'Dashboard',
    },
    {
      path: '/app/tenants',
      icon: Building2,
      label: t('tenants', 'المستأجرون'),
      labelEn: 'Tenants',
    },
    {
      path: '/app/agents',
      icon: Users,
      label: t('agents', 'الوكلاء'),
      labelEn: 'Agents',
    },
    {
      path: '/app/erpnext',
      icon: Server,
      label: t('erpnext', 'ERPNext'),
      labelEn: 'ERPNext',
    },
    {
      path: '/app/subscriptions',
      icon: CreditCard,
      label: t('subscriptions', 'الاشتراكات'),
      labelEn: 'Subscriptions',
    },
    {
      path: '/app/monitoring',
      icon: Activity,
      label: t('monitoring', 'المراقبة'),
      labelEn: 'Monitoring',
    },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div
      className={`fixed ${isRTL ? 'right-0' : 'left-0'} top-0 h-full bg-gradient-to-b from-indigo-800 to-indigo-900 text-white transition-all duration-300 z-40 ${
        isOpen ? 'w-64' : 'w-16'
      }`}
    >
      {/* Logo & Toggle */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-indigo-700">
        {isOpen && (
          <div className="flex items-center gap-2">
            <Server className="w-8 h-8 text-indigo-300" />
            <span className="text-xl font-bold">DoganSystem</span>
          </div>
        )}
        <button
          onClick={onToggle}
          className="p-2 rounded-lg hover:bg-indigo-700 transition-colors"
        >
          {isOpen ? (
            isRTL ? <ChevronRight size={20} /> : <ChevronLeft size={20} />
          ) : (
            <Menu size={20} />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="mt-6 px-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-4 px-4 py-3 mb-2 rounded-lg transition-all ${
                isActive(item.path)
                  ? 'bg-indigo-700 text-white shadow-lg'
                  : 'text-indigo-200 hover:bg-indigo-700/50 hover:text-white'
              } ${!isOpen && 'justify-center'}`}
              title={!isOpen ? (isRTL ? item.label : item.labelEn) : ''}
            >
              <Icon size={20} className="flex-shrink-0" />
              {isOpen && (
                <span className="font-medium">{isRTL ? item.label : item.labelEn}</span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      {isOpen && (
        <div className="absolute bottom-4 left-0 right-0 px-4">
          <div className="p-4 bg-indigo-700/50 rounded-lg text-sm">
            <p className="font-semibold mb-1">{t('version', 'الإصدار')}</p>
            <p className="text-indigo-300">v1.0.0</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
