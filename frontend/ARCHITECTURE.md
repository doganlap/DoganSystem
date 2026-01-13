# DoganSystem Frontend Architecture

## 📋 Table of Contents
- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Design Patterns](#design-patterns)
- [State Management](#state-management)
- [API Integration](#api-integration)
- [Routing](#routing)
- [Internationalization](#internationalization)
- [Testing Strategy](#testing-strategy)
- [Performance Optimization](#performance-optimization)
- [Code Quality](#code-quality)

---

## 🎯 Overview

DoganSystem frontend is a modern React-based single-page application (SPA) built with performance, maintainability, and scalability in mind. It serves as the user interface for a multi-tenant SaaS platform with integrated ERPNext functionality and AI agent management.

### Key Principles
- **Component-Based Architecture**: Modular, reusable components
- **Separation of Concerns**: Clear boundaries between UI, logic, and data
- **Mobile-First Design**: Responsive layouts that work on all devices
- **Accessibility**: WCAG 2.1 AA compliant
- **Performance**: Optimized bundle size and lazy loading
- **Type Safety**: PropTypes validation (ready for TypeScript migration)

---

## 🛠️ Technology Stack

### Core
- **React 18.2+**: UI library with concurrent features
- **Vite 5+**: Fast build tool and dev server
- **React Router 6+**: Client-side routing

### State Management
- **React Query (TanStack Query) 5+**: Server state management
- **React Hooks**: Local state management (useState, useReducer)
- **Context API**: Global UI state (theme, language)

### Styling
- **Tailwind CSS 3+**: Utility-first CSS framework
- **PostCSS**: CSS processing

### Data Fetching
- **Axios**: HTTP client with interceptors
- **React Query**: Caching, background updates, and optimistic updates

### Charts & Visualization
- **Recharts**: Responsive chart library

### Internationalization
- **i18next**: Translation framework
- **react-i18next**: React integration
- **RTL Support**: Arabic right-to-left layout

### Testing
- **Vitest**: Fast unit test framework
- **React Testing Library**: Component testing
- **jsdom**: DOM environment for tests

### Code Quality
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **lint-staged**: Pre-commit hooks
- **Husky**: Git hooks management

---

## 📁 Project Structure

```
frontend/
├── public/                    # Static assets
├── src/
│   ├── components/           # Reusable components
│   │   ├── Layout/          # Layout components
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Layout.jsx
│   │   └── __tests__/       # Component tests
│   │
│   ├── pages/               # Page components (routes)
│   │   ├── HomePage.jsx
│   │   ├── Dashboard.jsx
│   │   ├── TenantsPage.jsx
│   │   ├── AgentsPage.jsx
│   │   ├── ERPNextPage.jsx
│   │   ├── SubscriptionsPage.jsx
│   │   └── MonitoringPage.jsx
│   │
│   ├── hooks/               # Custom React hooks
│   │   └── useApi.js       # API query hooks
│   │
│   ├── services/            # External services
│   │   └── api.js          # API client and endpoints
│   │
│   ├── utils/               # Utility functions
│   │
│   ├── test/                # Test configuration
│   │   └── setup.js
│   │
│   ├── i18n.js             # Internationalization config
│   ├── index.css           # Global styles
│   ├── main.jsx            # Application entry point
│   └── App.jsx             # Root component
│
├── .eslintrc.cjs           # ESLint configuration
├── .prettierrc.json        # Prettier configuration
├── .lintstagedrc.json      # Lint-staged configuration
├── vitest.config.js        # Vitest test configuration
├── vite.config.js          # Vite build configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
├── package.json            # Dependencies and scripts
└── README.md               # Project documentation
```

### Directory Responsibilities

#### `/components`
- **Reusable UI components** that can be used across multiple pages
- Each component should be self-contained with its own styles and tests
- Components should be pure and receive data via props

#### `/pages`
- **Route-level components** that represent entire pages
- Orchestrate multiple components and handle page-specific logic
- Connect to API services and manage page state

#### `/hooks`
- **Custom React hooks** for reusable logic
- API hooks (useApi, useTenants, useAgents, etc.)
- UI hooks (useModal, useToast, etc.)

#### `/services`
- **External service integrations**
- API client configuration
- Third-party service wrappers

#### `/utils`
- **Pure utility functions**
- Formatters, validators, helpers
- No React dependencies

---

## 🎨 Design Patterns

### 1. Container/Presenter Pattern
Separate data fetching (container) from presentation (presenter):

```jsx
// Container Component (Smart Component)
function TenantsPageContainer() {
  const { data, isLoading } = useTenants();
  return <TenantsList tenants={data} loading={isLoading} />;
}

// Presenter Component (Dumb Component)
function TenantsList({ tenants, loading }) {
  if (loading) return <Spinner />;
  return tenants.map(tenant => <TenantCard key={tenant.id} {...tenant} />);
}
```

### 2. Custom Hooks Pattern
Extract reusable logic into custom hooks:

```jsx
// hooks/useApi.js
export const useTenants = (params) => {
  return useQuery('tenants', () => tenantApi.getAll(params));
};

// Usage in component
function MyComponent() {
  const { data, error, isLoading } = useTenants();
  // Component logic
}
```

### 3. Compound Components Pattern
Create related components that work together:

```jsx
function Sidebar() {
  return (
    <nav>
      <Sidebar.Section title="Main">
        <Sidebar.Item icon={Home} to="/dashboard">Dashboard</Sidebar.Item>
        <Sidebar.Item icon={Users} to="/tenants">Tenants</Sidebar.Item>
      </Sidebar.Section>
    </nav>
  );
}
```

### 4. Render Props Pattern
Share code between components using a prop whose value is a function:

```jsx
<QueryWrapper query={useTenants()}>
  {({ data }) => <TenantsList tenants={data} />}
</QueryWrapper>
```

---

## 🗃️ State Management

### Local State (useState/useReducer)
For component-specific state:
```jsx
const [isOpen, setIsOpen] = useState(false);
const [formData, setFormData] = useState({ name: '', email: '' });
```

### Global UI State (Context API)
For app-wide UI state (theme, language, sidebar state):
```jsx
const { theme, toggleTheme } = useTheme();
const { language, changeLanguage } = useLanguage();
```

### Server State (React Query)
For API data, caching, and synchronization:
```jsx
const { data, isLoading, error, refetch } = useQuery(
  'tenants',
  fetchTenants,
  {
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  }
);
```

---

## 🌐 API Integration

### API Client Structure

```javascript
// services/api.js
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

// Request interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error);
  }
);
```

### API Endpoints Structure

```javascript
export const tenantApi = {
  getAll: (params) => apiClient.get('/tenants', { params }),
  getById: (id) => apiClient.get(`/tenants/${id}`),
  create: (data) => apiClient.post('/tenants', data),
  update: (id, data) => apiClient.put(`/tenants/${id}`, data),
  delete: (id) => apiClient.delete(`/tenants/${id}`),
};
```

---

## 🛣️ Routing

Using React Router v6 with lazy loading:

```jsx
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Lazy load pages
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Tenants = lazy(() => import('./pages/TenantsPage'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="tenants" element={<Tenants />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

---

## 🌍 Internationalization

### i18next Configuration

```javascript
// i18n.js
i18n
  .use(initReactI18next)
  .init({
    resources: {
      ar: { translation: arTranslations },
      en: { translation: enTranslations },
    },
    lng: 'ar', // Default language
    fallbackLng: 'en',
  });
```

### Usage in Components

```jsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t, i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';

  return (
    <div dir={isRTL ? 'rtl' : 'ltr'}>
      <h1>{t('welcome')}</h1>
      <button onClick={() => i18n.changeLanguage('en')}>
        {t('changeLanguage')}
      </button>
    </div>
  );
}
```

---

## 🧪 Testing Strategy

### Unit Tests
Test individual components and functions:

```jsx
import { render, screen } from '@testing-library/react';
import Header from '../Header';

describe('Header', () => {
  it('renders tenant selector', () => {
    render(<Header currentTenantId="default" />);
    expect(screen.getByText('Current Tenant:')).toBeInTheDocument();
  });
});
```

### Integration Tests
Test component interactions:

```jsx
it('changes tenant when selector changes', () => {
  const mockSetTenant = vi.fn();
  render(<Header setCurrentTenantId={mockSetTenant} />);

  fireEvent.change(screen.getByRole('combobox'), {
    target: { value: 'new-tenant' }
  });

  expect(mockSetTenant).toHaveBeenCalledWith('new-tenant');
});
```

### Test Coverage Goals
- **Components**: 80%+ coverage
- **Hooks**: 90%+ coverage
- **Utils**: 95%+ coverage

---

## ⚡ Performance Optimization

### Code Splitting
```jsx
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

### Memoization
```jsx
const MemoizedComponent = React.memo(ExpensiveComponent);
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
const memoizedCallback = useCallback(() => { doSomething(); }, []);
```

### React Query Optimization
```jsx
useQuery('tenants', fetchTenants, {
  staleTime: 5 * 60 * 1000, // Don't refetch for 5 minutes
  cacheTime: 10 * 60 * 1000, // Keep in cache for 10 minutes
});
```

### Bundle Size Optimization
- Tree shaking with Vite
- Dynamic imports for large libraries
- Lazy loading of routes and components

---

## ✅ Code Quality

### ESLint Rules
- React best practices
- React Hooks rules
- Accessibility checks (jsx-a11y)
- No console.log in production

### Prettier Configuration
- Consistent code formatting
- 100 character line width
- Single quotes
- 2-space indentation

### Git Hooks
- **pre-commit**: Run ESLint and Prettier on staged files
- **pre-push**: Run tests before pushing

### Scripts
```bash
npm run lint        # Run ESLint
npm run format      # Run Prettier
npm run test        # Run tests
npm run test:ui     # Run tests with UI
npm run coverage    # Generate coverage report
```

---

## 🚀 Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm run test

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Testing Library Documentation](https://testing-library.com/)

---

## 👥 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and development process.
