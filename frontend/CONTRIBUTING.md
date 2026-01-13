# Contributing to DoganSystem Frontend

Thank you for your interest in contributing to DoganSystem! This document provides guidelines and standards for contributing to the frontend codebase.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 🤝 Code of Conduct

### Our Standards
- **Be respectful** and inclusive of all contributors
- **Be constructive** in feedback and discussions
- **Focus on the code**, not the person
- **Help others learn** and grow

### Unacceptable Behavior
- Harassment, discrimination, or offensive comments
- Trolling, insulting, or derogatory comments
- Publishing private information without permission

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18.x or 20.x
- npm 9.x or higher
- Git
- Code editor (VS Code recommended)

### Initial Setup

1. **Fork and Clone**
```bash
git clone https://github.com/doganlap/DoganSystem.git
cd DoganSystem/frontend
```

2. **Install Dependencies**
```bash
npm install
```

3. **Setup Environment**
```bash
cp .env.example .env
# Edit .env with your local configuration
```

4. **Start Development Server**
```bash
npm run dev
```

5. **Run Tests**
```bash
npm run test
```

---

## 💻 Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/feature-name` - New features
- `fix/bug-name` - Bug fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation updates

### Creating a New Branch

```bash
# For a new feature
git checkout -b feature/user-authentication

# For a bug fix
git checkout -b fix/sidebar-navigation

# For refactoring
git checkout -b refactor/api-client
```

### Development Process

1. **Create a branch** from `develop`
2. **Make your changes** following coding standards
3. **Write tests** for new functionality
4. **Run quality checks** before committing
5. **Commit your changes** with proper messages
6. **Push to your fork** and create a PR
7. **Address review comments** if any

---

## 📝 Coding Standards

### JavaScript/JSX

#### Component Structure
```jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';

/**
 * Component description
 * @param {Object} props - Component props
 * @param {string} props.title - Title text
 * @param {Function} props.onClick - Click handler
 */
const MyComponent = ({ title, onClick }) => {
  const { t } = useTranslation();

  // Component logic

  return (
    <div>
      <h1>{title}</h1>
      <button onClick={onClick}>{t('submit')}</button>
    </div>
  );
};

MyComponent.propTypes = {
  title: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default MyComponent;
```

#### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile`, `DashboardCard` |
| Functions | camelCase | `fetchData`, `handleClick` |
| Constants | UPPER_SNAKE_CASE | `API_BASE_URL`, `MAX_RETRIES` |
| Files (Components) | PascalCase | `UserProfile.jsx` |
| Files (Utilities) | camelCase | `apiClient.js`, `formatDate.js` |
| CSS Classes | kebab-case | `user-profile`, `dashboard-card` |

#### Best Practices

✅ **DO:**
- Use functional components with hooks
- Keep components small and focused
- Extract reusable logic into custom hooks
- Use PropTypes for type checking
- Write meaningful variable names
- Add JSDoc comments for complex functions
- Handle errors gracefully
- Use early returns to reduce nesting

❌ **DON'T:**
- Use class components (unless necessary)
- Deeply nest components
- Put business logic in components
- Use inline styles (use Tailwind)
- Leave console.log statements
- Ignore ESLint warnings
- Skip error handling

#### Code Examples

**Good:**
```jsx
const UserCard = ({ user }) => {
  if (!user) return null;

  return (
    <div className="p-4 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold">{user.name}</h3>
      <p className="text-gray-600">{user.email}</p>
    </div>
  );
};
```

**Bad:**
```jsx
const UserCard = ({ user }) => {
  return (
    <div style={{ padding: '16px', borderRadius: '8px' }}>
      {user ? (
        <div>
          <h3 style={{ fontSize: '18px', fontWeight: 'bold' }}>{user.name}</h3>
          <p style={{ color: '#666' }}>{user.email}</p>
        </div>
      ) : (
        <div></div>
      )}
    </div>
  );
};
```

### Styling with Tailwind CSS

✅ **DO:**
- Use Tailwind utility classes
- Group related utilities (layout, spacing, colors)
- Extract repeated patterns into components
- Use responsive prefixes (sm:, md:, lg:)
- Use dark mode classes when applicable

```jsx
// Good
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
  <h3 className="text-lg font-semibold text-gray-900">Title</h3>
  <button className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700">
    Action
  </button>
</div>
```

### Custom Hooks

✅ **DO:**
- Prefix with `use`
- Keep them focused and reusable
- Document parameters and return values
- Handle loading and error states

```jsx
/**
 * Custom hook to fetch user data
 * @param {string} userId - User ID to fetch
 * @returns {Object} { data, isLoading, error, refetch }
 */
const useUser = (userId) => {
  return useQuery(['user', userId], () => fetchUser(userId), {
    enabled: !!userId,
  });
};
```

---

## 🧪 Testing Guidelines

### Test Structure

```jsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import MyComponent from '../MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const mockClick = vi.fn();
    render(<MyComponent onClick={mockClick} />);

    fireEvent.click(screen.getByRole('button'));
    expect(mockClick).toHaveBeenCalledTimes(1);
  });
});
```

### Testing Best Practices

✅ **DO:**
- Test user behavior, not implementation
- Use `screen` queries from Testing Library
- Mock external dependencies
- Test error states and edge cases
- Aim for 80%+ code coverage

❌ **DON'T:**
- Test implementation details
- Use `.toMatchSnapshot()` excessively
- Skip error scenarios
- Write tests that depend on each other

### Coverage Requirements

| Category | Minimum Coverage |
|----------|------------------|
| Components | 80% |
| Hooks | 90% |
| Utils | 95% |
| Overall | 80% |

---

## 📝 Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

**Good:**
```
feat(auth): add user login functionality

- Implement login form with validation
- Add JWT token storage
- Integrate with authentication API

Closes #123
```

**Good:**
```
fix(dashboard): resolve chart rendering issue

Fix chart not displaying when data is empty
by adding proper null checks.

Fixes #456
```

**Bad:**
```
updated stuff
```

**Bad:**
```
fix bug
```

---

## 🔄 Pull Request Process

### Before Creating a PR

1. ✅ Code follows style guidelines
2. ✅ Tests pass locally (`npm run test`)
3. ✅ Linting passes (`npm run lint`)
4. ✅ No console errors or warnings
5. ✅ Code is properly formatted (`npm run format`)
6. ✅ Commits follow commit message guidelines

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing

## Screenshots (if applicable)
Add screenshots or GIFs

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Address feedback** and update PR
4. **Approval** required before merging
5. **Merge** using squash and merge

---

## 🛠️ Development Tools

### Recommended VS Code Extensions

- ESLint
- Prettier
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets
- Auto Rename Tag
- Path Intellisense
- GitLens

### Useful Commands

```bash
# Development
npm run dev              # Start dev server
npm run build            # Build for production
npm run preview          # Preview production build

# Code Quality
npm run lint             # Run ESLint
npm run lint:fix         # Fix ESLint issues
npm run format           # Format code with Prettier
npm run format:check     # Check formatting

# Testing
npm run test             # Run tests
npm run test:ui          # Run tests with UI
npm run test:watch       # Run tests in watch mode
npm run coverage         # Generate coverage report
```

---

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, browser, Node version
6. **Screenshots**: If applicable
7. **Additional Context**: Any other relevant info

---

## 💡 Suggesting Features

When suggesting features:

1. **Use Case**: Explain the problem it solves
2. **Proposed Solution**: Your suggested approach
3. **Alternatives**: Other solutions considered
4. **Additional Context**: Any other relevant info

---

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Testing Library Documentation](https://testing-library.com/)
- [React Query Documentation](https://tanstack.com/query/latest)

---

## 🙏 Questions?

If you have questions:
- Create a GitHub Discussion
- Reach out to maintainers
- Check existing documentation

---

Thank you for contributing to DoganSystem! 🎉
