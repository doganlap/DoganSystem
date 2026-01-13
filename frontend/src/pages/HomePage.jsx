import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import {
  Server,
  Users,
  Bot,
  CreditCard,
  ArrowRight,
  Globe,
  Sparkles
} from 'lucide-react';

const HomePage = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const isRTL = i18n.language === 'ar';

  const features = [
    {
      icon: Server,
      title: t('multiTenant'),
      description: t('multiTenantDesc'),
      color: 'bg-blue-500',
    },
    {
      icon: Server,
      title: t('erpIntegration'),
      description: t('erpIntegrationDesc'),
      color: 'bg-green-500',
    },
    {
      icon: Bot,
      title: t('aiAgents'),
      description: t('aiAgentsDesc'),
      color: 'bg-purple-500',
    },
    {
      icon: CreditCard,
      title: t('subscriptions'),
      description: t('subscriptionsDesc'),
      color: 'bg-orange-500',
    },
  ];

  const toggleLanguage = () => {
    const newLang = i18n.language === 'ar' ? 'en' : 'ar';
    i18n.changeLanguage(newLang);
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 ${isRTL ? 'rtl' : 'ltr'}`}>
      {/* Header */}
      <header className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Server className="w-10 h-10 text-white" />
            <h1 className="text-2xl font-bold text-white">DoganSystem</h1>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors"
            >
              <Globe size={18} />
              <span>{i18n.language === 'ar' ? 'English' : 'العربية'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-center gap-2 mb-6">
            <Sparkles className="w-8 h-8 text-yellow-400 animate-pulse" />
            <span className="text-yellow-400 font-semibold text-lg">
              {isRTL ? 'نظام SaaS متعدد المستأجرين' : 'Multi-Tenant SaaS Platform'}
            </span>
            <Sparkles className="w-8 h-8 text-yellow-400 animate-pulse" />
          </div>

          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            {t('welcome')}
          </h2>

          <p className="text-xl text-indigo-200 mb-8 leading-relaxed">
            {isRTL
              ? 'منصة شاملة لإدارة المستأجرين مع تكامل ERPNext ونظام وكلاء ذكي متقدم'
              : 'Complete tenant management platform with ERPNext integration and advanced AI agent system'}
          </p>

          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => navigate('/app/dashboard')}
              className="flex items-center gap-2 px-8 py-4 bg-white text-indigo-900 rounded-xl font-semibold hover:bg-indigo-50 transition-all transform hover:scale-105 shadow-xl"
            >
              <span>{t('getStarted')}</span>
              <ArrowRight size={20} className={isRTL ? 'rotate-180' : ''} />
            </button>

            <button
              onClick={() => navigate('/app/monitoring')}
              className="px-8 py-4 bg-white/10 hover:bg-white/20 text-white rounded-xl font-semibold backdrop-blur-sm transition-all border border-white/20"
            >
              {t('learnMore')}
            </button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="container mx-auto px-6 py-20">
        <h3 className="text-3xl font-bold text-white text-center mb-12">
          {t('features')}
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all transform hover:scale-105 cursor-pointer"
              >
                <div className={`${feature.color} w-14 h-14 rounded-xl flex items-center justify-center mb-4`}>
                  <Icon className="w-7 h-7 text-white" />
                </div>
                <h4 className="text-xl font-semibold text-white mb-2">
                  {feature.title}
                </h4>
                <p className="text-indigo-200 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="bg-white/10 backdrop-blur-md rounded-3xl p-12 border border-white/20">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-5xl font-bold text-white mb-2">100+</div>
              <div className="text-indigo-200 text-lg">
                {isRTL ? 'مستأجر نشط' : 'Active Tenants'}
              </div>
            </div>
            <div>
              <div className="text-5xl font-bold text-white mb-2">500+</div>
              <div className="text-indigo-200 text-lg">
                {isRTL ? 'وكيل ذكي' : 'AI Agents'}
              </div>
            </div>
            <div>
              <div className="text-5xl font-bold text-white mb-2">99.9%</div>
              <div className="text-indigo-200 text-lg">
                {isRTL ? 'وقت التشغيل' : 'Uptime'}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-8 border-t border-white/10">
        <div className="text-center text-indigo-200">
          <p>{t('footer')}</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
