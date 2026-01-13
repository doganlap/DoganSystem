'use client'

import { useState } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  MenuItem,
  Chip,
  Avatar,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Button,
} from '@mui/material'
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
} from '@mui/icons-material'

// Sample employee data
const employees = [
  {
    id: 'emp_ceo_001',
    name: 'عبدالله المهندس',
    nameEn: 'Abdullah Al-Muhandis',
    title: 'CEO',
    department: 'Executive',
    type: 'Plan',
    status: 'available',
    tasksCompleted: 45,
  },
  {
    id: 'emp_sales_dir_001',
    name: 'محمد المبيعات',
    nameEn: 'Mohammed Al-Mabiyat',
    title: 'Sales Director',
    department: 'Sales',
    type: 'Plan',
    status: 'busy',
    tasksCompleted: 127,
  },
  {
    id: 'emp_sales_quote_001',
    name: 'نوف العروض',
    nameEn: 'Nouf Al-Orood',
    title: 'Quotation Team Lead',
    department: 'Sales',
    type: 'general-purpose',
    status: 'available',
    tasksCompleted: 89,
  },
  {
    id: 'emp_crm_analyst_001',
    name: 'ياسر التحليل',
    nameEn: 'Yasser Al-Tahlil',
    title: 'CRM Analyst',
    department: 'CRM',
    type: 'Explore',
    status: 'available',
    tasksCompleted: 56,
  },
  {
    id: 'emp_acc_dir_001',
    name: 'سعد المحاسبة',
    nameEn: 'Saad Al-Muhasaba',
    title: 'Finance Director',
    department: 'Finance',
    type: 'Plan',
    status: 'available',
    tasksCompleted: 78,
  },
]

export default function EmployeeList() {
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  const [filterDept, setFilterDept] = useState('all')
  const [filterType, setFilterType] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage)
  }

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10))
    setPage(0)
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Explore':
        return 'info'
      case 'Plan':
        return 'secondary'
      case 'general-purpose':
        return 'success'
      default:
        return 'default'
    }
  }

  const getStatusColor = (status: string) => {
    return status === 'available' ? 'success' : 'warning'
  }

  return (
    <Card>
      <CardContent>
        {/* Header */}
        <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">AI Employees</Typography>
          <Button variant="contained" color="primary">
            Create Employee
          </Button>
        </Box>

        {/* Filters */}
        <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <TextField
            placeholder="Search employees..."
            size="small"
            sx={{ minWidth: 300 }}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'action.active' }} />,
            }}
          />
          <TextField
            select
            label="Department"
            size="small"
            value={filterDept}
            onChange={(e) => setFilterDept(e.target.value)}
            sx={{ minWidth: 150 }}
          >
            <MenuItem value="all">All Departments</MenuItem>
            <MenuItem value="Executive">Executive</MenuItem>
            <MenuItem value="Sales">Sales</MenuItem>
            <MenuItem value="CRM">CRM</MenuItem>
            <MenuItem value="Finance">Finance</MenuItem>
            <MenuItem value="Inventory">Inventory</MenuItem>
          </TextField>
          <TextField
            select
            label="Type"
            size="small"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            sx={{ minWidth: 150 }}
          >
            <MenuItem value="all">All Types</MenuItem>
            <MenuItem value="Explore">Explore</MenuItem>
            <MenuItem value="Plan">Plan</MenuItem>
            <MenuItem value="general-purpose">Operations</MenuItem>
          </TextField>
        </Box>

        {/* Employee Table */}
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Employee</TableCell>
                <TableCell>Title</TableCell>
                <TableCell>Department</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Tasks</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {employees
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((employee) => (
                  <TableRow key={employee.id} hover>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Avatar sx={{ bgcolor: 'primary.main' }}>
                          {employee.nameEn[0]}
                        </Avatar>
                        <Box>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {employee.nameEn}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {employee.name}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>{employee.title}</TableCell>
                    <TableCell>
                      <Chip
                        label={employee.department}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={employee.type}
                        size="small"
                        color={getTypeColor(employee.type) as any}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={employee.status}
                        size="small"
                        color={getStatusColor(employee.status) as any}
                      />
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        {employee.tasksCompleted}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <IconButton size="small" color="primary">
                        <ViewIcon />
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

        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={employees.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </CardContent>
    </Card>
  )
}
