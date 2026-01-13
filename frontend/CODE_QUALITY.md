# Code Quality Setup

Complete guide to the code quality tools and practices in DoganSystem Frontend.

## 📋 Table of Contents
- [Overview](#overview)
- [Tools](#tools)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Configuration Files](#configuration-files)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project uses a comprehensive code quality stack to ensure:
- **Consistent code style** across the codebase
- **High code quality** through linting and testing
- **Automated checks** via pre-commit hooks and CI/CD
- **Best practices** enforcement

### Quality Gates

Every code change must pass:
1. ✅ **ESLint** - Code quality and best practices
2. ✅ **Prettier** - Code formatting
3. ✅ **Vitest** - Unit and integration tests
4. ✅ **Type checking** - TypeScript validation (if enabled)

---

## 🛠️ Tools

### 1. ESLint
**Purpose**: Identify and fix code quality issues

**Configuration**: `.eslintrc.cjs`

**Features**:
- React best practices
- React Hooks rules
- JSX accessibility (a11y)
- Custom rules for project

**Rules**:
```javascript
{
  "react/react-in-jsx-scope": "off",      // Not needed in React 18
  "react-hooks/rules-of-hooks": "error",  // Enforce hooks rules
  "no-console": ["warn", { allow: ["warn", "error"] }],
  "jsx-a11y/anchor-is-valid": "warn"      // Accessibility
}
```

### 2. Prettier
**Purpose**: Automatic code formatting

**Configuration**: `.prettierrc.json`

**Settings**:
```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

**Why Prettier?**
- Saves time on code reviews
- Consistent formatting across team
- Integrates with editors
- Works with ESLint

### 3. Vitest
**Purpose**: Fast unit testing framework

**Configuration**: `vitest.config.js`

**Features**:
- Fast execution with Vite
- Compatible with Jest API
- Built-in code coverage
- Watch mode for development

**Coverage Goals**:
- Components: 80%+
- Hooks: 90%+
- Utils: 95%+
- Overall: 80%+

### 4. React Testing Library
**Purpose**: User-centric component testing

**Setup**: `src/test/setup.js`

**Philosophy**:
- Test behavior, not implementation
- Query by accessibility attributes
- User-focused assertions

**Example**:
```jsx
import { render, screen, fireEvent } from '@testing-library/react';

it('handles user clicks', () => {
  render(<Button onClick={mockFn}>Click me</Button>);
  fireEvent.click(screen.getByText('Click me'));
  expect(mockFn).toHaveBeenCalled();
});
```

### 5. Husky
**Purpose**: Git hooks automation

**Setup**: `.husky/` directory

**Hooks**:
- `pre-commit`: Run linters and formatters
- `pre-push`: Run tests (optional)

### 6. lint-staged
**Purpose**: Run linters on staged files only

**Configuration**: `.lintstagedrc.json`

**Process**:
```
git add file.js → pre-commit hook → lint-staged
                                   ↓
                          ESLint → Prettier → git commit
```

---

## 🚀 Setup Instructions

### Initial Setup

```bash
# Install dependencies
npm install

# Setup Husky (Git hooks)
npm run prepare

# Verify setup
npm run quality
```

### IDE Setup

#### VS Code

1. **Install Extensions**:
   - ESLint
   - Prettier - Code formatter
   - Tailwind CSS IntelliSense

2. **Settings** (`.vscode/settings.json`):
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact"
  ]
}
```

#### WebStorm/IntelliJ

1. Go to **Settings** → **Languages & Frameworks**
2. Enable **ESLint** and **Prettier**
3. Enable **Format on Save**

---

## 💻 Usage

### Commands

#### Linting
```bash
# Run ESLint
npm run lint

# Fix ESLint issues automatically
npm run lint:fix

# Lint specific file
npx eslint src/components/MyComponent.jsx

# Lint and fix specific file
npx eslint src/components/MyComponent.jsx --fix
```

#### Formatting
```bash
# Format all files
npm run format

# Check formatting without modifying
npm run format:check

# Format specific file
npx prettier --write src/components/MyComponent.jsx
```

#### Testing
```bash
# Run tests once
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with UI
npm run test:ui

# Run tests for CI (no watch)
npm run test:ci

# Generate coverage report
npm run coverage
```

#### All Quality Checks
```bash
# Run all quality checks
npm run quality

# This runs:
# 1. ESLint
# 2. Prettier check
# 3. All tests
```

### Pre-commit Process

When you commit code:

1. **Husky** triggers pre-commit hook
2. **lint-staged** runs on staged files:
   - ESLint fixes issues
   - Prettier formats code
3. If successful → commit proceeds
4. If failed → commit blocked, fix issues

```bash
# Example workflow
git add src/components/MyComponent.jsx
git commit -m "feat: add new component"

# Output:
# ✔ Preparing lint-staged...
# ✔ Running tasks for staged files...
# ✔ Applying modifications from tasks...
# ✔ Cleaning up temporary files...
# [main abc1234] feat: add new component
```

### Bypass Hooks (Use Sparingly!)

```bash
# Skip pre-commit hooks (NOT RECOMMENDED)
git commit --no-verify -m "message"
```

⚠️ **Warning**: Only use `--no-verify` in emergencies. CI will still catch issues.

---

## 📄 Configuration Files

### Project Structure
```
frontend/
├── .eslintrc.cjs              # ESLint configuration
├── .prettierrc.json           # Prettier configuration
├── .prettierignore            # Prettier ignore patterns
├── .lintstagedrc.json         # lint-staged configuration
├── vitest.config.js           # Vitest configuration
├── .husky/                    # Git hooks
│   ├── pre-commit            # Pre-commit hook
│   └── pre-push              # Pre-push hook (optional)
└── src/
    └── test/
        └── setup.js          # Test environment setup
```

### ESLint Configuration (`.eslintrc.cjs`)

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2021: true },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/recommended',
    'prettier', // Must be last
  ],
  rules: {
    // Custom rules
  },
};
```

### Prettier Configuration (`.prettierrc.json`)

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### lint-staged Configuration (`.lintstagedrc.json`)

```json
{
  "*.{js,jsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md,yml,yaml}": ["prettier --write"]
}
```

### Vitest Configuration (`vitest.config.js`)

```javascript
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

---

## 🔄 CI/CD Integration

### GitHub Actions

Configuration: `.github/workflows/frontend-ci.yml`

**Pipeline Steps**:

1. **Lint & Test Job**
   - Checkout code
   - Setup Node.js
   - Install dependencies
   - Run ESLint
   - Check Prettier formatting
   - Run tests
   - Generate coverage

2. **Build Job**
   - Build production bundle
   - Upload artifacts

3. **Deploy Jobs** (optional)
   - Deploy to staging (develop branch)
   - Deploy to production (main branch)

**Branch Protection**:
- Require CI checks to pass
- Require code review approval
- Prevent force pushes

### Running Locally (CI Simulation)

```bash
# Run the same checks as CI
npm run quality

# This is equivalent to:
npm run lint && \
npm run format:check && \
npm run test:ci
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. ESLint Errors Not Auto-Fixing

**Problem**: ESLint shows errors but doesn't fix them

**Solution**:
```bash
# Try manual fix
npm run lint:fix

# If persists, fix manually based on errors
npm run lint
```

#### 2. Prettier Conflicts with ESLint

**Problem**: Prettier and ESLint give conflicting rules

**Solution**: Already configured with `eslint-config-prettier` to disable conflicting ESLint rules

```bash
# Verify no conflicts
npm run lint
npm run format:check
```

#### 3. Tests Failing in CI but Pass Locally

**Problem**: Tests pass locally but fail in CI

**Possible Causes**:
- Environment differences
- Timing issues
- Missing dependencies

**Solution**:
```bash
# Run tests in CI mode locally
npm run test:ci

# Check for console warnings
npm run test -- --reporter=verbose
```

#### 4. Husky Hooks Not Running

**Problem**: Pre-commit hooks don't trigger

**Solution**:
```bash
# Reinstall Husky
rm -rf .husky
npm run prepare

# Verify hook exists
cat .husky/pre-commit

# Check Git hooks are enabled
git config core.hooksPath
```

#### 5. Slow Pre-commit Hooks

**Problem**: Commits take too long

**Solution**: lint-staged only runs on changed files. If still slow:

```bash
# Check what's running
cat .lintstagedrc.json

# Temporarily disable (not recommended)
git commit --no-verify
```

#### 6. Coverage Below Threshold

**Problem**: Coverage doesn't meet minimum

**Solution**:
```bash
# Generate detailed coverage report
npm run coverage

# Open HTML report
open coverage/index.html

# Add tests for uncovered lines
```

---

## 📊 Quality Metrics

### Code Quality Badges

Add to README:

```markdown
![ESLint](https://img.shields.io/badge/eslint-passing-brightgreen)
![Prettier](https://img.shields.io/badge/prettier-formatted-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)
```

### Tracking Quality

```bash
# Check linting issues
npm run lint -- --format=json > lint-report.json

# Check test coverage
npm run coverage

# Check bundle size
npm run build
du -sh dist/
```

---

## 🎯 Best Practices

### 1. Write Tests First (TDD)
```bash
# Create test file first
touch src/components/__tests__/MyComponent.test.jsx

# Write failing test
npm run test:watch

# Implement component
# Test passes ✅
```

### 2. Fix Linting Issues Immediately
- Don't accumulate ESLint warnings
- Fix during development, not before commit
- Use `// eslint-disable-next-line` sparingly

### 3. Keep Coverage High
- Add tests for new features
- Don't decrease overall coverage
- Aim for 100% on utility functions

### 4. Format Consistently
- Let Prettier handle formatting
- Don't waste time on style debates
- Focus on logic, not formatting

---

## 📚 Additional Resources

- [ESLint Documentation](https://eslint.org/)
- [Prettier Documentation](https://prettier.io/)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library Documentation](https://testing-library.com/)
- [Husky Documentation](https://typicode.github.io/husky/)

---

## 🚀 Quick Start Checklist

Before submitting code:

- [ ] `npm run lint` passes
- [ ] `npm run format:check` passes
- [ ] `npm run test` passes
- [ ] Coverage meets minimum (80%)
- [ ] No `console.log` statements
- [ ] Tests added for new features
- [ ] Documentation updated

---

**Questions?** Check [CONTRIBUTING.md](./CONTRIBUTING.md) or create an issue.
