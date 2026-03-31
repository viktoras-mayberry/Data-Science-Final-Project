-- ============================================================
-- Telco Customer Churn Database Schema
-- Run this SQL in pgAdmin Query Tool after creating the
-- 'telco_churn' database.
-- ============================================================

-- Drop tables if they already exist (for re-runs)
DROP TABLE IF EXISTS billing CASCADE;
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ============================================================
-- Table 1: customers
-- Stores demographic information about each customer
-- ============================================================
CREATE TABLE customers (
    customer_id     VARCHAR(20) PRIMARY KEY,
    gender          VARCHAR(10) NOT NULL,
    senior_citizen  INTEGER NOT NULL DEFAULT 0,
    partner         VARCHAR(5) NOT NULL,
    dependents      VARCHAR(5) NOT NULL,
    tenure          INTEGER NOT NULL
);

-- ============================================================
-- Table 2: services
-- Stores the services each customer has subscribed to
-- ============================================================
CREATE TABLE services (
    service_id          SERIAL PRIMARY KEY,
    customer_id         VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    phone_service       VARCHAR(5) NOT NULL,
    multiple_lines      VARCHAR(25) NOT NULL,
    internet_service    VARCHAR(20) NOT NULL,
    online_security     VARCHAR(25) NOT NULL,
    online_backup       VARCHAR(25) NOT NULL,
    device_protection   VARCHAR(25) NOT NULL,
    tech_support        VARCHAR(25) NOT NULL,
    streaming_tv        VARCHAR(25) NOT NULL,
    streaming_movies    VARCHAR(25) NOT NULL
);

-- ============================================================
-- Table 3: billing
-- Stores contract, billing, and churn information
-- ============================================================
CREATE TABLE billing (
    billing_id          SERIAL PRIMARY KEY,
    customer_id         VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    contract            VARCHAR(20) NOT NULL,
    paperless_billing   VARCHAR(5) NOT NULL,
    payment_method      VARCHAR(30) NOT NULL,
    monthly_charges     DECIMAL(10, 2) NOT NULL,
    total_charges       DECIMAL(10, 2),
    churn               VARCHAR(5) NOT NULL
);

-- ============================================================
-- Indexes for faster queries
-- ============================================================
CREATE INDEX idx_services_customer ON services(customer_id);
CREATE INDEX idx_billing_customer ON billing(customer_id);
CREATE INDEX idx_billing_churn ON billing(churn);
CREATE INDEX idx_customers_tenure ON customers(tenure);
