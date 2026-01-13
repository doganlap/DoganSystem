/**
 * Design Tokens
 * Generated from Figma design system
 * These tokens will be synced with Figma variables
 */

export const designTokens = {
  colors: {
    primary: {
      50: '#F0F9FF',
      100: '#E0F2FE',
      200: '#BAE6FD',
      300: '#7DD3FC',
      400: '#38BDF8',
      500: '#0EA5E9', // Base
      600: '#0284C7',
      700: '#0369A1',
      800: '#075985',
      900: '#0C4A6E',
    },
    secondary: {
      50: '#FDF4F4',
      100: '#FCE8E8',
      200: '#F9D1D1',
      300: '#F4AAAA',
      400: '#ED7A7A',
      500: '#E53E3E', // Saudi Green
      600: '#C53030',
      700: '#9B2C2C',
      800: '#742A2A',
      900: '#63171B',
    },
    neutral: {
      50: '#FAFAFA',
      100: '#F5F5F5',
      200: '#E5E5E5',
      300: '#D4D4D4',
      400: '#A3A3A3',
      500: '#737373',
      600: '#525252',
      700: '#404040',
      800: '#262626',
      900: '#171717',
    },
    semantic: {
      success: '#10B981',
      warning: '#F59E0B',
      error: '#EF4444',
      info: '#3B82F6',
    },
  },
  typography: {
    fontFamily: {
      primary: 'Inter, system-ui, -apple-system, sans-serif',
      secondary: 'IBM Plex Sans Arabic, Arial, sans-serif', // RTL support
      mono: 'JetBrains Mono, monospace',
    },
    fontSize: {
      display1: '72px',
      display2: '60px',
      h1: '48px',
      h2: '36px',
      h3: '30px',
      h4: '24px',
      h5: '20px',
      h6: '18px',
      bodyLarge: '18px',
      body: '16px',
      bodySmall: '14px',
      caption: '12px',
      label: '14px',
    },
    fontWeight: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.75,
    },
  },
  spacing: {
    0: '0px',
    1: '4px',
    2: '8px',
    3: '12px',
    4: '16px',
    5: '20px',
    6: '24px',
    8: '32px',
    10: '40px',
    12: '48px',
    16: '64px',
    20: '80px',
    24: '96px',
    32: '128px',
  },
  borderRadius: {
    none: '0px',
    small: '4px',
    medium: '8px',
    large: '12px',
    xlarge: '16px',
    full: '9999px',
  },
  shadows: {
    level0: 'none',
    level1: '0px 1px 2px rgba(0, 0, 0, 0.05)',
    level2: '0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)',
    level3: '0px 4px 6px rgba(0, 0, 0, 0.07), 0px 2px 4px rgba(0, 0, 0, 0.06)',
    level4: '0px 10px 15px rgba(0, 0, 0, 0.1), 0px 4px 6px rgba(0, 0, 0, 0.05)',
    level5: '0px 20px 25px rgba(0, 0, 0, 0.1), 0px 10px 10px rgba(0, 0, 0, 0.04)',
  },
  breakpoints: {
    mobile: '320px',
    tablet: '768px',
    desktop: '1024px',
    largeDesktop: '1440px',
  },
  animation: {
    duration: {
      instant: '0ms',
      fast: '150ms',
      normal: '250ms',
      slow: '350ms',
      slower: '500ms',
    },
    easing: {
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    },
  },
} as const;

export type DesignTokens = typeof designTokens;
