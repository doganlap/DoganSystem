'use client'

import { useState } from 'react'
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Avatar,
  Chip,
  IconButton,
  Tabs,
  Tab,
} from '@mui/material'
import {
  Group as GroupIcon,
  Work as WorkIcon,
  Assessment as AssessmentIcon,
  AccountTree as OrgChartIcon,
  PlayArrow as PlayIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material'
import DashboardLayout from '@/components/DashboardLayout'
import StatsCard from '@/components/StatsCard'
import EmployeeList from '@/components/EmployeeList'
import WorkflowList from '@/components/WorkflowList'
import OrgChartView from '@/components/OrgChartView'
import TaskMonitor from '@/components/TaskMonitor'
import ProtectedRoute from '@/components/ProtectedRoute'
import { useAuth } from '@/contexts/AuthContext'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  )
}

export default function Home() {
  const [tabValue, setTabValue] = useState(0)
  const { user } = useAuth()

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue)
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
      <Container maxWidth="xl">
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h3" gutterBottom>
            AI Organization Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Welcome back, {user?.name || user?.userName || 'User'}! Manage your ERPNext AI employees and automated workflows.
          </Typography>
        </Box>

        {/* Stats Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Total Employees"
              value="80+"
              icon={<GroupIcon />}
              color="primary"
              trend="+12%"
              trendLabel="from last month"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Active Workflows"
              value="42"
              icon={<WorkIcon />}
              color="success"
              trend="8 running"
              trendLabel="right now"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Tasks Completed"
              value="1,247"
              icon={<AssessmentIcon />}
              color="warning"
              trend="+23%"
              trendLabel="this week"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Departments"
              value="12"
              icon={<OrgChartIcon />}
              color="secondary"
              trend="100%"
              trendLabel="coverage"
            />
          </Grid>
        </Grid>

        {/* Main Content Tabs */}
        <Paper sx={{ width: '100%' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              variant="scrollable"
              scrollButtons="auto"
            >
              <Tab label="Overview" />
              <Tab label="Employees" />
              <Tab label="Workflows" />
              <Tab label="Organization Chart" />
              <Tab label="Task Monitor" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            {/* Overview Dashboard */}
            <Grid container spacing={3}>
              {/* Department Summary */}
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Department Overview
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                      {[
                        { name: 'Sales', count: 14, color: '#667eea' },
                        { name: 'Finance', count: 9, color: '#764ba2' },
                        { name: 'Inventory', count: 9, color: '#10b981' },
                        { name: 'CRM', count: 8, color: '#f59e0b' },
                        { name: 'HR', count: 7, color: '#ef4444' },
                      ].map((dept) => (
                        <Box
                          key={dept.name}
                          sx={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            mb: 2,
                          }}
                        >
                          <Typography variant="body1">{dept.name}</Typography>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            <Box
                              sx={{
                                width: 100,
                                height: 8,
                                bgcolor: 'grey.200',
                                borderRadius: 1,
                                overflow: 'hidden',
                              }}
                            >
                              <Box
                                sx={{
                                  width: `${(dept.count / 14) * 100}%`,
                                  height: '100%',
                                  bgcolor: dept.color,
                                }}
                              />
                            </Box>
                            <Typography variant="body2" sx={{ minWidth: 30 }}>
                              {dept.count}
                            </Typography>
                          </Box>
                        </Box>
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              {/* Recent Activity */}
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Recent Activity
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                      {[
                        {
                          time: '2 mins ago',
                          action: 'Sales quotation follow-up completed',
                          employee: 'Nouf Al-Orood',
                        },
                        {
                          time: '15 mins ago',
                          action: 'Monthly payroll processed',
                          employee: 'Rana Al-Rawatib',
                        },
                        {
                          time: '1 hour ago',
                          action: 'Stock reconciliation completed',
                          employee: 'Jawaher Al-Jard',
                        },
                        {
                          time: '2 hours ago',
                          action: 'CRM pipeline analysis finished',
                          employee: 'Yasser Al-Tahlil',
                        },
                      ].map((activity, idx) => (
                        <Box
                          key={idx}
                          sx={{
                            display: 'flex',
                            gap: 2,
                            mb: 2,
                            pb: 2,
                            borderBottom:
                              idx < 3 ? '1px solid' : 'none',
                            borderColor: 'divider',
                          }}
                        >
                          <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                            {activity.employee[0]}
                          </Avatar>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="body2">
                              {activity.action}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              by {activity.employee} • {activity.time}
                            </Typography>
                          </Box>
                        </Box>
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <EmployeeList />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <WorkflowList />
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <OrgChartView />
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            <TaskMonitor />
          </TabPanel>
        </Paper>
      </Container>
      </DashboardLayout>
    </ProtectedRoute>
  )
}
