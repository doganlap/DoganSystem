'use client';

import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  IconButton,
  AppBar,
  Toolbar,
  Paper,
} from '@mui/material';
import landingContent from '@/content/landing-pages.json';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import SecurityIcon from '@mui/icons-material/Security';
import SpeedIcon from '@mui/icons-material/Speed';
import LanguageIcon from '@mui/icons-material/Language';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { useRouter } from 'next/navigation';

type Language = 'ar' | 'en';

export default function LandingPage() {
  const router = useRouter();
  const [lang, setLang] = useState<Language>('ar');
  const content = landingContent.pages.doganconsult;
  const isRTL = lang === 'ar';

  const toggleLanguage = () => {
    setLang(lang === 'ar' ? 'en' : 'ar');
  };

  const handleGetStarted = () => {
    router.push('/login');
  };

  const handleContactSales = () => {
    window.location.href = 'mailto:info@doganconsult.com';
  };

  const navLinks = {
    ar: { about: 'من نحن', platforms: 'المنصات', contact: 'تواصل معنا' },
    en: { about: 'About', platforms: 'Platforms', contact: 'Contact' },
  };

  const footerContent = {
    ar: {
      brand: 'دوغان للاستشارات',
      tagline: 'منصات حوكمة وتشغيل مدعومة بالذكاء الاصطناعي',
      quickLinks: 'روابط سريعة',
      aboutPlatform: 'حول المنصة',
      pricing: 'الأسعار',
      contactUs: 'تواصل معنا',
      email: 'البريد الإلكتروني',
      phone: 'الهاتف',
      copyright: '© 2026 دوغان للاستشارات. جميع الحقوق محفوظة.',
    },
    en: {
      brand: 'Dogan Consult',
      tagline: 'AI-powered governance and operations platforms',
      quickLinks: 'Quick Links',
      aboutPlatform: 'About Platform',
      pricing: 'Pricing',
      contactUs: 'Contact Us',
      email: 'Email',
      phone: 'Phone',
      copyright: '© 2026 Dogan Consult. All rights reserved.',
    },
  };

  const ctaContent = {
    ar: {
      headline: 'هل أنتم مستعدون للتحول الرقمي؟',
      subheadline: 'انضموا إلى المؤسسات الرائدة في المملكة',
      button: 'ابدأ الآن',
    },
    en: {
      headline: 'Ready for Digital Transformation?',
      subheadline: 'Join leading organizations in Saudi Arabia',
      button: 'Get Started',
    },
  };

  return (
    <Box sx={{ direction: isRTL ? 'rtl' : 'ltr' }}>
      {/* Navigation Bar */}
      <AppBar position="fixed" sx={{ bgcolor: 'white', boxShadow: 1 }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>
            {lang === 'ar' ? 'دوغان للاستشارات' : 'Dogan Consult'}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
            <Typography
              sx={{ color: 'text.primary', cursor: 'pointer', '&:hover': { color: 'primary.main' } }}
            >
              {navLinks[lang].platforms}
            </Typography>
            <Typography
              sx={{ color: 'text.primary', cursor: 'pointer', '&:hover': { color: 'primary.main' } }}
            >
              {navLinks[lang].about}
            </Typography>
            <Typography
              sx={{ color: 'text.primary', cursor: 'pointer', '&:hover': { color: 'primary.main' } }}
            >
              {navLinks[lang].contact}
            </Typography>
            <IconButton onClick={toggleLanguage} sx={{ color: 'primary.main' }}>
              <LanguageIcon />
              <Typography variant="caption" sx={{ ml: 0.5 }}>
                {lang === 'ar' ? 'EN' : 'ع'}
              </Typography>
            </IconButton>
            <Button variant="contained" size="small" onClick={handleGetStarted}>
              {content.hero.cta.primary[lang]}
            </Button>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Spacer for fixed navbar */}
      <Toolbar />

      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #1a237e 0%, #0d47a1 50%, #01579b 100%)',
          color: 'white',
          py: { xs: 10, md: 14 },
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography
                variant="h1"
                sx={{
                  fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4rem' },
                  fontWeight: 800,
                  mb: 3,
                  textAlign: isRTL ? 'right' : 'left',
                  lineHeight: 1.2,
                }}
              >
                {content.hero.headline[lang]}
              </Typography>
              <Typography
                variant="h5"
                sx={{
                  fontSize: { xs: '1.1rem', sm: '1.3rem', md: '1.5rem' },
                  mb: 4,
                  opacity: 0.9,
                  textAlign: isRTL ? 'right' : 'left',
                  lineHeight: 1.6,
                }}
              >
                {content.hero.subheadline[lang]}
              </Typography>
              <Box
                sx={{
                  display: 'flex',
                  gap: 2,
                  justifyContent: isRTL ? 'flex-start' : 'flex-start',
                  flexWrap: 'wrap',
                }}
              >
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleGetStarted}
                  startIcon={<RocketLaunchIcon />}
                  sx={{
                    bgcolor: 'white',
                    color: 'primary.main',
                    fontSize: '1.1rem',
                    px: 4,
                    py: 1.5,
                    fontWeight: 600,
                    '&:hover': {
                      bgcolor: 'grey.100',
                      transform: 'translateY(-2px)',
                      boxShadow: 4,
                    },
                    transition: 'all 0.3s',
                  }}
                >
                  {content.hero.cta.primary[lang]}
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  onClick={handleContactSales}
                  sx={{
                    borderColor: 'white',
                    color: 'white',
                    fontSize: '1.1rem',
                    px: 4,
                    py: 1.5,
                    '&:hover': {
                      borderColor: 'white',
                      bgcolor: 'rgba(255,255,255,0.1)',
                    },
                  }}
                >
                  {content.hero.cta.secondary[lang]}
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12} md={5}>
              <Paper
                elevation={10}
                sx={{
                  p: 4,
                  borderRadius: 4,
                  bgcolor: 'rgba(255,255,255,0.1)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255,255,255,0.2)',
                }}
              >
                <Grid container spacing={3}>
                  {content.stats.items.map((stat, idx) => (
                    <Grid item xs={6} key={idx}>
                      <Box textAlign="center">
                        <Typography
                          variant="h3"
                          sx={{ fontWeight: 800, color: 'white', mb: 0.5 }}
                        >
                          {stat.value}
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                          {stat.label[lang]}
                        </Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Trust Bar */}
      <Box sx={{ bgcolor: '#0d47a1', color: 'white', py: 3 }}>
        <Container maxWidth="lg">
          <Typography
            variant="body1"
            textAlign="center"
            sx={{ mb: 2, fontWeight: 500, opacity: 0.9 }}
          >
            {content.trustBar.title[lang]}
          </Typography>
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              flexWrap: 'wrap',
              gap: 2,
            }}
          >
            {content.trustBar.items.map((item, index) => (
              <Chip
                key={index}
                label={item}
                icon={<SecurityIcon />}
                sx={{
                  bgcolor: 'rgba(255,255,255,0.15)',
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '0.9rem',
                  '& .MuiChip-icon': { color: 'white' },
                }}
              />
            ))}
          </Box>
        </Container>
      </Box>

      {/* Value Proposition */}
      <Container maxWidth="lg" sx={{ py: { xs: 6, md: 10 } }}>
        <Typography
          variant="h3"
          textAlign="center"
          sx={{
            fontSize: { xs: '1.75rem', md: '2.5rem' },
            fontWeight: 700,
            mb: 6,
            color: 'text.primary',
          }}
        >
          {content.valueProposition[lang]}
        </Typography>

        {/* Target Audiences */}
        <Grid container spacing={3}>
          {content.targetAudience.map((audience) => (
            <Grid item xs={12} sm={6} md={4} key={audience.id}>
              <Card
                sx={{
                  height: '100%',
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: 6,
                  },
                  borderTop: '4px solid',
                  borderColor: 'primary.main',
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Typography
                    variant="h5"
                    gutterBottom
                    sx={{ fontWeight: 600, color: 'primary.main', mb: 2 }}
                  >
                    {audience.name[lang]}
                  </Typography>
                  <Typography
                    variant="body1"
                    color="text.secondary"
                    sx={{ mb: 2, lineHeight: 1.7 }}
                  >
                    {audience.description[lang]}
                  </Typography>
                  <Box>
                    {audience.painPoints[lang].map((point, idx) => (
                      <Box
                        key={idx}
                        sx={{ display: 'flex', alignItems: 'center', mb: 1 }}
                      >
                        <CheckCircleIcon
                          sx={{ fontSize: 18, mr: 1, color: 'success.main' }}
                        />
                        <Typography variant="body2">{point}</Typography>
                      </Box>
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Platforms Section */}
      <Box sx={{ bgcolor: 'grey.50', py: { xs: 6, md: 10 } }}>
        <Container maxWidth="lg">
          <Typography
            variant="h3"
            textAlign="center"
            sx={{
              fontSize: { xs: '1.75rem', md: '2.5rem' },
              fontWeight: 700,
              mb: 2,
              color: 'primary.main',
            }}
          >
            {content.platforms.title[lang]}
          </Typography>
          <Typography
            variant="h6"
            textAlign="center"
            color="text.secondary"
            sx={{ mb: 6, maxWidth: '700px', mx: 'auto' }}
          >
            {lang === 'ar'
              ? 'حلول متكاملة للحوكمة والأتمتة والذكاء الاصطناعي'
              : 'Integrated solutions for governance, automation, and AI'}
          </Typography>

          <Grid container spacing={4}>
            {/* Shahin AI Platform */}
            <Grid item xs={12} md={6}>
              <Card
                sx={{
                  height: '100%',
                  transition: 'all 0.3s',
                  '&:hover': { transform: 'translateY(-4px)', boxShadow: 4 },
                  background: 'linear-gradient(135deg, #1a237e 0%, #0d47a1 100%)',
                  color: 'white',
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
                    Shahin AI
                  </Typography>
                  <Typography variant="h6" sx={{ mb: 2, opacity: 0.9 }}>
                    {lang === 'ar'
                      ? 'منصة الحوكمة والمخاطر والامتثال (GRC)'
                      : 'Governance, Risk & Compliance Platform'}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 3, opacity: 0.85 }}>
                    {lang === 'ar'
                      ? 'إدارة شاملة للامتثال التنظيمي مع 117+ إطار تنظيمي و3,200+ ضابط جاهز'
                      : 'Comprehensive regulatory compliance management with 117+ frameworks and 3,200+ pre-loaded controls'}
                  </Typography>
                  <Button
                    variant="contained"
                    sx={{
                      bgcolor: 'white',
                      color: 'primary.main',
                      '&:hover': { bgcolor: 'grey.100' },
                    }}
                  >
                    {lang === 'ar' ? 'اكتشف شاهين' : 'Explore Shahin'}
                  </Button>
                </CardContent>
              </Card>
            </Grid>

            {/* Dogan Systems Platform */}
            <Grid item xs={12} md={6}>
              <Card
                sx={{
                  height: '100%',
                  transition: 'all 0.3s',
                  '&:hover': { transform: 'translateY(-4px)', boxShadow: 4 },
                  background: 'linear-gradient(135deg, #00695c 0%, #00897b 100%)',
                  color: 'white',
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
                    Dogan Systems
                  </Typography>
                  <Typography variant="h6" sx={{ mb: 2, opacity: 0.9 }}>
                    {lang === 'ar'
                      ? 'أتمتة وذكاء تطبيقي فوق ERP'
                      : 'Automation & Applied AI over ERP'}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 3, opacity: 0.85 }}>
                    {lang === 'ar'
                      ? 'طبقات أتمتة وذكاء اصطناعي فوق أنظمتكم الحالية لرفع الكفاءة التشغيلية'
                      : 'Automation and AI layers on top of your existing systems to boost operational efficiency'}
                  </Typography>
                  <Button
                    variant="contained"
                    sx={{
                      bgcolor: 'white',
                      color: '#00695c',
                      '&:hover': { bgcolor: 'grey.100' },
                    }}
                  >
                    {lang === 'ar' ? 'اكتشف دوغان سيستمز' : 'Explore Dogan Systems'}
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #1a237e 0%, #0d47a1 100%)',
          color: 'white',
          py: { xs: 8, md: 10 },
          textAlign: 'center',
        }}
      >
        <Container maxWidth="md">
          <Typography
            variant="h3"
            gutterBottom
            sx={{
              fontSize: { xs: '2rem', md: '2.75rem' },
              fontWeight: 700,
              mb: 2,
            }}
          >
            {ctaContent[lang].headline}
          </Typography>
          <Typography
            variant="h6"
            sx={{
              mb: 4,
              opacity: 0.9,
              fontSize: { xs: '1.1rem', md: '1.3rem' },
            }}
          >
            {ctaContent[lang].subheadline}
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={handleGetStarted}
            startIcon={<SpeedIcon />}
            sx={{
              bgcolor: 'white',
              color: 'primary.main',
              fontSize: '1.2rem',
              px: 6,
              py: 2,
              fontWeight: 600,
              '&:hover': {
                bgcolor: 'grey.100',
                transform: 'scale(1.05)',
              },
              transition: 'all 0.3s',
            }}
          >
            {ctaContent[lang].button}
          </Button>
        </Container>
      </Box>

      {/* Footer */}
      <Box sx={{ bgcolor: 'grey.900', color: 'white', py: 6 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 700 }}>
                {footerContent[lang].brand}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8, mb: 2 }}>
                {footerContent[lang].tagline}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 700 }}>
                {footerContent[lang].quickLinks}
              </Typography>
              <Typography
                variant="body2"
                sx={{ opacity: 0.8, cursor: 'pointer', mb: 1, '&:hover': { opacity: 1 } }}
              >
                {footerContent[lang].aboutPlatform}
              </Typography>
              <Typography
                variant="body2"
                sx={{ opacity: 0.8, cursor: 'pointer', mb: 1, '&:hover': { opacity: 1 } }}
              >
                {footerContent[lang].pricing}
              </Typography>
              <Typography
                variant="body2"
                sx={{ opacity: 0.8, cursor: 'pointer', mb: 1, '&:hover': { opacity: 1 } }}
              >
                {footerContent[lang].contactUs}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 700 }}>
                {footerContent[lang].contactUs}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                {footerContent[lang].email}: info@doganconsult.com
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                {footerContent[lang].phone}: +966 XX XXX XXXX
              </Typography>
            </Grid>
          </Grid>
          <Box
            sx={{
              borderTop: '1px solid rgba(255,255,255,0.1)',
              mt: 4,
              pt: 3,
              textAlign: 'center',
            }}
          >
            <Typography variant="body2" sx={{ opacity: 0.7 }}>
              {footerContent[lang].copyright}
            </Typography>
          </Box>
        </Container>
      </Box>
    </Box>
  );
}
