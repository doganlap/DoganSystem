'use client'

import { useState } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material'
import {
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Edit as EditIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material'

// Sample workflow data
const workflows = [
  {
    id: 'crm_lead_processing',
    name: 'Daily Lead Processing',
    department: 'CRM',
    schedule: 'Daily 9:00 AM',
    lastRun: '2 hours ago',
    status: 'enabled',
    executions: 145,
    assignedTo: 'Lead Management Team Lead',
  },
  {
    id: 'sales_quotation_followup',
    name: 'Quotation Follow-up',
    department: 'Sales',
    schedule: 'Daily 10:00 AM',
    lastRun: '1 hour ago',
    status: 'enabled',
    executions: 203,
    assignedTo: 'Quotation Team Lead',
  },
  {
    id: 'acc_month_end',
    name: 'Month-End Close',
    department: 'Finance',
    schedule: 'Monthly (Last day)',
    lastRun: '5 days ago',
    status: 'enabled',
    executions: 12,
    assignedTo: 'Finance Director',
  },
  {
    id: 'inv_stock_check',
    name: 'Daily Stock Level Check',
    department: 'Inventory',
    schedule: 'Daily 7:00 AM',
    lastRun: '5 hours ago',
    status: 'enabled',
    executions: 187,
    assignedTo: 'Warehouse Management Lead',
  },
  {
    id: 'hr_payroll_processing',
    name: 'Monthly Payroll',
    department: 'HR',
    schedule: 'Monthly (25th)',
    lastRun: '10 days ago',
    status: 'enabled',
    executions: 8,
    assignedTo: 'Payroll Lead',
  },
]

export default function WorkflowList() {
  const [executeDialogOpen, setExecuteDialogOpen] = useState(false)
  const [selectedWorkflow, setSelectedWorkflow] = useState<string>('')

  const handleExecute = (workflowId: string) => {
    setSelectedWorkflow(workflowId)
    setExecuteDialogOpen(true)
  }

  const handleCloseDialog = () => {
    setExecuteDialogOpen(false)
    setSelectedWorkflow('')
  }

  const handleConfirmExecute = () => {
    // Execute workflow
    console.log('Executing workflow:', selectedWorkflow)
    handleCloseDialog()
  }

  const getStatusColor = (status: string) => {
    return status === 'enabled' ? 'success' : 'default'
  }

  const getDepartmentColor = (dept: string) => {
    const colors: Record<string, any> = {
      CRM: 'primary',
      Sales: 'secondary',
      Finance: 'warning',
      Inventory: 'success',
      HR: 'error',
    }
    return colors[dept] || 'default'
  }

  return (
    <>
      <Card>
        <CardContent>
          {/* Header */}
          <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5">Automated Workflows</Typography>
            <Button variant="contained" color="primary">
              Create Workflow
            </Button>
          </Box>

          {/* Workflow Table */}
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Workflow Name</TableCell>
                  <TableCell>Department</TableCell>
                  <TableCell>Schedule</TableCell>
                  <TableCell>Assigned To</TableCell>
                  <TableCell>Last Run</TableCell>
                  <TableCell align="right">Executions</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {workflows.map((workflow) => (
                  <TableRow key={workflow.id} hover>
                    <TableCell>
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 600 }}>
                          {workflow.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {workflow.id}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={workflow.department}
                        size="small"
                        color={getDepartmentColor(workflow.department)}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <ScheduleIcon fontSize="small" color="action" />
                        <Typography variant="body2">{workflow.schedule}</Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{workflow.assignedTo}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" color="text.secondary">
                        {workflow.lastRun}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        {workflow.executions}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={workflow.status}
                        size="small"
                        color={getStatusColor(workflow.status) as any}
                      />
                    </TableCell>
                    <TableCell align="right">
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => handleExecute(workflow.id)}
                      >
                        <PlayIcon />
                      </IconButton>
                      <IconButton size="small">
                        <EditIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Execute Workflow Dialog */}
      <Dialog open={executeDialogOpen} onClose={handleCloseDialog}>
        <DialogTitle>Execute Workflow</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Are you sure you want to execute this workflow now?
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Workflow ID: {selectedWorkflow}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleConfirmExecute}
            variant="contained"
            color="primary"
            startIcon={<PlayIcon />}
          >
            Execute Now
          </Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
