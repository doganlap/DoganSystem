import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Header from '../Header';
import '../../../i18n';

// Create a test QueryClient
const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

const renderWithProviders = (component) => {
  const queryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>{component}</QueryClientProvider>
  );
};

describe('Header Component', () => {
  it('renders header with tenant selector', () => {
    const mockSetTenant = vi.fn();

    renderWithProviders(
      <Header
        currentTenantId="default"
        setCurrentTenantId={mockSetTenant}
        onMenuClick={vi.fn()}
        isRTL={false}
      />
    );

    expect(screen.getByText('Current Tenant:')).toBeInTheDocument();
  });

  it('calls onMenuClick when menu button is clicked', () => {
    const mockMenuClick = vi.fn();
    const mockSetTenant = vi.fn();

    renderWithProviders(
      <Header
        currentTenantId="default"
        setCurrentTenantId={mockSetTenant}
        onMenuClick={mockMenuClick}
        isRTL={false}
      />
    );

    const menuButton = screen.getAllByRole('button')[0];
    fireEvent.click(menuButton);

    expect(mockMenuClick).toHaveBeenCalledTimes(1);
  });

  it('changes tenant when selector value changes', () => {
    const mockSetTenant = vi.fn();

    renderWithProviders(
      <Header
        currentTenantId="default"
        setCurrentTenantId={mockSetTenant}
        onMenuClick={vi.fn()}
        isRTL={false}
      />
    );

    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'new-tenant' } });

    expect(mockSetTenant).toHaveBeenCalledWith('new-tenant');
  });
});
