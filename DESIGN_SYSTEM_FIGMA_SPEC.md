# Design System - Figma Specification
## Enterprise Front-End Design System for DoganSystem

---

## 🎨 Design System Overview

This document provides the complete specification for designing the DoganSystem front-end in Figma, ensuring consistency, scalability, and enterprise-grade branding.

---

## 📐 Figma File Structure

### 1. **Design Tokens** (Foundation Layer)
```
📁 01_Design_Tokens
  ├── 📁 Colors
  │   ├── Primary Palette
  │   ├── Secondary Palette
  │   ├── Neutral Palette
  │   ├── Semantic Colors (Success, Warning, Error, Info)
  │   └── Gradients
  ├── 📁 Typography
  │   ├── Font Families
  │   ├── Font Sizes (Scale)
  │   ├── Font Weights
  │   ├── Line Heights
  │   └── Letter Spacing
  ├── 📁 Spacing
  │   ├── Base Unit (4px/8px grid)
  │   ├── Scale (0-128px)
  │   └── Layout Spacing
  ├── 📁 Shadows
  │   ├── Elevation Levels (0-24)
  │   └── Custom Shadows
  ├── 📁 Borders
  │   ├── Radius Scale
  │   ├── Width Scale
  │   └── Styles
  ├── 📁 Breakpoints
  │   ├── Mobile (320-767px)
  │   ├── Tablet (768-1023px)
  │   ├── Desktop (1024-1439px)
  │   └── Large Desktop (1440px+)
  └── 📁 Animation
      ├── Duration Scale
      ├── Easing Functions
      └── Motion Principles
```

### 2. **Components** (Component Library)
```
📁 02_Components
  ├── 📁 Primitives
  │   ├── Button (Variants: Primary, Secondary, Tertiary, Ghost, Danger)
  │   ├── Input (Text, Number, Email, Password, Textarea, Select)
  │   ├── Checkbox
  │   ├── Radio
  │   ├── Switch
  │   ├── Badge
  │   ├── Avatar
  │   ├── Icon
  │   └── Divider
  ├── 📁 Navigation
  │   ├── Navbar
  │   ├── Sidebar
  │   ├── Breadcrumbs
  │   ├── Tabs
  │   ├── Pagination
  │   └── Menu
  ├── 📁 Data Display
  │   ├── Table
  │   ├── Card
  │   ├── List
  │   ├── Stat Card
  │   ├── Chart Container
  │   └── Timeline
  ├── 📁 Feedback
  │   ├── Alert
  │   ├── Toast/Notification
  │   ├── Loading Spinner
  │   ├── Progress Bar
  │   ├── Skeleton
  │   └── Empty State
  ├── 📁 Overlay
  │   ├── Modal
  │   ├── Drawer
  │   ├── Dropdown
  │   ├── Tooltip
  │   └── Popover
  ├── 📁 Forms
  │   ├── Form Field
  │   ├── Form Group
  │   ├── Date Picker
  │   ├── Time Picker
  │   ├── File Upload
  │   └── Search
  └── 📁 Layout
      ├── Container
      ├── Grid
      ├── Stack
      └── Section
```

### 3. **Patterns** (Composed Components)
```
📁 03_Patterns
  ├── 📁 Dashboard
  │   ├── Dashboard Layout
  │   ├── Stats Overview
  │   ├── Activity Feed
  │   └── Quick Actions
  ├── 📁 Data Management
  │   ├── Data Table with Filters
  │   ├── Form Wizard
  │   ├── Bulk Actions
  │   └── Advanced Search
  ├── 📁 User Management
  │   ├── User Profile
  │   ├── User List
  │   └── Permission Matrix
  └── 📁 Workflows
      ├── Workflow Builder
      ├── Task Board
      └── Progress Tracker
```

### 4. **Pages** (Full Page Designs)
```
📁 04_Pages
  ├── 📁 Authentication
  │   ├── Login
  │   ├── Register
  │   ├── Forgot Password
  │   └── Reset Password
  ├── 📁 Dashboard
  │   ├── Main Dashboard
  │   ├── Analytics Dashboard
  │   └── Executive Dashboard
  ├── 📁 Employee Management
  │   ├── Employee List
  │   ├── Employee Detail
  │   └── Employee Create/Edit
  ├── 📁 Consultant Offers
  │   ├── Offers List
  │   ├── Offer Detail
  │   └── Offer Create/Edit
  ├── 📁 ERPNext Integration
  │   ├── Instance Management
  │   ├── Sync Status
  │   └── Configuration
  └── 📁 Settings
      ├── General Settings
      ├── User Preferences
      └── System Configuration
```

### 5. **Branding** (Visual Identity)
```
📁 05_Branding
  ├── Logo Variations
  ├── Color Usage Guidelines
  ├── Typography Guidelines
  ├── Icon Library
  ├── Illustration Style
  └── Photography Style
```

---

## 🎨 Design Tokens Specification

### Color System

#### Primary Palette
```figma
Primary-50:  #F0F9FF (Lightest)
Primary-100: #E0F2FE
Primary-200: #BAE6FD
Primary-300: #7DD3FC
Primary-400: #38BDF8
Primary-500: #0EA5E9 (Base)
Primary-600: #0284C7
Primary-700: #0369A1
Primary-800: #075985
Primary-900: #0C4A6E (Darkest)
```

#### Secondary Palette (KSA/Enterprise Theme)
```figma
Secondary-50:  #FDF4F4
Secondary-100: #FCE8E8
Secondary-200: #F9D1D1
Secondary-300: #F4AAAA
Secondary-400: #ED7A7A
Secondary-500: #E53E3E (Base - Saudi Green)
Secondary-600: #C53030
Secondary-700: #9B2C2C
Secondary-800: #742A2A
Secondary-900: #63171B
```

#### Neutral Palette
```figma
Neutral-50:  #FAFAFA
Neutral-100: #F5F5F5
Neutral-200: #E5E5E5
Neutral-300: #D4D4D4
Neutral-400: #A3A3A3
Neutral-500: #737373
Neutral-600: #525252
Neutral-700: #404040
Neutral-800: #262626
Neutral-900: #171717
```

#### Semantic Colors
```figma
Success: #10B981
Warning: #F59E0B
Error: #EF4444
Info: #3B82F6
```

### Typography System

#### Font Families
```figma
Primary Font: Inter (Sans-serif)
  - Weights: 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold)
  
Secondary Font: IBM Plex Sans Arabic (RTL Support)
  - Weights: 400, 500, 600, 700
  
Monospace: JetBrains Mono
  - Weights: 400, 500
```

#### Type Scale
```figma
Display-1: 72px / 80px / -0.02em (Bold)
Display-2: 60px / 68px / -0.02em (Bold)
H1: 48px / 56px / -0.02em (Bold)
H2: 36px / 44px / -0.02em (Bold)
H3: 30px / 38px / -0.01em (SemiBold)
H4: 24px / 32px / -0.01em (SemiBold)
H5: 20px / 28px / 0em (Medium)
H6: 18px / 26px / 0em (Medium)
Body-Large: 18px / 28px / 0em (Regular)
Body: 16px / 24px / 0em (Regular)
Body-Small: 14px / 20px / 0em (Regular)
Caption: 12px / 16px / 0.01em (Regular)
Label: 14px / 20px / 0.01em (Medium)
```

### Spacing System (8px Base Unit)
```figma
0: 0px
1: 4px
2: 8px
3: 12px
4: 16px
5: 20px
6: 24px
8: 32px
10: 40px
12: 48px
16: 64px
20: 80px
24: 96px
32: 128px
```

### Border Radius
```figma
None: 0px
Small: 4px
Medium: 8px
Large: 12px
XLarge: 16px
Full: 9999px (Pill)
```

### Shadows (Elevation)
```figma
Level 0: none
Level 1: 0px 1px 2px rgba(0,0,0,0.05)
Level 2: 0px 1px 3px rgba(0,0,0,0.1), 0px 1px 2px rgba(0,0,0,0.06)
Level 3: 0px 4px 6px rgba(0,0,0,0.07), 0px 2px 4px rgba(0,0,0,0.06)
Level 4: 0px 10px 15px rgba(0,0,0,0.1), 0px 4px 6px rgba(0,0,0,0.05)
Level 5: 0px 20px 25px rgba(0,0,0,0.1), 0px 10px 10px rgba(0,0,0,0.04)
```

---

## 🧩 Component Specifications

### Button Component

#### Variants
1. **Primary Button**
   - Background: Primary-500
   - Text: White
   - Hover: Primary-600
   - Active: Primary-700
   - Disabled: Neutral-200, Text: Neutral-400

2. **Secondary Button**
   - Background: Transparent
   - Border: 1px Primary-500
   - Text: Primary-500
   - Hover: Primary-50 background

3. **Tertiary Button**
   - Background: Transparent
   - Text: Primary-500
   - Hover: Primary-50 background

4. **Ghost Button**
   - Background: Transparent
   - Text: Neutral-700
   - Hover: Neutral-100 background

5. **Danger Button**
   - Background: Error
   - Text: White
   - Hover: Darker Error

#### Sizes
- Small: 32px height, 12px padding, 14px font
- Medium: 40px height, 16px padding, 16px font (Default)
- Large: 48px height, 20px padding, 18px font

#### States
- Default, Hover, Active, Focus, Disabled, Loading

### Input Component

#### Structure
- Label (14px, Medium, Neutral-700)
- Input Field (16px height, 16px padding, Border: Neutral-300)
- Helper Text (12px, Neutral-500)
- Error State (Border: Error, Error Text)

#### Variants
- Text, Number, Email, Password, Textarea, Select, Search

#### States
- Default, Focus, Error, Disabled, Read-only

### Card Component

#### Variants
1. **Default Card**
   - Background: White
   - Border: 1px Neutral-200
   - Shadow: Level 1
   - Padding: 24px
   - Radius: 12px

2. **Elevated Card**
   - Shadow: Level 3
   - No border

3. **Outlined Card**
   - Border: 1px Neutral-200
   - No shadow

---

## 📱 Responsive Breakpoints

```figma
Mobile: 320px - 767px
  - Single column layout
  - Stacked components
  - Bottom navigation

Tablet: 768px - 1023px
  - 2-column grid
  - Sidebar navigation
  - Adjusted spacing

Desktop: 1024px - 1439px
  - 3-4 column grid
  - Full sidebar
  - Optimal spacing

Large Desktop: 1440px+
  - 4+ column grid
  - Max-width container
  - Enhanced spacing
```

---

## 🌐 RTL (Right-to-Left) Support

### Arabic Language Considerations
- Mirror all layouts for RTL
- Text alignment: Right for Arabic
- Icon positioning: Flipped
- Navigation: Right-to-left flow
- Form fields: Right-aligned labels

---

## 🎭 Animation & Motion

### Duration Scale
```figma
Instant: 0ms
Fast: 150ms
Normal: 250ms
Slow: 350ms
Slower: 500ms
```

### Easing Functions
```figma
Ease In: cubic-bezier(0.4, 0, 1, 1)
Ease Out: cubic-bezier(0, 0, 0.2, 1)
Ease In Out: cubic-bezier(0.4, 0, 0.2, 1)
```

### Motion Principles
- **Micro-interactions**: 150ms for hover states
- **Page transitions**: 250ms for route changes
- **Modal/Drawer**: 300ms for open/close
- **Loading states**: 500ms for skeleton animations

---

## 📋 Figma Best Practices

### 1. **Component Organization**
- Use Auto Layout for all components
- Create variants for different states
- Use component properties for dynamic content
- Name layers clearly and consistently

### 2. **Design Tokens**
- Create styles for colors, text, effects
- Use variables for spacing and sizing
- Link components to design tokens
- Document token usage

### 3. **Responsive Design**
- Use constraints for flexible layouts
- Create breakpoint frames
- Test on different screen sizes
- Use auto-layout for responsive behavior

### 4. **Accessibility**
- Ensure color contrast (WCAG AA minimum)
- Use semantic color names
- Include focus states
- Test with screen readers

### 5. **Developer Handoff**
- Name components clearly
- Add descriptions to components
- Use consistent spacing
- Export assets at 2x resolution
- Include interaction specifications

---

## 🚀 Design-to-Code Workflow

### 1. **Figma to Code Tools**
- Figma Dev Mode
- Figma to React plugins
- Design token export
- Component code generation

### 2. **Export Specifications**
- Export design tokens as JSON
- Export icons as SVG
- Export images as optimized assets
- Generate component specs

### 3. **Implementation Checklist**
- ✅ Design tokens implemented
- ✅ Components built from Figma
- ✅ Responsive breakpoints match
- ✅ RTL support verified
- ✅ Accessibility tested
- ✅ Performance optimized

---

## 📚 Additional Resources

### Figma Plugins to Install
1. **Design Tokens** - Export tokens
2. **Figma to React** - Generate code
3. **Contrast Checker** - Accessibility
4. **RTL Layout** - RTL support
5. **Auto Layout** - Responsive design

### Design System Documentation
- Component usage guidelines
- Do's and Don'ts
- Accessibility guidelines
- Brand guidelines
- Animation principles

---

## ✅ Next Steps

1. **Create Figma File** with the structure above
2. **Design Tokens** - Build color, typography, spacing systems
3. **Components** - Create reusable component library
4. **Patterns** - Design common UI patterns
5. **Pages** - Design full page layouts
6. **Export** - Export tokens and assets
7. **Implement** - Build front-end from designs

---

**Status:** 📐 **READY FOR FIGMA DESIGN**

This specification provides everything needed to create a professional, scalable design system in Figma that can be directly implemented in code.
