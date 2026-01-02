-- Multi-Tenant SaaS Platform Database Schema
-- Main platform database (manages all tenants)

-- Tenants table
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    subdomain VARCHAR(100) UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'trial', -- trial, active, suspended, cancelled
    subscription_tier VARCHAR(50) DEFAULT 'starter', -- starter, professional, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trial_end_date TIMESTAMP,
    metadata JSONB,
    INDEX idx_tenant_status (status),
    INDEX idx_tenant_domain (domain),
    INDEX idx_tenant_subdomain (subdomain)
);

-- Tenant databases table
CREATE TABLE IF NOT EXISTS tenant_databases (
    tenant_id VARCHAR(50) PRIMARY KEY,
    database_name VARCHAR(255) NOT NULL UNIQUE,
    database_type VARCHAR(20) DEFAULT 'sqlite', -- sqlite, postgresql
    connection_string TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

-- Subscription plans table
CREATE TABLE IF NOT EXISTS subscription_plans (
    plan_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    tier VARCHAR(50) NOT NULL, -- starter, professional, enterprise
    price_monthly DECIMAL(10, 2) NOT NULL,
    price_yearly DECIMAL(10, 2),
    max_agents INTEGER,
    max_workflows INTEGER,
    max_api_calls INTEGER,
    max_storage_gb INTEGER,
    included_modules TEXT[], -- Array of module names
    features JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tenant subscriptions table
CREATE TABLE IF NOT EXISTS tenant_subscriptions (
    subscription_id VARCHAR(50) PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    plan_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, cancelled, expired, trial
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    renewal_date TIMESTAMP,
    billing_cycle VARCHAR(20) DEFAULT 'monthly', -- monthly, yearly
    payment_method_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(plan_id),
    INDEX idx_subscription_tenant (tenant_id),
    INDEX idx_subscription_status (status)
);

-- Tenant modules table
CREATE TABLE IF NOT EXISTS tenant_modules (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    module_name VARCHAR(100) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    purchased_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,
    configuration JSONB,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    UNIQUE(tenant_id, module_name),
    INDEX idx_tenant_modules (tenant_id, enabled)
);

-- Usage records table
CREATE TABLE IF NOT EXISTS usage_records (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    metric_name VARCHAR(100) NOT NULL, -- agents, workflows, api_calls, emails, storage
    usage_count INTEGER NOT NULL DEFAULT 0,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    INDEX idx_usage_tenant_period (tenant_id, period_start, period_end),
    INDEX idx_usage_metric (metric_name, period_start)
);

-- Invoices table
CREATE TABLE IF NOT EXISTS invoices (
    invoice_id VARCHAR(50) PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    subscription_id VARCHAR(50),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'SAR',
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, failed, refunded
    due_date TIMESTAMP,
    paid_date TIMESTAMP,
    invoice_number VARCHAR(100) UNIQUE,
    items JSONB, -- Array of invoice items
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    FOREIGN KEY (subscription_id) REFERENCES tenant_subscriptions(subscription_id),
    INDEX idx_invoice_tenant (tenant_id),
    INDEX idx_invoice_status (status)
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id VARCHAR(50) PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    invoice_id VARCHAR(50),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'SAR',
    payment_method VARCHAR(50), -- stripe, paypal, mada, bank_transfer
    payment_provider_id VARCHAR(100), -- External payment ID
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed, refunded
    transaction_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
    INDEX idx_payment_tenant (tenant_id),
    INDEX idx_payment_status (status)
);

-- Tenant API keys table
CREATE TABLE IF NOT EXISTS tenant_api_keys (
    key_id VARCHAR(50) PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    api_key VARCHAR(255) NOT NULL UNIQUE,
    api_secret VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    permissions JSONB, -- Array of permissions
    last_used TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    INDEX idx_api_key_tenant (tenant_id),
    INDEX idx_api_key_value (api_key)
);

-- Insert default subscription plans
INSERT INTO subscription_plans (plan_id, name, tier, price_monthly, price_yearly, max_agents, max_workflows, max_api_calls, max_storage_gb, included_modules, features) VALUES
('starter', 'Starter Plan', 'starter', 99.00, 990.00, 5, 10, 10000, 10, ARRAY['email_automation'], '{"support": "email", "custom_workflows": false}'),
('professional', 'Professional Plan', 'professional', 299.00, 2990.00, 20, 50, 100000, 50, ARRAY['email_automation', 'sales_agent', 'support_agent'], '{"support": "priority", "custom_workflows": true}'),
('enterprise', 'Enterprise Plan', 'enterprise', 999.00, 9990.00, NULL, NULL, NULL, 500, ARRAY['all'], '{"support": "dedicated", "custom_workflows": true, "sla": true, "custom_integrations": true}')
ON CONFLICT (plan_id) DO NOTHING;
