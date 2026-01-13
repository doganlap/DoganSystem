/**
 * Card Component
 * Built from Figma design system
 * Supports multiple variants
 */

import React from 'react';
import { Card as MuiCard, CardProps as MuiCardProps, CardContent, CardHeader, CardActions } from '@mui/material';
import { designTokens } from '../../design-system/tokens';

export type CardVariant = 'default' | 'elevated' | 'outlined';

export interface CardProps extends MuiCardProps {
  variant?: CardVariant;
  title?: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  variant = 'default',
  title,
  subtitle,
  actions,
  children,
  ...props
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'default':
        return {
          backgroundColor: '#FFFFFF',
          border: `1px solid ${designTokens.colors.neutral[200]}`,
          boxShadow: designTokens.shadows.level1,
        };
      case 'elevated':
        return {
          backgroundColor: '#FFFFFF',
          boxShadow: designTokens.shadows.level3,
          border: 'none',
        };
      case 'outlined':
        return {
          backgroundColor: '#FFFFFF',
          border: `1px solid ${designTokens.colors.neutral[200]}`,
          boxShadow: 'none',
        };
      default:
        return {};
    }
  };

  return (
    <MuiCard
      {...props}
      sx={{
        borderRadius: designTokens.borderRadius.large,
        padding: designTokens.spacing[6],
        ...getVariantStyles(),
        ...props.sx,
      }}
    >
      {(title || subtitle) && (
        <CardHeader
          title={title}
          subheader={subtitle}
          sx={{
            padding: 0,
            marginBottom: designTokens.spacing[4],
            '& .MuiCardHeader-title': {
              fontSize: designTokens.typography.fontSize.h5,
              fontWeight: designTokens.typography.fontWeight.semibold,
              color: designTokens.colors.neutral[900],
            },
            '& .MuiCardHeader-subheader': {
              fontSize: designTokens.typography.fontSize.bodySmall,
              color: designTokens.colors.neutral[600],
            },
          }}
        />
      )}
      <CardContent sx={{ padding: 0, '&:last-child': { paddingBottom: 0 } }}>
        {children}
      </CardContent>
      {actions && (
        <CardActions sx={{ padding: 0, marginTop: designTokens.spacing[4] }}>
          {actions}
        </CardActions>
      )}
    </MuiCard>
  );
};
