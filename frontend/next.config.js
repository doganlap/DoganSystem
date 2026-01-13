/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,

  // Output configuration
  output: 'standalone',

  // Image optimization
  images: {
    domains: [
      'localhost',
      'doganconsult.com',
      'saudibusinessgate.com',
      'shahin-grc.com',
      'doganlab.com',
      'doganhub.com',
    ],
    formats: ['image/avif', 'image/webp'],
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_VERSION: process.env.NEXT_PUBLIC_VERSION || '1.0.0',
    NEXT_PUBLIC_BUILD_DATE: new Date().toISOString(),
  },

  // API rewrites
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/api/:path*`,
      },
      {
        source: '/api/dashboard/:path*',
        destination: `${process.env.NEXT_PUBLIC_DASHBOARD_API_URL || 'http://localhost:8007'}/api/:path*`,
      },
      {
        source: '/api/gateway/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_GATEWAY_URL || 'http://localhost:8006'}/api/:path*`,
      },
    ]
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
    ]
  },

  // Headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },

  // Webpack configuration
  webpack: (config, { isServer }) => {
    // Performance optimizations
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      }
    }

    return config
  },

  // Experimental features
  experimental: {
    optimizePackageImports: ['@mui/icons-material', 'lucide-react'],
  },

  // Compiler options
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // PoweredBy header
  poweredByHeader: false,

  // Compression
  compress: true,
}

module.exports = nextConfig
