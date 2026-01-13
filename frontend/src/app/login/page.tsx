'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Avatar,
  FormControlLabel,
  Checkbox,
} from '@mui/material'
import {
  LockOutlined as LockIcon,
  Security as SecurityIcon,
} from '@mui/icons-material'
import { useAuth } from '@/contexts/AuthContext'
import { authApi } from '@/services/api'

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { login, isAuthenticated, isLoading: authLoading, refreshUser } = useAuth()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // 2FA state
  const [requires2FA, setRequires2FA] = useState(false)
  const [twoFactorCode, setTwoFactorCode] = useState('')

  // Check for expired token message
  const expired = searchParams.get('expired')

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated && !authLoading) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, authLoading, router])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      const response = await login({
        userNameOrEmail: username,
        password: password,
        rememberMe: rememberMe,
      })

      // Check if 2FA is required
      if (response.requiresTwoFactor) {
        setRequires2FA(true)
        setIsLoading(false)
        return
      }

      router.push('/')
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.')
    } finally {
      setIsLoading(false)
    }
  }

  const handle2FASubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await authApi.completeTwoFactorLogin(twoFactorCode)
      await refreshUser()
      router.push('/')
    } catch (err: any) {
      setError(err.message || 'Invalid 2FA code. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleBack = () => {
    setRequires2FA(false)
    setTwoFactorCode('')
    setError('')
  }

  if (authLoading) {
    return (
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}
      >
        <CircularProgress sx={{ color: 'white' }} />
      </Box>
    )
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        py: 4,
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={24}
          sx={{
            p: 4,
            borderRadius: 3,
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
          }}
        >
          {/* Logo and Title */}
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Avatar
              sx={{
                mx: 'auto',
                mb: 2,
                bgcolor: requires2FA ? 'secondary.main' : 'primary.main',
                width: 56,
                height: 56,
              }}
            >
              {requires2FA ? <SecurityIcon /> : <LockIcon />}
            </Avatar>
            <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
              {requires2FA ? 'Two-Factor Authentication' : 'DoganSystem'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {requires2FA
                ? 'Enter the 6-digit code from your authenticator app'
                : 'AI Organization Management Platform'}
            </Typography>
          </Box>

          {/* Alerts */}
          {expired && !requires2FA && (
            <Alert severity="warning" sx={{ mb: 3 }}>
              Your session has expired. Please log in again.
            </Alert>
          )}

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* 2FA Form */}
          {requires2FA ? (
            <Box component="form" onSubmit={handle2FASubmit}>
              <TextField
                fullWidth
                label="Authentication Code"
                value={twoFactorCode}
                onChange={(e) => setTwoFactorCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                margin="normal"
                required
                autoFocus
                disabled={isLoading}
                inputProps={{
                  maxLength: 6,
                  pattern: '[0-9]*',
                  inputMode: 'numeric',
                  style: { textAlign: 'center', fontSize: '1.5rem', letterSpacing: '0.5rem' },
                }}
                placeholder="000000"
                helperText="Enter the code from your authenticator app or use a backup code"
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading || twoFactorCode.length < 6}
                sx={{
                  mt: 3,
                  mb: 2,
                  py: 1.5,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%)',
                  },
                }}
              >
                {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Verify'}
              </Button>

              <Button
                fullWidth
                variant="text"
                onClick={handleBack}
                disabled={isLoading}
                sx={{ mt: 1 }}
              >
                Back to Login
              </Button>
            </Box>
          ) : (
            /* Login Form */
            <Box component="form" onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Username or Email"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                margin="normal"
                required
                autoComplete="username"
                autoFocus
                disabled={isLoading}
              />

              <TextField
                fullWidth
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                margin="normal"
                required
                autoComplete="current-password"
                disabled={isLoading}
              />

              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      color="primary"
                      disabled={isLoading}
                    />
                  }
                  label="Remember me"
                />
                <Link href="/forgot-password" style={{ textDecoration: 'none' }}>
                  <Typography variant="body2" color="primary" sx={{ cursor: 'pointer', '&:hover': { textDecoration: 'underline' } }}>
                    Forgot password?
                  </Typography>
                </Link>
              </Box>

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading}
                sx={{
                  mt: 3,
                  mb: 2,
                  py: 1.5,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%)',
                  },
                }}
              >
                {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Sign In'}
              </Button>
            </Box>
          )}

          {/* Footer */}
          {!requires2FA && (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                Default credentials for development:
              </Typography>
              <Typography variant="caption" display="block" color="text.secondary">
                Username: <strong>admin</strong> | Password: <strong>Admin@123456</strong>
              </Typography>
            </Box>
          )}
        </Paper>

        {/* Copyright */}
        <Typography
          variant="body2"
          sx={{ textAlign: 'center', mt: 3, color: 'rgba(255,255,255,0.8)' }}
        >
          &copy; {new Date().getFullYear()} DoganSystem. All rights reserved.
        </Typography>
      </Container>
    </Box>
  )
}
