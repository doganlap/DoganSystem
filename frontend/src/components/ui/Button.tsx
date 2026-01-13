/**
 * Button Component
 * Built from Figma design system
 * Supports all variants and states
 */

import React from 'react';
import { Button as MuiButton, ButtonProps as MuiButtonProps, CircularProgress } from '@mui/material';
import { designTokens } from '../../design-system/tokens';

export type ButtonVariant = 'primary' | 'secondary' | 'tertiary' | 'ghost' | 'danger';
export type ButtonSize = 'small' | 'medium' | 'large';

export interface ButtonProps extends Omit<MuiButtonProps, 'variant' | 'size'> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  loading = false,
  disabled,
  children,
  ...props
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'primary':
        return {
          backgroundColor: designTokens.colors.primary[500],
          color: '#FFFFFF',
          '&:hover': {
            backgroundColor: designTokens.colors.primary[600],
          },
          '&:active': {
            backgroundColor: designTokens.colors.primary[700],
          },
        };
      case 'secondary':
        return {
          backgroundColor: 'transparent',
          border: `1px solid ${designTokens.colors.primary[500]}`,
          color: designTokens.colors.primary[500],
          '&:hover': {
            backgroundColor: designTokens.colors.primary[50],
          },
        };
      case 'tertiary':
        return {
          backgroundColor: 'transparent',
          color: designTokens.colors.primary[500],
          '&:hover': {
            backgroundColor: designTokens.colors.primary[50],
          },
        };
      case 'ghost':
        return {
          backgroundColor: 'transparent',
          color: designTokens.colors.neutral[700],
          '&:hover': {
            backgroundColor: designTokens.colors.neutral[100],
          },
        };
      case 'danger':
        return {
          backgroundColor: designTokens.colors.semantic.error,
          color: '#FFFFFF',
          '&:hover': {
            backgroundColor: '#DC2626',
          },
        };
      default:
        return {};
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          height: '32px',
          padding: `${designTokens.spacing[2]} ${designTokens.spacing[4]}`,
          fontSize: designTokens.typography.fontSize.bodySmall,
        };
      case 'medium':
        return {
          height: '40px',
          padding: `${designTokens.spacing[3]} ${designTokens.spacing[6]}`,
          fontSize: designTokens.typography.fontSize.body,
        };
      case 'large':
        return {
          height: '48px',
          padding: `${designTokens.spacing[5]} ${designTokens.spacing[8]}`,
          fontSize: designTokens.typography.fontSize.bodyLarge,
        };
      default:
        return {};
    }
  };

  return (
    <MuiButton
      {...props}
      disabled={disabled || loading}
      sx={{
        ...getVariantStyles(),
        ...getSizeStyles(),
        borderRadius: designTokens.borderRadius.medium,
        fontWeight: designTokens.typography.fontWeight.medium,
        textTransform: 'none',
        boxShadow: 'none',
        '&:hover': {
          boxShadow: designTokens.shadows.level2,
        },
        '&:disabled': {
          backgroundColor: designTokens.colors.neutral[200],
          color: designTokens.colors.neutral[400],
        },
        ...props.sx,
      }}
    >
      {loading ? (
        <>
          <CircularProgress size={16} sx={{ mr: 1, color: 'inherit' }} />
          {children}
        </>
      ) : (
        children
      )}
    </MuiButton>
  );
};
