import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  ar: {
    translation: {
      // Common
      welcome: 'مرحباً بك في نظام دوجان',
      subtitle: 'منصة SaaS متعددة المستأجرين',
      features: 'المميزات',
      loading: 'جاري التحميل...',
      search: 'بحث',
      save: 'حفظ',
      cancel: 'إلغاء',
      delete: 'حذف',
      edit: 'تعديل',
      view: 'عرض',
      create: 'إنشاء',
      add: 'إضافة',

      // Navigation
      dashboard: 'لوحة التحكم',
      tenants: 'المستأجرون',
      agents: 'الوكلاء',
      erpnext: 'ERPNext',
      subscriptions: 'الاشتراكات',
      monitoring: 'المراقبة',
      notifications: 'الإشعارات',
      version: 'الإصدار',
      currentTenant: 'المستأجر الحالي',
      systemOnline: 'النظام متصل',
      changeLanguage: 'تغيير اللغة',

      // Features
      multiTenant: 'بنية متعددة المستأجرين',
      multiTenantDesc: 'عزل كامل للمستأجرين وإدارة متقدمة',
      erpIntegration: 'تكامل ERPNext',
      erpIntegrationDesc: 'إدارة مثيلات ERPNext متعددة',
      aiAgents: 'نظام الوكلاء الذكي',
      aiAgentsDesc: 'وكلاء بأسلوب الموظفين مع Claude AI',
      subscriptions: 'إدارة الاشتراكات',
      subscriptionsDesc: 'الفوترة ودورة حياة الاشتراك',

      // Actions
      getStarted: 'ابدأ الآن',
      learnMore: 'اعرف المزيد',
      contact: 'تواصل معنا',

      // Footer
      footer: '© 2026 نظام دوجان. جميع الحقوق محفوظة.'
    }
  },
  en: {
    translation: {
      // Common
      welcome: 'Welcome to DoganSystem',
      subtitle: 'Multi-Tenant SaaS Platform',
      features: 'Features',
      loading: 'Loading...',
      search: 'Search',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      view: 'View',
      create: 'Create',
      add: 'Add',

      // Navigation
      dashboard: 'Dashboard',
      tenants: 'Tenants',
      agents: 'Agents',
      erpnext: 'ERPNext',
      subscriptions: 'Subscriptions',
      monitoring: 'Monitoring',
      notifications: 'Notifications',
      version: 'Version',
      currentTenant: 'Current Tenant',
      systemOnline: 'System Online',
      changeLanguage: 'Change Language',

      // Features
      multiTenant: 'Multi-Tenant Architecture',
      multiTenantDesc: 'Complete tenant isolation and management',
      erpIntegration: 'ERPNext Integration',
      erpIntegrationDesc: 'Manage multiple ERPNext instances',
      aiAgents: 'AI Agent System',
      aiAgentsDesc: 'Employee-style agents with Claude AI',
      subscriptions: 'Subscription Management',
      subscriptionsDesc: 'Billing and subscription lifecycle',

      // Actions
      getStarted: 'Get Started',
      learnMore: 'Learn More',
      contact: 'Contact Us',

      // Footer
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
