# DoganSystem Frontend

Modern React + Vite frontend for the DoganSystem multi-tenant SaaS platform.

## Features

- 🎨 **Modern UI**: Built with React 18 and Tailwind CSS
- 🌍 **Internationalization**: Full Arabic and English support with RTL layout
- 📊 **Data Visualization**: Charts and metrics using Recharts
- 🔄 **Real-time Updates**: React Query for efficient data fetching
- 📱 **Responsive Design**: Mobile-first approach
- 🎯 **Type Safety**: Clean component architecture

## Technology Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Recharts** - Charting library
- **i18next** - Internationalization
- **Axios** - HTTP client
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env with your API URL
# VITE_API_URL=http://localhost:8006/api/v1
```

### Development

```bash
# Start development server
npm run dev

# Access the app at http://localhost:5173
```

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Layout/        # Layout components (Header, Sidebar)
│   │   ├── Dashboard/     # Dashboard components
│   │   ├── Tenants/       # Tenant management components
│   │   ├── Agents/        # Agent management components
│   │   └── Common/        # Shared components
│   ├── pages/             # Page components
│   │   ├── HomePage.jsx
│   │   ├── Dashboard.jsx
│   │   ├── TenantsPage.jsx
│   │   ├── AgentsPage.jsx
│   │   ├── ERPNextPage.jsx
│   │   ├── SubscriptionsPage.jsx
│   │   └── MonitoringPage.jsx
│   ├── services/          # API services
│   │   └── api.js         # API client and endpoints
│   ├── hooks/             # Custom React hooks
│   │   └── useApi.js      # API hooks
│   ├── utils/             # Utility functions
│   ├── i18n.js            # Internationalization config
│   ├── App.jsx            # Main app component
│   └── main.jsx           # Entry point
├── public/                # Static assets
├── index.html             # HTML template
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind configuration
└── package.json           # Dependencies and scripts
```

## Pages

### 🏠 Home Page
- Landing page with feature showcase
- Language toggle (Arabic/English)
- Call-to-action buttons

### 📊 Dashboard
- System overview and metrics
- Real-time activity charts
- Quick actions
- Recent activity feed

### 🏢 Tenants Management
- List all tenants
- Create/edit/delete tenants
- View tenant details and statistics
- Search and filter

### 🤖 Agents Management
- Manage AI agents
- Start/stop agents
- View agent tasks and performance
- Configure agent settings

### 💾 ERPNext Integration
- Manage ERPNext instances
- Test connections
- View sync status
- Configure API credentials

### 💳 Subscriptions
- View subscription plans
- Manage billing
- Upgrade/downgrade plans

### 📈 Monitoring
- System health metrics
- CPU, Memory, Disk usage
- Service status
- Performance charts

## API Integration

The frontend communicates with the DoganSystem backend via REST API:

```javascript
// Example: Fetching tenants
import { tenantApi } from './services/api';

const tenants = await tenantApi.getAll();
```

## Internationalization

The app supports Arabic (RTL) and English (LTR):

```javascript
import { useTranslation } from 'react-i18next';

const { t, i18n } = useTranslation();

// Use translations
<h1>{t('welcome')}</h1>

// Change language
i18n.changeLanguage('ar'); // or 'en'
```

## Customization

### Colors
Edit `tailwind.config.js` to customize colors:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#6366f1',
        // Add more colors
      }
    }
  }
}
```

### API URL
Configure API URL in `.env`:

```env
VITE_API_URL=https://api.yourdomai n.com/api/v1
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8006/api/v1` |
| `VITE_APP_NAME` | Application name | `DoganSystem` |
| `VITE_DEFAULT_LANGUAGE` | Default language | `ar` |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For support, email support@dogansystem.com or open an issue.

---

**Built with ❤️ by DoganSystem Team**
