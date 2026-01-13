import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Server, Plus, CheckCircle, XCircle, RefreshCw } from 'lucide-react';

const ERPNextPage = ({ tenantId }) => {
  const { t, i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';

  const mockInstances = [
    {
      id: '1',
      name: isRTL ? 'ERPNext الرئيسي' : 'Main ERPNext',
      baseUrl: 'https://erp.company.com',
      status: 'connected',
      version: 'v16.2',
      lastSync: '2026-01-13T11:30:00',
    },
    {
      id: '2',
      name: isRTL ? 'ERPNext التطوير' : 'Dev ERPNext',
      baseUrl: 'https://dev-erp.company.com',
      status: 'disconnected',
      version: 'v16.2',
      lastSync: '2026-01-12T15:20:00',
    },
  ];

  const InstanceCard = ({ instance }) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
            instance.status === 'connected' ? 'bg-green-100' : 'bg-red-100'
          }`}>
            <Server className={`w-6 h-6 ${
              instance.status === 'connected' ? 'text-green-600' : 'text-red-600'
            }`} />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">{instance.name}</h3>
            <p className="text-sm text-gray-500">{instance.baseUrl}</p>
          </div>
        </div>

        {instance.status === 'connected' ? (
          <CheckCircle className="w-6 h-6 text-green-600" />
        ) : (
          <XCircle className="w-6 h-6 text-red-600" />
        )}
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">{isRTL ? 'الإصدار' : 'Version'}</span>
          <span className="font-medium text-gray-900">{instance.version}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">{isRTL ? 'آخر مزامنة' : 'Last Sync'}</span>
          <span className="text-gray-900">
            {new Date(instance.lastSync).toLocaleDateString(isRTL ? 'ar-SA' : 'en-US')}
          </span>
        </div>
      </div>

      <button className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
        <RefreshCw size={18} />
        <span>{isRTL ? 'اختبار الاتصال' : 'Test Connection'}</span>
      </button>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">ERPNext</h1>
          <p className="text-gray-600 mt-1">
            {isRTL ? 'إدارة مثيلات ERPNext' : 'Manage ERPNext instances'}
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
          <Plus size={20} />
          <span>{isRTL ? 'إضافة مثيل' : 'Add Instance'}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockInstances.map((instance) => (
          <InstanceCard key={instance.id} instance={instance} />
        ))}
      </div>
    </div>
  );
};

export default ERPNextPage;
