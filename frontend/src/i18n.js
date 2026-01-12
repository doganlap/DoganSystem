import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  ar: {
    translation: {
      welcome: 'مرحباً بك في نظام دوجان',
      subtitle: 'منصة SaaS متعددة المستأجرين',
      features: 'المميزات',
      multiTenant: 'بنية متعددة المستأجرين',
      multiTenantDesc: 'عزل كامل للمستأجرين وإدارة متقدمة',
      erpIntegration: 'تكامل ERPNext',
      erpIntegrationDesc: 'إدارة مثيلات ERPNext متعددة',
      aiAgents: 'نظام الوكلاء الذكي',
      aiAgentsDesc: 'وكلاء بأسلوب الموظفين مع Claude AI',
      subscriptions: 'إدارة الاشتراكات',
      subscriptionsDesc: 'الفوترة ودورة حياة الاشتراك',
      getStarted: 'ابدأ الآن',
      learnMore: 'اعرف المزيد',
      contact: 'تواصل معنا',
      footer: '© 2026 نظام دوجان. جميع الحقوق محفوظة.'
    }
  },
  en: {
    translation: {
      welcome: 'Welcome to DoganSystem',
      subtitle: 'Multi-Tenant SaaS Platform',
      features: 'Features',
      multiTenant: 'Multi-Tenant Architecture',
      multiTenantDesc: 'Complete tenant isolation and management',
      erpIntegration: 'ERPNext Integration',
      erpIntegrationDesc: 'Manage multiple ERPNext instances',
      aiAgents: 'AI Agent System',
      aiAgentsDesc: 'Employee-style agents with Claude AI',
      subscriptions: 'Subscription Management',
      subscriptionsDesc: 'Billing and subscription lifecycle',
      getStarted: 'Get Started',
      learnMore: 'Learn More',
      contact: 'Contact Us',
      footer: '© 2026 DoganSystem. All rights reserved.'
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'ar',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
