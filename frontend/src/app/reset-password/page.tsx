'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
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
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import {
  LockReset as ResetIcon,
  Check as CheckIcon,
  Close as CloseIcon,
} from '@mui/icons-material'
import { authApi } from '@/services/api'

export default function ResetPasswordPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const token = searchParams.get('token')
  const email = searchParams.get('email')

  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  // Password validation
  const passwordRequirements = [
    { label: 'At least 8 characters', valid: newPassword.length >= 8 },
    { label: 'At least one uppercase letter', valid: /[A-Z]/.test(newPassword) },
    { label: 'At least one lowercase letter', valid: /[a-z]/.test(newPassword) },
    { label: 'At least one number', valid: /\d/.test(newPassword) },
    { label: 'At least one special character (!@#$%^&*)', valid: /[!@#$%^&*]/.test(newPassword) },
  ]

  const isPasswordValid = passwordRequirements.every((req) => req.valid)
  const doPasswordsMatch = newPassword === confirmPassword && confirmPassword.length > 0

  useEffect(() => {
    if (!token || !email) {
      setError('Invalid or expired reset link. Please request a new password reset.')
    }
  }, [token, email])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!isPasswordValid) {
      setError('Please meet all password requirements.')
      return
    }

    if (!doPasswordsMatch) {
      setError('Passwords do not match.')
      return
    }

    if (!token || !email) {
      setError('Invalid reset link. Please request a new password reset.')
      return
    }

    setIsLoading(true)

    try {
      await authApi.resetPassword(email, token, newPassword)
      setSuccess(true)
    } catch (err: any) {
      setError(err.message || 'Failed to reset password. The link may have expired.')
    } finally {
      setIsLoading(false)
    }
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
          {/* Header */}
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Avatar
              sx={{
                mx: 'auto',
                mb: 2,
                bgcolor: success ? 'success.main' : 'primary.main',
                width: 56,
                height: 56,
              }}
            >
              {success ? <CheckIcon /> : <ResetIcon />}
            </Avatar>
            <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
              {success ? 'Password Reset!' : 'Reset Password'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {success
                ? 'Your password has been successfully reset'
                : 'Enter your new password below'}
            </Typography>
          </Box>

          {/* Alerts */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {success ? (
            <Box sx={{ textAlign: 'center' }}>
              <Alert severity="success" sx={{ mb: 3 }}>
                Your password has been reset successfully. You can now log in with your new password.
              </Alert>
              <Button
                variant="contained"
                size="large"
                onClick={() => router.push('/login')}
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%)',
                  },
                }}
              >
                Go to Login
              </Button>
            </Box>
          ) : token && email ? (
            <Box component="form" onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="New Password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                margin="normal"
                required
                autoFocus
                disabled={isLoading}
                autoComplete="new-password"
              />

              <TextField
                fullWidth
                label="Confirm New Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                margin="normal"
                required
                disabled={isLoading}
                autoComplete="new-password"
                error={confirmPassword.length > 0 && !doPasswordsMatch}
                helperText={
                  confirmPassword.length > 0 && !doPasswordsMatch
                    ? 'Passwords do not match'
                    : ''
                }
              />

              {/* Password Requirements */}
              <Box sx={{ mt: 2, mb: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Password Requirements:
                </Typography>
                <List dense>
                  {passwordRequirements.map((req, index) => (
                    <ListItem key={index} sx={{ py: 0 }}>
                      <ListItemIcon sx={{ minWidth: 32 }}>
                        {req.valid ? (
                          <CheckIcon color="success" fontSize="small" />
                        ) : (
                          <CloseIcon color="error" fontSize="small" />
                        )}
                      </ListItemIcon>
                      <ListItemText
                        primary={req.label}
                        primaryTypographyProps={{
                          variant: 'caption',
                          color: req.valid ? 'success.main' : 'text.secondary',
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading || !isPasswordValid || !doPasswordsMatch}
                sx={{
                  mt: 2,
                  mb: 2,
                  py: 1.5,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%)',
                  },
                }}
              >
                {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Reset Password'}
              </Button>

              <Button
                fullWidth
                variant="text"
                onClick={() => router.push('/login')}
                disabled={isLoading}
              >
                Back to Login
              </Button>
            </Box>
          ) : (
            <Box sx={{ textAlign: 'center' }}>
              <Button
                variant="contained"
                onClick={() => router.push('/forgot-password')}
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%)',
                  },
                }}
              >
                Request New Reset Link
              </Button>
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
