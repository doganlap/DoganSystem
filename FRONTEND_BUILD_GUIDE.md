# Front-End Build Guide
## Building from Figma Design System

---

## 🎯 Overview

This guide explains how to build the front-end application from scratch using the Figma design system, ensuring consistency, scalability, and enterprise-grade quality.

---

## 📋 Prerequisites

1. **Figma Design File** - Complete design system in Figma
2. **Node.js 18+** - Runtime environment
3. **npm/yarn/pnpm** - Package manager
4. **VS Code** - Recommended IDE
5. **Figma Desktop App** - For design token export

---

## 🏗️ Architecture

### Technology Stack
```
Front-End Framework: React 18 + TypeScript
Build Tool: Vite
UI Library: Material-UI (MUI) v5
Styling: Tailwind CSS + Design Tokens
State Management: React Query + Zustand
Routing: React Router v6
Forms: React Hook Form + Zod
Internationalization: react-i18next
Testing: Vitest + React Testing Library
```

### Project Structure
```
frontend/
├── src/
│   ├── design-system/          # Design tokens & theme
│   │   ├── tokens.ts           # Design tokens from Figma
│   │   └── theme.ts             # MUI theme configuration
│   ├── components/
│   │   ├── ui/                  # Base components (from Figma)
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   └── index.ts
│   │   ├── layout/               # Layout components
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   └── features/             # Feature-specific components
│   │       ├── dashboard/
│   │       ├── employees/
│   │       └── offers/
│   ├── pages/                    # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Employees.tsx
│   │   └── Offers.tsx
│   ├── hooks/                     # Custom React hooks
│   ├── services/                 # API services
│   ├── utils/                     # Utility functions
│   ├── types/                     # TypeScript types
│   ├── locales/                   # i18n translations
│   └── App.tsx                    # Root component
├── public/                        # Static assets
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

---

## 🚀 Step-by-Step Build Process

### Step 1: Export Design Tokens from Figma

1. **Install Figma Plugins:**
   - Design Tokens
   - Figma to React

2. **Export Tokens:**
   ```bash
   # In Figma:
   # 1. Select all design tokens
   # 2. Use "Design Tokens" plugin
   # 3. Export as JSON
   # 4. Save to frontend/src/design-system/tokens.json
   ```

3. **Update tokens.ts:**
   ```typescript
   // Import from Figma export
   import figmaTokens from './tokens.json';
   export const designTokens = figmaTokens;
   ```

### Step 2: Set Up Project

```bash
cd frontend

# Install dependencies
npm install

# Install additional design system dependencies
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled
npm install tailwindcss postcss autoprefixer
npm install @tanstack/react-query zustand
npm install react-router-dom react-hook-form zod
npm install react-i18next i18next
```

### Step 3: Configure Build Tools

**vite.config.ts:**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@design-system': path.resolve(__dirname, './src/design-system'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});
```

**tailwind.config.js:**
```javascript
import { designTokens } from './src/design-system/tokens';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: designTokens.colors,
      spacing: designTokens.spacing,
      borderRadius: designTokens.borderRadius,
      fontFamily: designTokens.typography.fontFamily,
      fontSize: designTokens.typography.fontSize,
    },
  },
  plugins: [],
};
```

### Step 4: Build Components from Figma

#### Component Development Workflow

1. **Identify Component in Figma**
   - Select component frame
   - Note all variants and states
   - Check spacing, colors, typography

2. **Create Component File**
   ```bash
   touch src/components/ui/Button.tsx
   ```

3. **Implement Component**
   - Use design tokens
   - Support all variants
   - Add TypeScript types
   - Include accessibility

4. **Test Component**
   - Visual regression
   - Accessibility audit
   - Responsive behavior

#### Example: Building Button Component

```typescript
// 1. Check Figma for:
//    - Variants: Primary, Secondary, Tertiary, Ghost, Danger
//    - Sizes: Small, Medium, Large
//    - States: Default, Hover, Active, Disabled, Loading

// 2. Implement using design tokens
import { designTokens } from '@design-system/tokens';

export const Button = ({ variant, size, ...props }) => {
  const styles = {
    backgroundColor: designTokens.colors.primary[500],
    padding: designTokens.spacing[3],
    borderRadius: designTokens.borderRadius.medium,
    // ... more styles from Figma
  };
  
  return <button style={styles} {...props} />;
};
```

### Step 5: Build Layout Components

1. **Navbar** - From Figma navigation design
2. **Sidebar** - From Figma sidebar design
3. **Footer** - From Figma footer design
4. **Container** - From Figma layout grid

### Step 6: Build Pages

1. **Dashboard** - From Figma dashboard page
2. **Employee Management** - From Figma employee pages
3. **Consultant Offers** - From Figma offers pages
4. **Settings** - From Figma settings pages

### Step 7: Implement RTL Support

```typescript
// src/utils/rtl.ts
export const isRTL = (locale: string) => locale === 'ar';

// src/App.tsx
import { ThemeProvider } from '@mui/material';
import { rtlTheme } from '@design-system/theme';

const App = () => {
  const { locale } = useTranslation();
  const theme = isRTL(locale) ? rtlTheme : defaultTheme;
  
  return (
    <ThemeProvider theme={theme}>
      <div dir={isRTL(locale) ? 'rtl' : 'ltr'}>
        {/* App content */}
      </div>
    </ThemeProvider>
  );
};
```

### Step 8: Connect to Backend API

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
});

// Use React Query for data fetching
import { useQuery } from '@tanstack/react-query';

export const useEmployees = () => {
  return useQuery({
    queryKey: ['employees'],
    queryFn: () => api.get('/employees').then(res => res.data),
  });
};
```

---

## 🎨 Design System Integration

### Using Design Tokens

```typescript
import { designTokens } from '@design-system/tokens';

// In components
const styles = {
  color: designTokens.colors.primary[500],
  padding: designTokens.spacing[4],
  borderRadius: designTokens.borderRadius.medium,
  fontSize: designTokens.typography.fontSize.body,
};
```

### Using MUI Theme

```typescript
import { useTheme } from '@mui/material';

const Component = () => {
  const theme = useTheme();
  
  return (
    <Box sx={{ color: theme.palette.primary.main }}>
      {/* Content */}
    </Box>
  );
};
```

### Using Tailwind CSS

```tsx
<div className="bg-primary-500 p-4 rounded-medium">
  Content
</div>
```

---

## 📱 Responsive Design

### Breakpoints

```typescript
import { designTokens } from '@design-system/tokens';

const breakpoints = {
  mobile: `@media (max-width: ${designTokens.breakpoints.tablet})`,
  tablet: `@media (min-width: ${designTokens.breakpoints.tablet})`,
  desktop: `@media (min-width: ${designTokens.breakpoints.desktop})`,
};
```

### Responsive Components

```tsx
<Box
  sx={{
    display: { xs: 'block', md: 'flex' },
    padding: { xs: 2, md: 4 },
  }}
>
  Content
</Box>
```

---

## ✅ Quality Checklist

### Before Deployment

- [ ] All components match Figma designs
- [ ] Design tokens synced with Figma
- [ ] Responsive on all breakpoints
- [ ] RTL support tested
- [ ] Accessibility (WCAG AA)
- [ ] Performance optimized
- [ ] Cross-browser tested
- [ ] Unit tests written
- [ ] Documentation complete

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Static Hosting

```bash
# Vercel
vercel deploy

# Netlify
netlify deploy --prod

# AWS S3 + CloudFront
aws s3 sync dist/ s3://your-bucket
```

---

## 📚 Additional Resources

- [Figma Design System](DESIGN_SYSTEM_FIGMA_SPEC.md)
- [Component Library Documentation](./storybook)
- [API Documentation](../docs/api.md)
- [Deployment Guide](../docs/deployment.md)

---

**Status:** 🚀 **READY TO BUILD**

Follow this guide step-by-step to build a production-ready front-end from your Figma designs.
