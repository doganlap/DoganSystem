'use client'

import { Card, CardContent, Box, Typography, Avatar } from '@mui/material'
import { TrendingUp, TrendingDown } from '@mui/icons-material'

interface StatsCardProps {
  title: string
  value: string | number
  icon: React.ReactNode
  color: 'primary' | 'secondary' | 'success' | 'warning' | 'error'
  trend?: string
  trendLabel?: string
}

export default function StatsCard({
  title,
  value,
  icon,
  color,
  trend,
  trendLabel,
}: StatsCardProps) {
  const isPositive = trend?.startsWith('+')

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box>
            <Typography color="text.secondary" variant="body2" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
              {value}
            </Typography>
            {trend && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 1 }}>
                {isPositive ? (
                  <TrendingUp fontSize="small" color="success" />
                ) : (
                  <TrendingDown fontSize="small" color="error" />
                )}
                <Typography
                  variant="caption"
                  sx={{
                    color: isPositive ? 'success.main' : 'error.main',
                    fontWeight: 600,
                  }}
                >
                  {trend}
                </Typography>
                {trendLabel && (
                  <Typography variant="caption" color="text.secondary">
                    {trendLabel}
                  </Typography>
                )}
              </Box>
            )}
          </Box>
          <Avatar
            sx={{
              bgcolor: `${color}.main`,
              width: 56,
              height: 56,
            }}
          >
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  )
}
