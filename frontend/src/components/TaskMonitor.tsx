'use client'

import { useState } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  LinearProgress,
  Avatar,
  Tab,
  Tabs,
} from '@mui/material'
import {
  CheckCircle as CompletedIcon,
  HourglassEmpty as PendingIcon,
  Error as ErrorIcon,
} from '@mui/icons-material'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props

  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 2 }}>{children}</Box>}
    </div>
  )
}

// Sample task data
const tasks = {
  active: [
    {
      id: 'task_001',
      name: 'Processing monthly sales closing',
      employee: 'Mohammed Al-Mabiyat',
      department: 'Sales',
      progress: 75,
      startedAt: '10 mins ago',
    },
    {
      id: 'task_002',
      name: 'Analyzing inventory movements',
      employee: 'Fahad Al-Tahlil',
      department: 'Inventory',
      progress: 45,
      startedAt: '25 mins ago',
    },
  ],
  completed: [
    {
      id: 'task_003',
      name: 'Daily lead processing',
      employee: 'Ahmed Al-Furas',
      department: 'CRM',
      completedAt: '1 hour ago',
      duration: '5 mins',
    },
    {
      id: 'task_004',
      name: 'Stock level check',
      employee: 'Latifa Al-Mustawda\'at',
      department: 'Inventory',
      completedAt: '2 hours ago',
      duration: '3 mins',
    },
  ],
  failed: [
    {
      id: 'task_005',
      name: 'Payment matching',
      employee: 'Ghada Al-Madyooneen',
      department: 'Finance',
      failedAt: '3 hours ago',
      error: 'Connection timeout to ERPNext API',
    },
  ],
}

export default function TaskMonitor() {
  const [tabValue, setTabValue] = useState(0)

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue)
  }

  return (
    <Card>
      <CardContent>
        {/* Header */}
        <Typography variant="h5" gutterBottom>
          Task Monitor
        </Typography>

        {/* Summary Stats */}
        <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
          <Chip
            icon={<HourglassEmpty />}
            label={`${tasks.active.length} Active`}
            color="primary"
          />
          <Chip
            icon={<CompletedIcon />}
            label={`${tasks.completed.length} Completed`}
            color="success"
          />
          <Chip
            icon={<ErrorIcon />}
            label={`${tasks.failed.length} Failed`}
            color="error"
          />
        </Box>

        {/* Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Active Tasks" />
            <Tab label="Completed" />
            <Tab label="Failed" />
          </Tabs>
        </Box>

        {/* Active Tasks */}
        <TabPanel value={tabValue} index={0}>
          {tasks.active.map((task) => (
            <Box
              key={task.id}
              sx={{
                p: 2,
                mb: 2,
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 1,
              }}
            >
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                    {task.employee[0]}
                  </Avatar>
                  <Box>
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>
                      {task.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {task.employee} • {task.department}
                    </Typography>
                  </Box>
                </Box>
                <Chip label={task.startedAt} size="small" variant="outlined" />
              </Box>
              <Box sx={{ mt: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="caption">Progress</Typography>
                  <Typography variant="caption">{task.progress}%</Typography>
                </Box>
                <LinearProgress variant="determinate" value={task.progress} />
              </Box>
            </Box>
          ))}
        </TabPanel>

        {/* Completed Tasks */}
        <TabPanel value={tabValue} index={1}>
          {tasks.completed.map((task) => (
            <Box
              key={task.id}
              sx={{
                p: 2,
                mb: 2,
                border: '1px solid',
                borderColor: 'success.light',
                borderRadius: 1,
                bgcolor: 'success.50',
              }}
            >
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'success.main', width: 32, height: 32 }}>
                    <CompletedIcon fontSize="small" />
                  </Avatar>
                  <Box>
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>
                      {task.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {task.employee} • {task.department} • Duration: {task.duration}
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="caption" color="text.secondary">
                  {task.completedAt}
                </Typography>
              </Box>
            </Box>
          ))}
        </TabPanel>

        {/* Failed Tasks */}
        <TabPanel value={tabValue} index={2}>
          {tasks.failed.map((task) => (
            <Box
              key={task.id}
              sx={{
                p: 2,
                mb: 2,
                border: '1px solid',
                borderColor: 'error.light',
                borderRadius: 1,
                bgcolor: 'error.50',
              }}
            >
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'error.main', width: 32, height: 32 }}>
                    <ErrorIcon fontSize="small" />
                  </Avatar>
                  <Box>
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>
                      {task.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {task.employee} • {task.department}
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="caption" color="text.secondary">
                  {task.failedAt}
                </Typography>
              </Box>
              <Typography variant="caption" color="error.main">
                Error: {task.error}
              </Typography>
            </Box>
          ))}
        </TabPanel>
      </CardContent>
    </Card>
  )
}
