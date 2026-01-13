'use client'

import { useState } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  ButtonGroup,
  Paper,
} from '@mui/material'
import {
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
  CenterFocusStrong as CenterIcon,
} from '@mui/icons-material'

// Simplified org chart component (you can integrate react-flow or d3 later)
export default function OrgChartView() {
  const [zoom, setZoom] = useState(1)

  const handleZoomIn = () => setZoom((prev) => Math.min(prev + 0.1, 2))
  const handleZoomOut = () => setZoom((prev) => Math.max(prev - 0.1, 0.5))
  const handleReset = () => setZoom(1)

  // Simplified org structure
  const orgStructure = {
    ceo: {
      name: 'Abdullah Al-Muhandis',
      title: 'CEO',
      reports: [
        {
          name: 'Noura Al-Tiqniya',
          title: 'CTO',
          reports: [
            { name: 'Ali Al-Tiqniya', title: 'IT Director' },
          ],
        },
        {
          name: 'Khaled Al-Mali',
          title: 'CFO',
          reports: [
            { name: 'Saad Al-Muhasaba', title: 'Finance Director' },
            { name: 'Faisal Al-Usool', title: 'Assets Director' },
          ],
        },
        {
          name: 'Reem Al-Amaliyat',
          title: 'COO',
          reports: [
            { name: 'Sarah Al-Omala', title: 'CRM Director' },
            { name: 'Mohammed Al-Mabiyat', title: 'Sales Director' },
            { name: 'Tariq Al-Mushtarayat', title: 'Procurement Director' },
            { name: 'Rashed Al-Makhzoon', title: 'Inventory Director' },
          ],
        },
      ],
    },
  }

  const renderNode = (node: any, level: number = 0) => (
    <Box
      key={node.name}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        mb: 4,
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: 2,
          minWidth: 200,
          textAlign: 'center',
          bgcolor: level === 0 ? 'primary.main' : 'background.paper',
          color: level === 0 ? 'white' : 'text.primary',
          border: level > 0 ? '2px solid' : 'none',
          borderColor: 'primary.light',
        }}
      >
        <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
          {node.name}
        </Typography>
        <Typography variant="caption">{node.title}</Typography>
      </Paper>

      {node.reports && node.reports.length > 0 && (
        <Box
          sx={{
            display: 'flex',
            gap: 3,
            mt: 4,
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}
        >
          {node.reports.map((report: any) => renderNode(report, level + 1))}
        </Box>
      )}
    </Box>
  )

  return (
    <Card>
      <CardContent>
        {/* Header */}
        <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">Organization Chart</Typography>
          <ButtonGroup size="small">
            <Button onClick={handleZoomOut} startIcon={<ZoomOutIcon />}>
              Zoom Out
            </Button>
            <Button onClick={handleReset} startIcon={<CenterIcon />}>
              Reset
            </Button>
            <Button onClick={handleZoomIn} startIcon={<ZoomInIcon />}>
              Zoom In
            </Button>
          </ButtonGroup>
        </Box>

        {/* Org Chart */}
        <Box
          sx={{
            overflow: 'auto',
            maxHeight: 600,
            p: 3,
            transform: `scale(${zoom})`,
            transformOrigin: 'top center',
            transition: 'transform 0.3s',
          }}
        >
          {renderNode(orgStructure.ceo)}
        </Box>

        {/* Stats */}
        <Box
          sx={{
            mt: 3,
            p: 2,
            bgcolor: 'grey.100',
            borderRadius: 1,
            display: 'flex',
            justifyContent: 'space-around',
          }}
        >
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6">4</Typography>
            <Typography variant="caption">C-Level</Typography>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6">12</Typography>
            <Typography variant="caption">Directors</Typography>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6">25</Typography>
            <Typography variant="caption">Team Leads</Typography>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6">40+</Typography>
            <Typography variant="caption">Specialists</Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  )
}
