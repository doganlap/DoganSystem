import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Bot, Plus, Search, Play, Pause, Settings, Activity } from 'lucide-react';
import { useAgents } from '../hooks/useApi';

const AgentsPage = ({ tenantId }) => {
  const { t, i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';
  const [searchQuery, setSearchQuery] = useState('');

  const { data: agentsData, isLoading } = useAgents(tenantId);

  const mockAgents = [
    {
      id: '1',
      name: isRTL ? 'وكيل المبيعات' : 'Sales Agent',
      type: 'sales',
      status: 'active',
      tasksCompleted: 145,
      lastActive: '2026-01-13T10:30:00',
    },
    {
      id: '2',
      name: isRTL ? 'وكيل المخزون' : 'Inventory Agent',
      type: 'inventory',
      status: 'active',
      tasksCompleted: 89,
      lastActive: '2026-01-13T11:15:00',
    },
    {
      id: '3',
      name: isRTL ? 'وكيل المحاسبة' : 'Accounting Agent',
      type: 'accounting',
      status: 'paused',
      tasksCompleted: 234,
      lastActive: '2026-01-13T09:00:00',
    },
  ];

  const agents = agentsData?.data || mockAgents;

  const AgentCard = ({ agent }) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
            agent.status === 'active' ? 'bg-green-100' : 'bg-gray-100'
          }`}>
            <Bot className={`w-6 h-6 ${agent.status === 'active' ? 'text-green-600' : 'text-gray-600'}`} />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">{agent.name}</h3>
            <p className="text-sm text-gray-500">{agent.type}</p>
          </div>
        </div>

        <div className="flex gap-2">
          <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
            {agent.status === 'active' ? (
              <Pause size={18} className="text-gray-600" />
            ) : (
              <Play size={18} className="text-gray-600" />
            )}
          </button>
          <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <Settings size={18} className="text-gray-600" />
          </button>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">{isRTL ? 'الحالة' : 'Status'}</span>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            agent.status === 'active'
              ? 'bg-green-100 text-green-700'
              : 'bg-gray-100 text-gray-700'
          }`}>
            {agent.status === 'active' ? (isRTL ? 'نشط' : 'Active') : (isRTL ? 'متوقف' : 'Paused')}
          </span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">{isRTL ? 'المهام المكتملة' : 'Tasks Completed'}</span>
          <span className="font-semibold text-gray-900">{agent.tasksCompleted}</span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">{isRTL ? 'آخر نشاط' : 'Last Active'}</span>
          <span className="text-sm text-gray-900">
            {new Date(agent.lastActive).toLocaleTimeString(isRTL ? 'ar-SA' : 'en-US', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </span>
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{t('agents', 'الوكلاء')}</h1>
          <p className="text-gray-600 mt-1">
            {isRTL ? 'إدارة الوكلاء الأذكياء' : 'Manage AI agents'}
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
          <Plus size={20} />
          <span>{isRTL ? 'إضافة وكيل' : 'Add Agent'}</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="relative">
          <Search className={`absolute ${isRTL ? 'right-3' : 'left-3'} top-1/2 -translate-y-1/2 text-gray-400`} size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={isRTL ? 'البحث عن وكيل...' : 'Search agents...'}
            className={`w-full ${isRTL ? 'pr-10 pl-4' : 'pl-10 pr-4'} py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500`}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
};

export default AgentsPage;
