import React from 'react';
import { useTranslation } from 'react-i18next';
import { CreditCard, CheckCircle, Calendar } from 'lucide-react';

const SubscriptionsPage = ({ tenantId }) => {
  const { t, i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';

  const plans = [
    {
      name: isRTL ? 'الأساسية' : 'Basic',
      price: '$99',
      features: [
        isRTL ? 'حتى 10 مستخدمين' : 'Up to 10 users',
        isRTL ? '5 وكلاء ذكيين' : '5 AI agents',
        isRTL ? 'دعم البريد الإلكتروني' : 'Email support',
      ],
      color: 'bg-blue-500',
    },
    {
      name: isRTL ? 'المحترفة' : 'Professional',
      price: '$299',
      features: [
        isRTL ? 'حتى 50 مستخدم' : 'Up to 50 users',
        isRTL ? '25 وكيل ذكي' : '25 AI agents',
        isRTL ? 'دعم ذو أولوية' : 'Priority support',
        isRTL ? 'تكاملات متقدمة' : 'Advanced integrations',
      ],
      color: 'bg-purple-500',
      popular: true,
    },
    {
      name: isRTL ? 'للمؤسسات' : 'Enterprise',
      price: isRTL ? 'مخصص' : 'Custom',
      features: [
        isRTL ? 'مستخدمون غير محدودين' : 'Unlimited users',
        isRTL ? 'وكلاء غير محدودين' : 'Unlimited agents',
        isRTL ? 'دعم مخصص 24/7' : 'Dedicated 24/7 support',
        isRTL ? 'نشر خاص' : 'Private deployment',
      ],
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{t('subscriptions', 'الاشتراكات')}</h1>
        <p className="text-gray-600 mt-1">
          {isRTL ? 'اختر الخطة المناسبة لك' : 'Choose the right plan for you'}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((plan, index) => (
          <div
            key={index}
            className={`bg-white rounded-2xl shadow-sm border-2 ${
              plan.popular ? 'border-indigo-500' : 'border-gray-200'
            } p-6 relative`}
          >
            {plan.popular && (
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2">
                <span className="px-4 py-1 bg-indigo-500 text-white text-sm font-semibold rounded-full">
                  {isRTL ? 'الأكثر شيوعاً' : 'Most Popular'}
                </span>
              </div>
            )}

            <div className={`w-12 h-12 ${plan.color} rounded-lg flex items-center justify-center mb-4`}>
              <CreditCard className="w-6 h-6 text-white" />
            </div>

            <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
            <div className="mb-6">
              <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
              {plan.price !== (isRTL ? 'مخصص' : 'Custom') && (
                <span className="text-gray-600">/{isRTL ? 'شهر' : 'month'}</span>
              )}
            </div>

            <ul className="space-y-3 mb-6">
              {plan.features.map((feature, i) => (
                <li key={i} className="flex items-center gap-2 text-gray-700">
                  <CheckCircle size={20} className="text-green-600 flex-shrink-0" />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <button
              className={`w-full px-4 py-3 rounded-lg font-semibold transition-colors ${
                plan.popular
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                  : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
              }`}
            >
              {isRTL ? 'اشترك الآن' : 'Subscribe Now'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SubscriptionsPage;
