/**
 * Theme Configuration
 * MUI Theme with Design Tokens
 */

import { createTheme } from '@mui/material/styles';
import { designTokens } from './tokens';

export const theme = createTheme({
  palette: {
    primary: {
      main: designTokens.colors.primary[500],
      light: designTokens.colors.primary[300],
      dark: designTokens.colors.primary[700],
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: designTokens.colors.secondary[500],
      light: designTokens.colors.secondary[300],
      dark: designTokens.colors.secondary[700],
      contrastText: '#FFFFFF',
    },
    error: {
      main: designTokens.colors.semantic.error,
    },
    warning: {
      main: designTokens.colors.semantic.warning,
    },
    info: {
      main: designTokens.colors.semantic.info,
    },
    success: {
      main: designTokens.colors.semantic.success,
    },
    grey: {
      50: designTokens.colors.neutral[50],
      100: designTokens.colors.neutral[100],
      200: designTokens.colors.neutral[200],
      300: designTokens.colors.neutral[300],
      400: designTokens.colors.neutral[400],
      500: designTokens.colors.neutral[500],
      600: designTokens.colors.neutral[600],
      700: designTokens.colors.neutral[700],
      800: designTokens.colors.neutral[800],
      900: designTokens.colors.neutral[900],
    },
    background: {
      default: designTokens.colors.neutral[50],
      paper: '#FFFFFF',
    },
    text: {
      primary: designTokens.colors.neutral[900],
      secondary: designTokens.colors.neutral[600],
    },
  },
  typography: {
    fontFamily: designTokens.typography.fontFamily.primary,
    h1: {
      fontSize: designTokens.typography.fontSize.h1,
      fontWeight: designTokens.typography.fontWeight.bold,
      lineHeight: designTokens.typography.lineHeight.tight,
    },
    h2: {
      fontSize: designTokens.typography.fontSize.h2,
      fontWeight: designTokens.typography.fontWeight.bold,
      lineHeight: designTokens.typography.lineHeight.tight,
    },
    h3: {
      fontSize: designTokens.typography.fontSize.h3,
      fontWeight: designTokens.typography.fontWeight.semibold,
      lineHeight: designTokens.typography.lineHeight.tight,
    },
    h4: {
      fontSize: designTokens.typography.fontSize.h4,
      fontWeight: designTokens.typography.fontWeight.semibold,
      lineHeight: designTokens.typography.lineHeight.normal,
    },
    h5: {
      fontSize: designTokens.typography.fontSize.h5,
      fontWeight: designTokens.typography.fontWeight.medium,
      lineHeight: designTokens.typography.lineHeight.normal,
    },
    h6: {
      fontSize: designTokens.typography.fontSize.h6,
      fontWeight: designTokens.typography.fontWeight.medium,
      lineHeight: designTokens.typography.lineHeight.normal,
    },
    body1: {
      fontSize: designTokens.typography.fontSize.body,
      lineHeight: designTokens.typography.lineHeight.normal,
    },
    body2: {
      fontSize: designTokens.typography.fontSize.bodySmall,
      lineHeight: designTokens.typography.lineHeight.normal,
    },
    button: {
      fontSize: designTokens.typography.fontSize.body,
      fontWeight: designTokens.typography.fontWeight.medium,
      textTransform: 'none' as const,
    },
  },
  shape: {
    borderRadius: parseInt(designTokens.borderRadius.medium),
  },
  shadows: [
    'none',
    designTokens.shadows.level1,
    designTokens.shadows.level2,
    designTokens.shadows.level3,
    designTokens.shadows.level4,
    designTokens.shadows.level5,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
    designTokens.shadows.level2,
  ],
  spacing: (factor: number) => `${factor * 4}px`, // 4px base unit
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: designTokens.borderRadius.medium,
          padding: `${designTokens.spacing[3]} ${designTokens.spacing[6]}`,
          fontSize: designTokens.typography.fontSize.body,
          fontWeight: designTokens.typography.fontWeight.medium,
          textTransform: 'none',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: designTokens.shadows.level2,
          },
        },
        sizeSmall: {
          height: '32px',
          padding: `${designTokens.spacing[2]} ${designTokens.spacing[4]}`,
          fontSize: designTokens.typography.fontSize.bodySmall,
        },
        sizeLarge: {
          height: '48px',
          padding: `${designTokens.spacing[5]} ${designTokens.spacing[8]}`,
          fontSize: designTokens.typography.fontSize.bodyLarge,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: designTokens.borderRadius.large,
          boxShadow: designTokens.shadows.level1,
          border: `1px solid ${designTokens.colors.neutral[200]}`,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: designTokens.borderRadius.medium,
          },
        },
      },
    },
  },
});

// RTL Support
export const rtlTheme = createTheme({
  ...theme,
  direction: 'rtl',
});
