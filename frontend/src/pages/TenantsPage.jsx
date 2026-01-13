import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Building2,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { useTenants } from '../hooks/useApi';
import { tenantApi } from '../services/api';
import { useApiMutation } from '../hooks/useApi';

const TenantsPage = () => {
  const { t, i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);

  const { data: tenantsData, isLoading, error } = useTenants();

  // Mock data for demonstration
  const mockTenants = [
    {
      id: '1',
      name: isRTL ? 'شركة التقنية المتقدمة' : 'Advanced Tech Corp',
      domain: 'advancedtech.dogan.io',
      status: 'active',
      createdAt: '2026-01-01',
      users: 45,
      agents: 12,
    },
    {
      id: '2',
      name: isRTL ? 'مؤسسة الابتكار' : 'Innovation Enterprise',
      domain: 'innovation.dogan.io',
      status: 'active',
      createdAt: '2026-01-05',
      users: 32,
      agents: 8,
    },
    {
      id: '3',
      name: isRTL ? 'شركة الحلول الذكية' : 'Smart Solutions LLC',
      domain: 'smartsolutions.dogan.io',
      status: 'inactive',
      createdAt: '2025-12-20',
      users: 15,
      agents: 5,
    },
  ];

  const tenants = tenantsData?.data || mockTenants;

  const TenantCard = ({ tenant }) => {
    const [showMenu, setShowMenu] = useState(false);

    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
              <Building2 className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{tenant.name}</h3>
              <p className="text-sm text-gray-500">{tenant.domain}</p>
            </div>
          </div>

          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <MoreVertical size={20} className="text-gray-600" />
            </button>

            {showMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10">
                <button className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2">
                  <Eye size={16} />
                  <span>{t('view', 'عرض')}</span>
                </button>
                <button className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2">
                  <Edit size={16} />
                  <span>{t('edit', 'تعديل')}</span>
                </button>
                <button className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2 text-red-600">
                  <Trash2 size={16} />
                  <span>{t('delete', 'حذف')}</span>
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 mb-4">
          {tenant.status === 'active' ? (
            <span className="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
              <CheckCircle size={14} />
              {isRTL ? 'نشط' : 'Active'}
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-medium">
              <XCircle size={14} />
              {isRTL ? 'غير نشط' : 'Inactive'}
            </span>
          )}
        </div>

        <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
          <div>
            <p className="text-xs text-gray-500 mb-1">{isRTL ? 'المستخدمون' : 'Users'}</p>
            <p className="text-lg font-semibold text-gray-900">{tenant.users}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">{isRTL ? 'الوكلاء' : 'Agents'}</p>
            <p className="text-lg font-semibold text-gray-900">{tenant.agents}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">{isRTL ? 'تاريخ الإنشاء' : 'Created'}</p>
            <p className="text-sm font-medium text-gray-900">
              {new Date(tenant.createdAt).toLocaleDateString(isRTL ? 'ar-SA' : 'en-US', {
                month: 'short',
                day: 'numeric',
              })}
            </p>
          </div>
        </div>
      </div>
    );
  };

  const CreateTenantModal = () => {
    const [formData, setFormData] = useState({
      name: '',
      domain: '',
      email: '',
    });

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            {isRTL ? 'إضافة مستأجر جديد' : 'Add New Tenant'}
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isRTL ? 'اسم الشركة' : 'Company Name'}
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder={isRTL ? 'مثال: شركة التقنية' : 'e.g., Tech Corp'}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isRTL ? 'النطاق' : 'Domain'}
              </label>
              <input
                type="text"
                value={formData.domain}
                onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="company.dogan.io"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {isRTL ? 'البريد الإلكتروني' : 'Email'}
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="admin@company.com"
              />
            </div>
          </div>

          <div className="flex gap-3 mt-6">
            <button
              onClick={() => setShowCreateModal(false)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              {isRTL ? 'إلغاء' : 'Cancel'}
            </button>
            <button
              onClick={() => {
                // Handle create tenant
                setShowCreateModal(false);
              }}
              className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              {isRTL ? 'إنشاء' : 'Create'}
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {t('tenants', 'المستأجرون')}
          </h1>
          <p className="text-gray-600 mt-1">
            {isRTL ? 'إدارة جميع المستأجرين في النظام' : 'Manage all tenants in the system'}
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
          <Plus size={20} />
          <span>{isRTL ? 'إضافة مستأجر' : 'Add Tenant'}</span>
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="relative">
          <Search className={`absolute ${isRTL ? 'right-3' : 'left-3'} top-1/2 -translate-y-1/2 text-gray-400`} size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={isRTL ? 'البحث عن مستأجر...' : 'Search tenants...'}
            className={`w-full ${isRTL ? 'pr-10 pl-4' : 'pl-10 pr-4'} py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500`}
          />
        </div>
      </div>

      {/* Tenants Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">{t('loading', 'جاري التحميل...')}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tenants.map((tenant) => (
            <TenantCard key={tenant.id} tenant={tenant} />
          ))}
        </div>
      )}

      {/* Create Tenant Modal */}
      {showCreateModal && <CreateTenantModal />}
    </div>
  );
};

export default TenantsPage;
