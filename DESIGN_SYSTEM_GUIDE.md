# Unified Enterprise Design System

A Modern, Responsive Design System for Web & Mobile Apps

## Overview

This design system provides a comprehensive set of design tokens, components, and utilities for building consistent, accessible, and responsive user interfaces. It follows industry best practices from IBM Carbon, Google Material Design, and Microsoft Fluent Design System.

## Key Features

- ✅ **Three-Tier Token Hierarchy** (Global → Alias → Component)
- ✅ **WCAG AA Accessibility Compliance**
- ✅ **Full RTL (Right-to-Left) Support** for Arabic
- ✅ **Mobile-First Responsive Design**
- ✅ **Comprehensive Component Library**
- ✅ **Semantic Color System**
- ✅ **Consistent Spacing & Typography**

## File Structure

```
wwwroot/css/
├── design-system.css      # Main entry point (imports all)
├── design-tokens.css      # Design tokens (CSS variables)
└── components.css         # Core component styles
```

## Quick Start

### 1. Include in Your Layout

Add to `_Layout.cshtml` or `_PublicLayout.cshtml`:

```html
<link rel="stylesheet" href="~/css/design-system.css" />
```

**Note:** The design system works alongside Bootstrap 5. Include Bootstrap first, then the design system:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
<link rel="stylesheet" href="~/css/design-system.css" />
```

### 2. Use Design Tokens

All tokens are available as CSS variables:

```css
.my-custom-button {
  background-color: var(--color-primary);
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-border-radius);
  color: var(--color-text-inverse);
}
```

### 3. Use Components

Components follow standard HTML patterns:

```html
<!-- Button -->
<button class="btn btn-primary">Primary Action</button>
<button class="btn btn-secondary">Secondary Action</button>
<button class="btn btn-danger">Delete</button>

<!-- Form -->
<div class="form-group">
  <label class="form-label">Email Address</label>
  <input type="email" class="form-control" placeholder="user@example.com" />
  <div class="invalid-feedback">Please provide a valid email.</div>
</div>

<!-- Alert -->
<div class="alert alert-success" role="alert">
  <span class="alert-icon">✓</span>
  <div class="alert-content">
    <strong>Success!</strong> Your changes have been saved.
  </div>
</div>

<!-- Card -->
<div class="card">
  <div class="card-header">Card Title</div>
  <div class="card-body">
    <h5 class="card-title">Card Heading</h5>
    <p class="card-text">Card content goes here.</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Action</button>
  </div>
</div>
```

## Design Tokens

### Color Palette

#### Primary Colors
- `--color-primary`: `#0d6efd` (Primary Blue)
- `--color-primary-hover`: `#0056b3`
- `--color-primary-active`: `#004080`

#### Status Colors
- `--color-success`: `#4caf50` (Green)
- `--color-warning`: `#f5c247` (Amber)
- `--color-error`: `#f44336` (Red)
- `--color-info`: `#008080` (Teal)

#### Neutral Colors
- `--color-gray-50` to `--color-gray-900`
- `--color-text-primary`: `#333333`
- `--color-text-secondary`: `#616161`
- `--color-bg-primary`: `#ffffff`
- `--color-bg-secondary`: `#fafafa`

### Typography

#### Font Sizes
- `--font-size-xs`: `0.75rem` (12px)
- `--font-size-sm`: `0.875rem` (14px)
- `--font-size-base`: `1rem` (16px)
- `--font-size-lg`: `1.125rem` (18px)
- `--font-size-xl`: `1.25rem` (20px)
- `--font-size-2xl`: `1.5rem` (24px)
- `--font-size-3xl`: `1.875rem` (30px)
- `--font-size-4xl`: `2rem` (32px)
- `--font-size-5xl`: `2.5rem` (40px)

#### Headings
- `--font-size-heading-xs`: `1.125rem`
- `--font-size-heading-sm`: `1.25rem`
- `--font-size-heading-base`: `1.5rem`
- `--font-size-heading-lg`: `1.875rem`
- `--font-size-heading-xl`: `2rem`
- `--font-size-heading-2xl`: `2.5rem`

### Spacing

Base unit: **8px**

- `--space-1`: `0.25rem` (4px)
- `--space-2`: `0.5rem` (8px)
- `--space-3`: `0.75rem` (12px)
- `--space-4`: `1rem` (16px)
- `--space-6`: `1.5rem` (24px)
- `--space-8`: `2rem` (32px)
- `--space-12`: `3rem` (48px)
- `--space-16`: `4rem` (64px)

### Border Radius

- `--radius-sm`: `0.25rem` (4px)
- `--radius-base`: `0.375rem` (6px)
- `--radius-md`: `0.5rem` (8px)
- `--radius-lg`: `0.75rem` (12px)
- `--radius-xl`: `1rem` (16px)
- `--radius-full`: `9999px`

### Shadows

- `--shadow-sm`: Subtle shadow
- `--shadow-base`: Default shadow
- `--shadow-md`: Medium shadow
- `--shadow-lg`: Large shadow
- `--shadow-xl`: Extra large shadow

## Components

### Buttons

```html
<!-- Primary (One per view) -->
<button class="btn btn-primary">Primary Action</button>

<!-- Secondary (Outline) -->
<button class="btn btn-secondary">Secondary</button>

<!-- Danger -->
<button class="btn btn-danger">Delete</button>

<!-- Success -->
<button class="btn btn-success">Save</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-lg">Large</button>
```

### Forms

```html
<div class="form-group">
  <label for="email" class="form-label">Email Address</label>
  <input type="email" class="form-control" id="email" placeholder="user@example.com" />
  <div class="form-text">We'll never share your email.</div>
</div>

<!-- Validation States -->
<input type="email" class="form-control is-invalid" />
<div class="invalid-feedback">Please provide a valid email.</div>

<input type="email" class="form-control is-valid" />
<div class="valid-feedback">Looks good!</div>

<!-- Sizes -->
<input class="form-control form-control-sm" placeholder="Small" />
<input class="form-control" placeholder="Default" />
<input class="form-control form-control-lg" placeholder="Large" />
```

### Alerts

```html
<div class="alert alert-success" role="alert">
  <span class="alert-icon">✓</span>
  <div class="alert-content">
    <strong>Success!</strong> Your changes have been saved.
  </div>
</div>

<div class="alert alert-danger alert-dismissible" role="alert">
  <span class="alert-icon">⚠</span>
  <div class="alert-content">
    <strong>Error!</strong> Something went wrong.
  </div>
  <button type="button" class="btn-close" aria-label="Close"></button>
</div>

<!-- Variants: alert-primary, alert-success, alert-warning, alert-danger, alert-info -->
```

### Cards

```html
<div class="card">
  <div class="card-header">Header</div>
  <div class="card-body">
    <h5 class="card-title">Card Title</h5>
    <p class="card-text">Card content.</p>
    <button class="btn btn-primary">Action</button>
  </div>
  <div class="card-footer">Footer</div>
</div>
```

### Modals

```html
<!-- Modal Structure -->
<div class="modal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal Title</h5>
        <button type="button" class="btn-close" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>Modal body text goes here.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary">Cancel</button>
        <button type="button" class="btn btn-primary">Save</button>
      </div>
    </div>
  </div>
</div>

<!-- Sizes: modal-sm, modal-lg, modal-xl -->
```

## Responsive Design

The design system uses a mobile-first approach with standard breakpoints:

- **xs**: `< 576px` (Mobile)
- **sm**: `≥ 576px` (Large Mobile)
- **md**: `≥ 768px` (Tablet)
- **lg**: `≥ 992px` (Desktop)
- **xl**: `≥ 1200px` (Large Desktop)
- **xxl**: `≥ 1400px` (Extra Large Desktop)

### Grid System

```html
<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4">
      <!-- Content -->
    </div>
    <div class="col-12 col-md-6 col-lg-4">
      <!-- Content -->
    </div>
    <div class="col-12 col-md-12 col-lg-4">
      <!-- Content -->
    </div>
  </div>
</div>
```

## RTL (Right-to-Left) Support

The design system fully supports Arabic and RTL layouts. Simply add `dir="rtl"` to your HTML element:

```html
<html lang="ar" dir="rtl">
```

All components, spacing, and navigation automatically adjust for RTL.

## Accessibility (WCAG AA)

- ✅ **Color Contrast**: All text meets WCAG AA standards (4.5:1 ratio)
- ✅ **Focus Indicators**: Clear focus outlines for keyboard navigation
- ✅ **Touch Targets**: Minimum 44px height for interactive elements
- ✅ **Screen Reader Support**: Proper ARIA labels and semantic HTML
- ✅ **Reduced Motion**: Respects `prefers-reduced-motion` media query
- ✅ **High Contrast**: Supports high contrast mode

### Accessibility Best Practices

1. **Use Semantic HTML**: `<button>`, `<nav>`, `<main>`, etc.
2. **Add ARIA Labels**: For icon-only buttons and custom components
3. **Provide Alt Text**: For images and icons
4. **Keyboard Navigation**: Ensure all interactive elements are keyboard accessible
5. **Focus Management**: Don't remove focus indicators

```html
<!-- Good: Semantic button -->
<button class="btn btn-primary" aria-label="Save changes">
  <i class="fas fa-save"></i>
</button>

<!-- Good: Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Good: Screen reader text -->
<span class="sr-only">Loading, please wait</span>
```

## Integration with Bootstrap 5

The design system is designed to work alongside Bootstrap 5:

1. **Include Bootstrap First**: The design system enhances Bootstrap components
2. **Override Variables**: Design tokens can override Bootstrap's default variables
3. **Custom Components**: Use design system components for consistency
4. **Utility Classes**: Both systems' utility classes work together

### Bootstrap Variable Overrides (Optional)

Create a custom Bootstrap theme file:

```scss
// bootstrap-custom.scss
@import "bootstrap/functions";
@import "bootstrap/variables";

// Override with design tokens
$primary: var(--color-primary);
$success: var(--color-success);
$danger: var(--color-error);
$warning: var(--color-warning);
$info: var(--color-info);

@import "bootstrap/bootstrap";
```

## Utility Classes

### Text Utilities

```html
<p class="text-primary">Primary text</p>
<p class="text-secondary">Secondary text</p>
<p class="text-success">Success text</p>
<p class="text-danger">Danger text</p>
<p class="text-muted">Muted text</p>

<p class="text-center">Centered</p>
<p class="text-start">Left aligned</p>
<p class="text-end">Right aligned</p>
```

### Background Utilities

```html
<div class="bg-primary">Primary background</div>
<div class="bg-secondary">Secondary background</div>
<div class="bg-success">Success background</div>
```

### Spacing Utilities

```html
<div class="m-4">Margin 4</div>
<div class="mt-2">Margin top 2</div>
<div class="p-4">Padding 4</div>
<div class="px-3">Padding horizontal 3</div>
```

### Display Utilities

```html
<div class="d-none d-md-block">Hidden on mobile, visible on desktop</div>
<div class="d-flex">Flex container</div>
```

## Customization

### Overriding Tokens

Override design tokens in your custom CSS:

```css
:root {
  --color-primary: #your-brand-color;
  --font-size-base: 18px;
  --space-unit: 10px;
}
```

### Creating Custom Components

Use design tokens when creating custom components:

```css
.my-custom-component {
  background-color: var(--color-bg-primary);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  color: var(--color-text-primary);
}

.my-custom-component:hover {
  box-shadow: var(--shadow-lg);
}
```

## Best Practices

1. **Use Design Tokens**: Always use CSS variables instead of hardcoded values
2. **Follow Component Patterns**: Use existing components before creating custom ones
3. **Mobile-First**: Design for mobile, then enhance for larger screens
4. **Accessibility First**: Ensure components are accessible from the start
5. **Consistent Spacing**: Use the spacing scale (multiples of 8px)
6. **Semantic Colors**: Use semantic color tokens (--color-success, not --color-green-500)
7. **One Primary Action**: Only one primary button per view/section

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [IBM Carbon Design System](https://www.carbondesignsystem.com/)
- [Google Material Design](https://material.io/design)
- [Microsoft Fluent Design](https://www.microsoft.com/design/fluent/)

## Support

For questions or issues with the design system, please contact the design system team.
