-- FlowbitAI Database Schema and Sample Data
-- PostgreSQL Seed Script

-- Create database if not exists
-- Note: This script assumes the database 'flowbit_ai' is already created

-- Drop existing tables if they exist
DROP TABLE IF EXISTS invoices CASCADE;
DROP TABLE IF EXISTS vendors CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- Create Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Vendors table
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Invoices table
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    "invoiceId" VARCHAR(100) NOT NULL,
    "vendorId" INTEGER REFERENCES vendors(id),
    "categoryId" INTEGER REFERENCES categories(id),
    "totalAmount" DECIMAL(10, 2) NOT NULL,
    "issueDate" DATE NOT NULL,
    "dueDate" DATE,
    "paymentDate" DATE,
    status VARCHAR(50) DEFAULT 'pending',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Categories
INSERT INTO categories (name, description) VALUES
('General', 'General business expenses and services'),
('Document', 'Document processing and management related expenses'),
('Office Supplies', 'Office supplies and equipment'),
('Software', 'Software licenses and subscriptions'),
('Marketing', 'Marketing and advertising expenses'),
('Travel', 'Travel and accommodation expenses');

-- Insert Vendors
INSERT INTO vendors (name, email, phone, address) VALUES
('TechCorp Solutions', 'billing@techcorp.com', '+49 30 12345678', 'Friedrichstraße 123, 10117 Berlin, Germany'),
('Global Services GmbH', 'invoices@globalservices.de', '+49 89 87654321', 'Maximilianstraße 45, 80539 München, Germany'),
('Digital Innovations AG', 'accounts@digitalinno.com', '+49 40 11223344', 'Hafencity 22, 20457 Hamburg, Germany'),
('Business Solutions Ltd', 'finance@businesssol.eu', '+49 221 55667788', 'Domstraße 67, 50668 Köln, Germany'),
('Enterprise Systems', 'billing@enterprisesys.de', '+49 711 99887766', 'Königstraße 89, 70173 Stuttgart, Germany'),
('CloudTech Partners', 'invoicing@cloudtech.com', '+49 351 44332211', 'Prager Straße 12, 01069 Dresden, Germany'),
('Innovation Hub GmbH', 'accounts@innovhub.de', '+49 511 77665544', 'Georgstraße 34, 30159 Hannover, Germany'),
('Smart Solutions AG', 'billing@smartsol.com', '+49 621 33445566', 'Planken 56, 68161 Mannheim, Germany'),
('Future Technologies', 'finance@futuretech.eu', '+49 201 88776655', 'Kettwiger Straße 78, 45127 Essen, Germany'),
('Advanced Systems Ltd', 'invoices@advsystems.de', '+49 561 22334455', 'Königsplatz 90, 34117 Kassel, Germany');

-- Insert Sample Invoices with realistic data
INSERT INTO invoices ("invoiceId", "vendorId", "categoryId", "totalAmount", "issueDate", "dueDate", "paymentDate", status, description) VALUES
-- January 2024
('INV-2024-001', 1, 1, 1250.00, '2024-01-15', '2024-02-14', '2024-02-10', 'paid', 'Software development services'),
('INV-2024-002', 2, 2, 850.00, '2024-01-20', '2024-02-19', '2024-02-15', 'paid', 'Document processing system'),
('INV-2024-003', 3, 1, 2300.00, '2024-01-25', '2024-02-24', '2024-02-20', 'paid', 'Digital transformation consulting'),

-- February 2024
('INV-2024-004', 4, 3, 450.00, '2024-02-05', '2024-03-06', '2024-03-01', 'paid', 'Office equipment purchase'),
('INV-2024-005', 5, 4, 1800.00, '2024-02-12', '2024-03-13', '2024-03-08', 'paid', 'Annual software license'),
('INV-2024-006', 6, 1, 3200.00, '2024-02-18', '2024-03-19', '2024-03-14', 'paid', 'Cloud infrastructure setup'),

-- March 2024
('INV-2024-007', 7, 5, 1150.00, '2024-03-08', '2024-04-07', '2024-04-02', 'paid', 'Marketing campaign development'),
('INV-2024-008', 8, 1, 2750.00, '2024-03-15', '2024-04-14', '2024-04-09', 'paid', 'Smart automation solution'),
('INV-2024-009', 9, 6, 950.00, '2024-03-22', '2024-04-21', '2024-04-16', 'paid', 'Business travel expenses'),

-- April 2024
('INV-2024-010', 10, 2, 1650.00, '2024-04-10', '2024-05-10', '2024-05-05', 'paid', 'Advanced document management'),
('INV-2024-011', 1, 4, 750.00, '2024-04-18', '2024-05-18', '2024-05-13', 'paid', 'Software maintenance'),
('INV-2024-012', 2, 1, 4200.00, '2024-04-25', '2024-05-25', '2024-05-20', 'paid', 'Enterprise integration project'),

-- May 2024
('INV-2024-013', 3, 3, 320.00, '2024-05-07', '2024-06-06', '2024-06-01', 'paid', 'Office supplies restocking'),
('INV-2024-014', 4, 5, 2150.00, '2024-05-14', '2024-06-13', '2024-06-08', 'paid', 'Digital marketing services'),
('INV-2024-015', 5, 1, 1890.00, '2024-05-21', '2024-06-20', '2024-06-15', 'paid', 'System optimization'),

-- June 2024
('INV-2024-016', 6, 2, 1200.00, '2024-06-05', '2024-07-05', '2024-06-30', 'paid', 'Document workflow automation'),
('INV-2024-017', 7, 6, 1750.00, '2024-06-12', '2024-07-12', '2024-07-07', 'paid', 'Conference and training'),
('INV-2024-018', 8, 1, 3450.00, '2024-06-19', '2024-07-19', '2024-07-14', 'paid', 'Smart analytics platform'),

-- July 2024
('INV-2024-019', 9, 4, 850.00, '2024-07-08', '2024-08-07', '2024-08-02', 'paid', 'Software subscription renewal'),
('INV-2024-020', 10, 1, 2950.00, '2024-07-15', '2024-08-14', '2024-08-09', 'paid', 'Advanced system implementation'),
('INV-2024-021', 1, 3, 580.00, '2024-07-22', '2024-08-21', '2024-08-16', 'paid', 'Equipment maintenance'),

-- August 2024
('INV-2024-022', 2, 5, 1450.00, '2024-08-06', '2024-09-05', '2024-08-31', 'paid', 'Brand development project'),
('INV-2024-023', 3, 1, 3850.00, '2024-08-13', '2024-09-12', '2024-09-07', 'paid', 'Digital transformation phase 2'),
('INV-2024-024', 4, 2, 750.00, '2024-08-20', '2024-09-19', '2024-09-14', 'paid', 'Document digitization'),

-- September 2024
('INV-2024-025', 5, 6, 1250.00, '2024-09-04', '2024-10-04', '2024-09-29', 'paid', 'Team training workshop'),
('INV-2024-026', 6, 1, 2200.00, '2024-09-11', '2024-10-11', '2024-10-06', 'paid', 'Cloud migration services'),
('INV-2024-027', 7, 4, 950.00, '2024-09-18', '2024-10-18', '2024-10-13', 'paid', 'Software licensing'),

-- October 2024
('INV-2024-028', 8, 1, 4150.00, '2024-10-02', '2024-11-01', '2024-10-27', 'paid', 'Smart solution deployment'),
('INV-2024-029', 9, 3, 425.00, '2024-10-09', '2024-11-08', '2024-11-03', 'paid', 'Office equipment upgrade'),
('INV-2024-030', 10, 2, 1680.00, '2024-10-16', '2024-11-15', '2024-11-10', 'paid', 'Advanced document processing'),

-- November 2024 (Recent invoices - some pending)
('INV-2024-031', 1, 1, 2850.00, '2024-11-05', '2024-12-05', NULL, 'pending', 'Q4 development milestone'),
('INV-2024-032', 2, 5, 1200.00, '2024-11-08', '2024-12-08', NULL, 'pending', 'Marketing automation setup'),
('INV-2024-033', 3, 1, 3650.00, '2024-11-10', '2024-12-10', '2024-11-28', 'paid', 'Digital innovation project'),
('INV-2024-034', 4, 2, 890.00, '2024-11-12', '2024-12-12', NULL, 'pending', 'Document management upgrade'),
('INV-2024-035', 5, 4, 750.00, '2024-11-15', '2024-12-15', NULL, 'pending', 'Software support package'),

-- December 2024 (Current month - mostly pending)
('INV-2024-036', 6, 1, 5200.00, '2024-12-01', '2024-12-31', NULL, 'pending', 'Year-end cloud optimization'),
('INV-2024-037', 7, 6, 1850.00, '2024-12-03', '2025-01-02', NULL, 'pending', 'End-of-year team retreat'),
('INV-2024-038', 8, 1, 2950.00, '2024-12-05', '2025-01-04', NULL, 'pending', 'Smart analytics enhancement'),
('INV-2024-039', 9, 3, 650.00, '2024-12-08', '2025-01-07', NULL, 'pending', 'Holiday office supplies'),
('INV-2024-040', 10, 2, 1450.00, '2024-12-10', '2025-01-09', NULL, 'pending', 'Document archive project');

-- Add indexes for better performance
CREATE INDEX idx_invoices_vendor_id ON invoices("vendorId");
CREATE INDEX idx_invoices_category_id ON invoices("categoryId");
CREATE INDEX idx_invoices_issue_date ON invoices("issueDate");
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_amount ON invoices("totalAmount");

-- Create views for common queries
CREATE VIEW invoice_summary AS
SELECT 
    i.id,
    i."invoiceId",
    v.name as vendor_name,
    c.name as category_name,
    i."totalAmount",
    i."issueDate",
    i."dueDate",
    i."paymentDate",
    i.status,
    i.description
FROM invoices i
LEFT JOIN vendors v ON i."vendorId" = v.id
LEFT JOIN categories c ON i."categoryId" = c.id;

-- Summary statistics view
CREATE VIEW analytics_summary AS
SELECT 
    COUNT(*) as total_invoices,
    SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) as paid_invoices,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_invoices,
    SUM("totalAmount") as total_amount,
    SUM(CASE WHEN status = 'paid' THEN "totalAmount" ELSE 0 END) as paid_amount,
    SUM(CASE WHEN status = 'pending' THEN "totalAmount" ELSE 0 END) as pending_amount,
    AVG("totalAmount") as average_invoice_amount
FROM invoices;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flowbit_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO flowbit_user;

-- Display summary
SELECT 'Database setup complete!' as status;
SELECT * FROM analytics_summary;