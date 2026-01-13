# Cloudflare Tunnel Configuration Steps

## Current Status
- ✅ Tunnel is RUNNING (4 active connections)
- ✅ Landing page is RUNNING on localhost:80
- ❌ Hostname routing NOT configured yet

## Step-by-Step Instructions

### 1. Navigate to Tunnels Section
1. In the left sidebar, click **"Networks"** (not "Team & Resources")
2. Click **"Tunnels"**
3. You should see your tunnel listed

### 2. Edit Public Hostname
1. Find your tunnel: **c8597b06-afa7-40a8-b406-8212e6b5337c**
2. Click on the tunnel name or the **"Configure"** button
3. You should see a **"Public Hostnames"** tab
4. Click **"Edit"** next to the doganconsult.com hostname

### 3. Update Configuration
Change these settings:
- **Subdomain**: (leave empty or enter "www")
- **Domain**: doganconsult.com
- **Type**: HTTP
- **URL**: **http://localhost:80** ⚠️ CHANGE FROM 3001 to 80
- **HTTP Host Header**: doganconsult.com

### 4. Save Changes
Click **"Save hostname"**

### 5. Test Access
Wait 30 seconds, then visit: https://doganconsult.com

---

## Quick Navigation
From current page (Devices):
1. Click **"Networks"** in the left sidebar (below "Team & Resources")
2. Click **"Tunnels"**
3. Configure your tunnel

---

## Tunnel Details
- Tunnel ID: c8597b06-afa7-40a8-b406-8212e6b5337c
- Status: Active (4 connections)
- Locations: Riyadh (ruh04), Marseille (mrs06)
- Protocol: QUIC
- Local Service: http://localhost:80 (nginx-landing container)
