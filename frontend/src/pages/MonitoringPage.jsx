import React from 'react';
import { useTranslation } from 'react-i18next';
import { Activity, Cpu, HardDrive, Database, CheckCircle, AlertTriangle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const MonitoringPage = () => {
  const { t, i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';

  const cpuData = [
    { time: '10:00', value: 45 },
    { time: '10:15', value: 52 },
    { time: '10:30', value: 48 },
    { time: '10:45', value: 65 },
    { time: '11:00', value: 58 },
    { time: '11:15', value: 72 },
    { time: '11:30', value: 55 },
  ];

  const MetricCard = ({ icon: Icon, title, value, status, color }) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 ${color} bg-opacity-10 rounded-lg flex items-center justify-center`}>
          <Icon className={`w-6 h-6 ${color.replace('bg-', 'text-')}`} />
        </div>
        {status === 'healthy' ? (
          <CheckCircle className="w-6 h-6 text-green-600" />
        ) : (
          <AlertTriangle className="w-6 h-6 text-yellow-600" />
        )}
      </div>
      <h3 className="text-gray-600 text-sm font-medium mb-1">{title}</h3>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{t('monitoring', 'المراقبة')}</h1>
        <p className="text-gray-600 mt-1">
          {isRTL ? 'مراقبة صحة النظام والأداء' : 'Monitor system health and performance'}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          icon={Cpu}
          title={isRTL ? 'استخدام المعالج' : 'CPU Usage'}
          value="58%"
          status="healthy"
          color="bg-blue-500"
        />
        <MetricCard
          icon={HardDrive}
          title={isRTL ? 'استخدام الذاكرة' : 'Memory Usage'}
          value="72%"
          status="healthy"
          color="bg-purple-500"
        />
        <MetricCard
          icon={Database}
          title={isRTL ? 'استخدام القرص' : 'Disk Usage'}
          value="45%"
          status="healthy"
          color="bg-green-500"
        />
        <MetricCard
          icon={Activity}
          title={isRTL ? 'حركة الشبكة' : 'Network Traffic'}
          value="234MB/s"
          status="healthy"
          color="bg-orange-500"
        />
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          {isRTL ? 'استخدام المعالج - آخر ساعة' : 'CPU Usage - Last Hour'}
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={cpuData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="time" stroke="#6b7280" />
            <YAxis stroke="#6b7280" />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#6366f1"
              strokeWidth={2}
              dot={{ fill: '#6366f1', r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          {isRTL ? 'حالة الخدمات' : 'Service Status'}
        </h3>
        <div className="space-y-3">
          {[
            { name: 'API Gateway', status: 'operational' },
            { name: 'Tenant Service', status: 'operational' },
            { name: 'Agent Orchestrator', status: 'operational' },
            { name: 'Database', status: 'operational' },
          ].map((service, i) => (
            <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-900">{service.name}</span>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-sm text-green-600">
                  {isRTL ? 'يعمل' : 'Operational'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MonitoringPage;
