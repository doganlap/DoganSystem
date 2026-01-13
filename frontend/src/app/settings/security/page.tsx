'use client'

import { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  CardActions,
  Divider,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Grid,
} from '@mui/material'
import {
  Security as SecurityIcon,
  Smartphone as PhoneIcon,
  Devices as DevicesIcon,
  Delete as DeleteIcon,
  ContentCopy as CopyIcon,
  QrCode as QrCodeIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material'
import DashboardLayout from '@/components/DashboardLayout'
import ProtectedRoute from '@/components/ProtectedRoute'
import { authApi, TwoFactorSetupResponse, SessionInfo } from '@/services/api'

export default function SecuritySettingsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // 2FA State
  const [is2FAEnabled, setIs2FAEnabled] = useState(false)
  const [setupData, setSetupData] = useState<TwoFactorSetupResponse | null>(null)
  const [showSetupDialog, setShowSetupDialog] = useState(false)
  const [showDisableDialog, setShowDisableDialog] = useState(false)
  const [showBackupCodesDialog, setShowBackupCodesDialog] = useState(false)
  const [verificationCode, setVerificationCode] = useState('')
  const [password, setPassword] = useState('')
  const [backupCodes, setBackupCodes] = useState<string[]>([])
  const [isProcessing, setIsProcessing] = useState(false)

  // Sessions State
  const [sessions, setSessions] = useState<SessionInfo[]>([])
  const [isLoadingSessions, setIsLoadingSessions] = useState(false)

  useEffect(() => {
    loadSecurityStatus()
    loadSessions()
  }, [])

  const loadSecurityStatus = async () => {
    try {
      const status = await authApi.twoFactor.getStatus()
      setIs2FAEnabled(status.isEnabled)
    } catch (err: any) {
      console.error('Failed to load 2FA status:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const loadSessions = async () => {
    setIsLoadingSessions(true)
    try {
      const sessionList = await authApi.sessions.getAll()
      setSessions(sessionList)
    } catch (err: any) {
      console.error('Failed to load sessions:', err)
    } finally {
      setIsLoadingSessions(false)
    }
  }

  const handleSetup2FA = async () => {
    setIsProcessing(true)
    setError('')
    try {
      const data = await authApi.twoFactor.setup()
      setSetupData(data)
      setShowSetupDialog(true)
    } catch (err: any) {
      setError(err.message || 'Failed to initialize 2FA setup')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleVerify2FA = async () => {
    setIsProcessing(true)
    setError('')
    try {
      const result = await authApi.twoFactor.verifySetup(verificationCode)
      setBackupCodes(result.backupCodes)
      setShowSetupDialog(false)
      setShowBackupCodesDialog(true)
      setIs2FAEnabled(true)
      setVerificationCode('')
      setSuccess('Two-factor authentication has been enabled!')
    } catch (err: any) {
      setError(err.message || 'Invalid verification code')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleDisable2FA = async () => {
    setIsProcessing(true)
    setError('')
    try {
      await authApi.twoFactor.disable(password)
      setIs2FAEnabled(false)
      setShowDisableDialog(false)
      setPassword('')
      setSuccess('Two-factor authentication has been disabled')
    } catch (err: any) {
      setError(err.message || 'Failed to disable 2FA')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleRegenerateBackupCodes = async () => {
    setIsProcessing(true)
    setError('')
    try {
      const result = await authApi.twoFactor.regenerateBackupCodes(password)
      setBackupCodes(result.backupCodes)
      setShowBackupCodesDialog(true)
      setShowDisableDialog(false)
      setPassword('')
      setSuccess('New backup codes have been generated')
    } catch (err: any) {
      setError(err.message || 'Failed to regenerate backup codes')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleRevokeSession = async (sessionId: string) => {
    try {
      await authApi.sessions.revoke(sessionId)
      setSessions(sessions.filter((s) => s.sessionId !== sessionId))
      setSuccess('Session has been revoked')
    } catch (err: any) {
      setError(err.message || 'Failed to revoke session')
    }
  }

  const handleRevokeAllSessions = async () => {
    try {
      await authApi.sessions.revokeAll()
      setSessions([])
      setSuccess('All other sessions have been revoked')
    } catch (err: any) {
      setError(err.message || 'Failed to revoke sessions')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    setSuccess('Copied to clipboard!')
  }

  if (isLoading) {
    return (
      <ProtectedRoute>
        <DashboardLayout>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
            <CircularProgress />
          </Box>
        </DashboardLayout>
      </ProtectedRoute>
    )
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <Container maxWidth="lg">
          {/* Header */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <SecurityIcon />
              Security Settings
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Manage your account security, two-factor authentication, and active sessions
            </Typography>
          </Box>

          {/* Alerts */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess('')}>
              {success}
            </Alert>
          )}

          <Grid container spacing={3}>
            {/* Two-Factor Authentication */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <PhoneIcon color="primary" />
                    <Box>
                      <Typography variant="h6">Two-Factor Authentication</Typography>
                      <Typography variant="body2" color="text.secondary">
                        Add an extra layer of security to your account
                      </Typography>
                    </Box>
                    <Chip
                      label={is2FAEnabled ? 'Enabled' : 'Disabled'}
                      color={is2FAEnabled ? 'success' : 'default'}
                      size="small"
                      sx={{ ml: 'auto' }}
                    />
                  </Box>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    {is2FAEnabled
                      ? 'Your account is protected with two-factor authentication using an authenticator app.'
                      : 'Enable two-factor authentication to require a verification code from your authenticator app when signing in.'}
                  </Typography>
                </CardContent>
                <CardActions>
                  {is2FAEnabled ? (
                    <>
                      <Button
                        variant="outlined"
                        color="error"
                        onClick={() => setShowDisableDialog(true)}
                        disabled={isProcessing}
                      >
                        Disable 2FA
                      </Button>
                      <Button
                        variant="outlined"
                        onClick={() => {
                          setShowDisableDialog(true)
                        }}
                        disabled={isProcessing}
                      >
                        View Backup Codes
                      </Button>
                    </>
                  ) : (
                    <Button
                      variant="contained"
                      onClick={handleSetup2FA}
                      disabled={isProcessing}
                      startIcon={isProcessing ? <CircularProgress size={20} /> : <PhoneIcon />}
                    >
                      Enable 2FA
                    </Button>
                  )}
                </CardActions>
              </Card>
            </Grid>

            {/* Active Sessions */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <DevicesIcon color="primary" />
                    <Box>
                      <Typography variant="h6">Active Sessions</Typography>
                      <Typography variant="body2" color="text.secondary">
                        Manage devices where you're logged in
                      </Typography>
                    </Box>
                    <IconButton onClick={loadSessions} disabled={isLoadingSessions} sx={{ ml: 'auto' }}>
                      <RefreshIcon />
                    </IconButton>
                  </Box>
                </CardContent>
                <Divider />
                {isLoadingSessions ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                    <CircularProgress size={24} />
                  </Box>
                ) : sessions.length === 0 ? (
                  <Box sx={{ p: 3, textAlign: 'center' }}>
                    <Typography variant="body2" color="text.secondary">
                      No active sessions found
                    </Typography>
                  </Box>
                ) : (
                  <List>
                    {sessions.map((session) => (
                      <ListItem key={session.sessionId} divider>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              {session.deviceInfo}
                              {session.isCurrent && (
                                <Chip label="Current" color="primary" size="small" />
                              )}
                            </Box>
                          }
                          secondary={
                            <>
                              IP: {session.ipAddress} | Last active:{' '}
                              {new Date(session.lastActivity).toLocaleString()}
                            </>
                          }
                        />
                        {!session.isCurrent && (
                          <ListItemSecondaryAction>
                            <IconButton
                              edge="end"
                              color="error"
                              onClick={() => handleRevokeSession(session.sessionId)}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </ListItemSecondaryAction>
                        )}
                      </ListItem>
                    ))}
                  </List>
                )}
                {sessions.length > 1 && (
                  <CardActions>
                    <Button color="error" onClick={handleRevokeAllSessions}>
                      Revoke All Other Sessions
                    </Button>
                  </CardActions>
                )}
              </Card>
            </Grid>
          </Grid>

          {/* 2FA Setup Dialog */}
          <Dialog open={showSetupDialog} onClose={() => setShowSetupDialog(false)} maxWidth="sm" fullWidth>
            <DialogTitle>Set Up Two-Factor Authentication</DialogTitle>
            <DialogContent>
              {setupData && (
                <>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    1. Scan this QR code with your authenticator app (Google Authenticator, Authy, etc.)
                  </Typography>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      mb: 2,
                      p: 2,
                      bgcolor: 'grey.100',
                      borderRadius: 1,
                    }}
                  >
                    <Box sx={{ textAlign: 'center' }}>
                      <QrCodeIcon sx={{ fontSize: 120, color: 'grey.400' }} />
                      <Typography variant="caption" display="block" color="text.secondary">
                        QR Code will be displayed here
                      </Typography>
                      <Typography variant="caption" display="block" sx={{ wordBreak: 'break-all' }}>
                        {setupData.qrCodeUri}
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    Or enter this secret key manually:
                  </Typography>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1,
                      mb: 3,
                      p: 1,
                      bgcolor: 'grey.100',
                      borderRadius: 1,
                    }}
                  >
                    <Typography variant="body2" sx={{ fontFamily: 'monospace', flex: 1 }}>
                      {setupData.secretKey}
                    </Typography>
                    <IconButton size="small" onClick={() => copyToClipboard(setupData.secretKey)}>
                      <CopyIcon fontSize="small" />
                    </IconButton>
                  </Box>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    2. Enter the 6-digit code from your authenticator app to verify:
                  </Typography>
                  <TextField
                    fullWidth
                    label="Verification Code"
                    value={verificationCode}
                    onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                    inputProps={{
                      maxLength: 6,
                      pattern: '[0-9]*',
                      inputMode: 'numeric',
                      style: { textAlign: 'center', fontSize: '1.5rem', letterSpacing: '0.5rem' },
                    }}
                    placeholder="000000"
                  />
                </>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setShowSetupDialog(false)}>Cancel</Button>
              <Button
                variant="contained"
                onClick={handleVerify2FA}
                disabled={verificationCode.length !== 6 || isProcessing}
              >
                {isProcessing ? <CircularProgress size={24} /> : 'Verify & Enable'}
              </Button>
            </DialogActions>
          </Dialog>

          {/* Disable 2FA / Regenerate Backup Codes Dialog */}
          <Dialog open={showDisableDialog} onClose={() => setShowDisableDialog(false)} maxWidth="sm" fullWidth>
            <DialogTitle>Manage Two-Factor Authentication</DialogTitle>
            <DialogContent>
              <Typography variant="body2" sx={{ mb: 2 }}>
                Enter your password to continue:
              </Typography>
              <TextField
                fullWidth
                type="password"
                label="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setShowDisableDialog(false)}>Cancel</Button>
              <Button
                variant="outlined"
                onClick={handleRegenerateBackupCodes}
                disabled={!password || isProcessing}
              >
                Regenerate Backup Codes
              </Button>
              <Button
                variant="contained"
                color="error"
                onClick={handleDisable2FA}
                disabled={!password || isProcessing}
              >
                {isProcessing ? <CircularProgress size={24} /> : 'Disable 2FA'}
              </Button>
            </DialogActions>
          </Dialog>

          {/* Backup Codes Dialog */}
          <Dialog open={showBackupCodesDialog} onClose={() => setShowBackupCodesDialog(false)} maxWidth="sm" fullWidth>
            <DialogTitle>Backup Codes</DialogTitle>
            <DialogContent>
              <Alert severity="warning" sx={{ mb: 2 }}>
                Save these backup codes in a safe place. Each code can only be used once. If you lose access to
                your authenticator app, you can use these codes to sign in.
              </Alert>
              <Box
                sx={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(2, 1fr)',
                  gap: 1,
                  p: 2,
                  bgcolor: 'grey.100',
                  borderRadius: 1,
                  fontFamily: 'monospace',
                }}
              >
                {backupCodes.map((code, index) => (
                  <Typography key={index} variant="body2">
                    {code}
                  </Typography>
                ))}
              </Box>
              <Button
                fullWidth
                startIcon={<CopyIcon />}
                onClick={() => copyToClipboard(backupCodes.join('\n'))}
                sx={{ mt: 2 }}
              >
                Copy All Codes
              </Button>
            </DialogContent>
            <DialogActions>
              <Button variant="contained" onClick={() => setShowBackupCodesDialog(false)}>
                Done
              </Button>
            </DialogActions>
          </Dialog>
        </Container>
      </DashboardLayout>
    </ProtectedRoute>
  )
}
