import React from 'react';
import { useTranslation } from 'react-i18next';
import {
  Users,
  Server,
  Bot,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Activity,
  Clock,
} from 'lucide-react';
import { useTenantDashboard, useTenantMetrics } from '../hooks/useApi';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = ({ tenantId }) => {
  const { t, i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';

  const { data: dashboard, isLoading: dashboardLoading } = useTenantDashboard(tenantId);
  const { data: metrics, isLoading: metricsLoading } = useTenantMetrics(tenantId);

  // Mock data for charts (replace with real data from API)
  const activityData = [
    { name: isRTL ? 'السبت' : 'Sat', value: 65 },
    { name: isRTL ? 'الأحد' : 'Sun', value: 78 },
    { name: isRTL ? 'الاثنين' : 'Mon', value: 90 },
    { name: isRTL ? 'الثلاثاء' : 'Tue', value: 81 },
    { name: isRTL ? 'الأربعاء' : 'Wed', value: 95 },
    { name: isRTL ? 'الخميس' : 'Thu', value: 72 },
    { name: isRTL ? 'الجمعة' : 'Fri', value: 55 },
  ];

  const agentTasksData = [
    { name: isRTL ? 'مكتملة' : 'Completed', value: 245, color: '#10b981' },
    { name: isRTL ? 'قيد التنفيذ' : 'In Progress', value: 89, color: '#3b82f6' },
    { name: isRTL ? 'معلقة' : 'Pending', value: 34, color: '#f59e0b' },
    { name: isRTL ? 'فاشلة' : 'Failed', value: 12, color: '#ef4444' },
  ];

  const StatCard = ({ icon: Icon, title, value, change, trend, color }) => (
    <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 rounded-lg ${color} bg-opacity-10 flex items-center justify-center`}>
          <Icon className={`w-6 h-6 ${color.replace('bg-', 'text-')}`} />
        </div>
        {change && (
          <div className={`flex items-center gap-1 text-sm font-medium ${
            trend === 'up' ? 'text-green-600' : 'text-red-600'
          }`}>
            <TrendingUp size={16} className={trend === 'down' ? 'rotate-180' : ''} />
            <span>{change}</span>
          </div>
        )}
      </div>
      <h3 className="text-gray-600 text-sm font-medium mb-1">{title}</h3>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
    </div>
  );

  const QuickAction = ({ icon: Icon, title, description, onClick }) => (
    <button
      onClick={onClick}
      className="flex items-start gap-4 p-4 bg-white rounded-lg border border-gray-200 hover:border-indigo-500 hover:shadow-md transition-all text-left w-full"
    >
      <div className="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
        <Icon className="w-5 h-5 text-indigo-600" />
      </div>
      <div className="flex-1">
        <h4 className="font-semibold text-gray-900 mb-1">{title}</h4>
        <p className="text-sm text-gray-600">{description}</p>
      </div>
    </button>
  );

  if (dashboardLoading || metricsLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <Activity className="w-12 h-12 text-indigo-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">{t('loading', 'جاري التحميل...')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {t('dashboard', 'لوحة التحكم')}
          </h1>
          <p className="text-gray-600 mt-1">
            {isRTL ? 'نظرة عامة على النظام والأداء' : 'System overview and performance'}
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Clock size={16} />
          <span>{new Date().toLocaleDateString(isRTL ? 'ar-SA' : 'en-US')}</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Users}
          title={t('totalTenants', 'إجمالي المستأجرين')}
          value="24"
          change="+12%"
          trend="up"
          color="bg-blue-500"
        />
        <StatCard
          icon={Bot}
          title={t('activeAgents', 'الوكلاء النشطون')}
          value="156"
          change="+8%"
          trend="up"
          color="bg-purple-500"
        />
        <StatCard
          icon={Server}
          title={t('erpInstances', 'مثيلات ERPNext')}
          value="18"
          change="+3"
          trend="up"
          color="bg-green-500"
        />
        <StatCard
          icon={Activity}
          title={t('systemHealth', 'صحة النظام')}
          value="99.8%"
          change="+0.2%"
          trend="up"
          color="bg-orange-500"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Chart */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isRTL ? 'نشاط الأسبوع' : 'Weekly Activity'}
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={activityData}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#6366f1"
                fillOpacity={1}
                fill="url(#colorValue)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Agent Tasks Distribution */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isRTL ? 'توزيع مهام الوكلاء' : 'Agent Tasks Distribution'}
          </h3>
          <div className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={agentTasksData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {agentTasksData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Quick Actions & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isRTL ? 'إجراءات سريعة' : 'Quick Actions'}
          </h3>
          <div className="space-y-3">
            <QuickAction
              icon={Users}
              title={isRTL ? 'إضافة مستأجر جديد' : 'Add New Tenant'}
              description={isRTL ? 'إنشاء مستأجر جديد في النظام' : 'Create a new tenant in the system'}
            />
            <QuickAction
              icon={Bot}
              title={isRTL ? 'إنشاء وكيل' : 'Create Agent'}
              description={isRTL ? 'إضافة وكيل ذكي جديد' : 'Add a new AI agent'}
            />
            <QuickAction
              icon={Server}
              title={isRTL ? 'إضافة ERPNext' : 'Add ERPNext'}
              description={isRTL ? 'ربط مثيل ERPNext جديد' : 'Connect a new ERPNext instance'}
            />
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {isRTL ? 'النشاط الأخير' : 'Recent Activity'}
          </h3>
          <div className="space-y-4">
            {[
              {
                icon: CheckCircle,
                text: isRTL ? 'تم إنشاء مستأجر جديد: شركة التقنية' : 'New tenant created: Tech Corp',
                time: isRTL ? 'منذ 5 دقائق' : '5 minutes ago',
                color: 'text-green-600',
              },
              {
                icon: Bot,
                text: isRTL ? 'وكيل "المبيعات-001" أكمل 45 مهمة' : 'Agent "Sales-001" completed 45 tasks',
                time: isRTL ? 'منذ 12 دقيقة' : '12 minutes ago',
                color: 'text-blue-600',
              },
              {
                icon: Server,
                text: isRTL ? 'مثيل ERPNext متصل بنجاح' : 'ERPNext instance connected successfully',
                time: isRTL ? 'منذ 30 دقيقة' : '30 minutes ago',
                color: 'text-purple-600',
              },
              {
                icon: AlertCircle,
                text: isRTL ? 'تنبيه: استخدام الذاكرة 85%' : 'Alert: Memory usage at 85%',
                time: isRTL ? 'منذ ساعة' : '1 hour ago',
                color: 'text-orange-600',
              },
            ].map((activity, index) => {
              const Icon = activity.icon;
              return (
                <div key={index} className="flex items-start gap-3">
                  <Icon className={`w-5 h-5 ${activity.color} flex-shrink-0 mt-0.5`} />
                  <div className="flex-1">
                    <p className="text-sm text-gray-900">{activity.text}</p>
                    <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
