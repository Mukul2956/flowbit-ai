# Database Schema Documentation

## Overview

FlowbitAI uses PostgreSQL as its primary database with a simple yet effective schema for invoice analytics. The database is designed for optimal query performance and natural language processing.

## Entity Relationship Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   CATEGORIES    │     │    VENDORS      │     │    INVOICES     │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │     │ id (PK)         │
│ name            │────┐│ name            │────┐│ invoiceId       │
│ description     │    ││ email           │    ││ vendorId (FK)   │
│ created_at      │    ││ phone           │    ││ categoryId (FK) │
└─────────────────┘    ││ address         │    ││ totalAmount     │
                       ││ created_at      │    ││ issueDate       │
                       │└─────────────────┘    ││ dueDate         │
                       │                       ││ paymentDate     │
                       │                       ││ status          │
                       │                       ││ description     │
                       │                       ││ created_at      │
                       │                       │└─────────────────┘
                       │                       │
                       └───────────────────────┘
                        Categories (1) ──── (Many) Invoices
                        Vendors (1) ────────── (Many) Invoices
```

## Table Definitions

### Categories Table

Stores invoice categories for grouping and analysis.

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `id`: Primary key, auto-incrementing
- `name`: Category name (e.g., "General", "Document", "Office Supplies")
- `description`: Optional detailed description
- `created_at`: Record creation timestamp

**Constraints:**
- `name` must be unique
- `name` cannot be null

### Vendors Table

Stores vendor/supplier information.

```sql
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `id`: Primary key, auto-incrementing
- `name`: Vendor company name
- `email`: Contact email address
- `phone`: Contact phone number
- `address`: Full address
- `created_at`: Record creation timestamp

**Constraints:**
- `name` cannot be null

### Invoices Table

Core table storing all invoice data with camelCase column names for JavaScript compatibility.

```sql
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
```

**Columns:**
- `id`: Primary key, auto-incrementing
- `invoiceId`: Business invoice identifier (e.g., "INV-2024-001")
- `vendorId`: Foreign key to vendors table
- `categoryId`: Foreign key to categories table
- `totalAmount`: Invoice total in decimal format (up to 99,999,999.99)
- `issueDate`: Date invoice was issued
- `dueDate`: Payment due date (optional)
- `paymentDate`: Actual payment date (null if unpaid)
- `status`: Payment status ('paid', 'pending', 'overdue')
- `description`: Additional details or notes
- `created_at`: Record creation timestamp

**Constraints:**
- `invoiceId` cannot be null
- `totalAmount` cannot be null and must be positive
- `issueDate` cannot be null
- Foreign key relationships with vendors and categories

## Indexes

Performance-optimized indexes for common query patterns:

```sql
-- Vendor lookup optimization
CREATE INDEX idx_invoices_vendor_id ON invoices("vendorId");

-- Category analysis optimization  
CREATE INDEX idx_invoices_category_id ON invoices("categoryId");

-- Date-based queries optimization
CREATE INDEX idx_invoices_issue_date ON invoices("issueDate");

-- Status filtering optimization
CREATE INDEX idx_invoices_status ON invoices(status);

-- Amount-based queries optimization
CREATE INDEX idx_invoices_amount ON invoices("totalAmount");

-- Composite index for common analytics queries
CREATE INDEX idx_invoices_status_date ON invoices(status, "issueDate");

-- Descending amount index for "top spending" queries
CREATE INDEX idx_invoices_amount_desc ON invoices("totalAmount" DESC);
```

## Views

Pre-built views for common data access patterns:

### Invoice Summary View

Joins invoices with vendor and category information:

```sql
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
```

### Analytics Summary View

Pre-calculated analytics for dashboard display:

```sql
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
```

## Sample Data

The database includes 40 sample invoices across 6 categories and 10 vendors:

### Categories
1. **General** (42 invoices) - €111,000.50
2. **Document** (8 invoices) - €4,669.88
3. **Office Supplies** - Office equipment and supplies
4. **Software** - Software licenses and subscriptions
5. **Marketing** - Marketing and advertising expenses
6. **Travel** - Travel and accommodation expenses

### Vendors
1. **TechCorp Solutions** - Berlin-based technology company
2. **Global Services GmbH** - München business services
3. **Digital Innovations AG** - Hamburg digital agency
4. **Business Solutions Ltd** - Köln consulting firm
5. **Enterprise Systems** - Stuttgart enterprise software
6. **CloudTech Partners** - Dresden cloud services
7. **Innovation Hub GmbH** - Hannover innovation center
8. **Smart Solutions AG** - Mannheim automation
9. **Future Technologies** - Essen technology services
10. **Advanced Systems Ltd** - Kassel advanced systems

### Invoice Distribution

**By Status:**
- **Paid**: 35 invoices (€89,234.50)
- **Pending**: 15 invoices (€26,435.88)

**By Time Period:**
- **Q1 2024**: 12 invoices (€19,800.00)
- **Q2 2024**: 13 invoices (€26,450.00)
- **Q3 2024**: 10 invoices (€21,200.00)
- **Q4 2024**: 15 invoices (€48,220.38)

## Query Examples

### Basic Analytics
```sql
-- Total spending by status
SELECT 
    status,
    COUNT(*) as invoice_count,
    SUM("totalAmount") as total_amount,
    AVG("totalAmount") as average_amount
FROM invoices 
GROUP BY status;

-- Monthly spending trend
SELECT 
    DATE_TRUNC('month', "issueDate") as month,
    SUM("totalAmount") as monthly_total,
    COUNT(*) as invoice_count
FROM invoices 
GROUP BY month 
ORDER BY month;
```

### Vendor Analysis
```sql
-- Top vendors by spending
SELECT 
    v.name,
    COUNT(i.id) as invoice_count,
    SUM(i."totalAmount") as total_spent,
    AVG(i."totalAmount") as average_invoice
FROM vendors v
JOIN invoices i ON v.id = i."vendorId"
GROUP BY v.id, v.name
ORDER BY total_spent DESC
LIMIT 10;
```

### Category Breakdown
```sql
-- Category spending distribution
SELECT 
    c.name as category,
    COUNT(i.id) as invoice_count,
    SUM(i."totalAmount") as total_amount,
    ROUND(
        SUM(i."totalAmount") * 100.0 / 
        (SELECT SUM("totalAmount") FROM invoices), 
        2
    ) as percentage
FROM categories c
JOIN invoices i ON c.id = i."categoryId"
GROUP BY c.id, c.name
ORDER BY total_amount DESC;
```

### Advanced Queries
```sql
-- Vendors with both high and low value invoices
SELECT v.name
FROM vendors v
JOIN invoices i ON v.id = i."vendorId"
GROUP BY v.id, v.name
HAVING 
    MAX(i."totalAmount") > 2000 
    AND MIN(i."totalAmount") < 500;

-- Monthly payment efficiency
SELECT 
    DATE_TRUNC('month', "issueDate") as month,
    AVG(
        CASE 
            WHEN "paymentDate" IS NOT NULL 
            THEN "paymentDate" - "issueDate"
        END
    ) as avg_payment_days
FROM invoices 
WHERE "paymentDate" IS NOT NULL
GROUP BY month
ORDER BY month;
```

## Data Types and Constraints

### Decimal Precision
- `totalAmount`: DECIMAL(10,2) allows values up to 99,999,999.99
- All monetary calculations maintain precision

### Date Handling
- All dates stored in DATE format (YYYY-MM-DD)
- Timestamps in TIMESTAMP format with timezone support
- NULL values allowed for optional dates (`dueDate`, `paymentDate`)

### String Lengths
- `invoiceId`: VARCHAR(100) - accommodates various formats
- Vendor `name`: VARCHAR(255) - standard business name length
- Category `name`: VARCHAR(100) - category identifiers
- `status`: VARCHAR(50) - status values
- `description`: TEXT - unlimited length for details

## Migration Scripts

For schema updates, use versioned migration scripts:

```sql
-- Migration: Add payment terms column
ALTER TABLE invoices 
ADD COLUMN payment_terms VARCHAR(50) DEFAULT '30 days';

-- Migration: Add vendor tax ID
ALTER TABLE vendors 
ADD COLUMN tax_id VARCHAR(50);

-- Migration: Add invoice currency
ALTER TABLE invoices 
ADD COLUMN currency VARCHAR(3) DEFAULT 'EUR';
```

## Performance Considerations

### Query Optimization
- Use indexes for WHERE clauses on commonly filtered columns
- Avoid SELECT * in production queries
- Use LIMIT for paginated results
- Consider materialized views for complex analytics

### Connection Management
- Use connection pooling (recommended: 10-20 connections)
- Close connections properly to prevent leaks
- Monitor active connections with `pg_stat_activity`

### Backup Strategy
- Daily automated backups recommended
- Point-in-time recovery capability
- Test backup restoration regularly

## Security

### Access Control
- Create dedicated application user with limited permissions
- Grant only necessary privileges (SELECT, INSERT, UPDATE)
- Avoid using superuser accounts for applications

### Data Protection
- Use parameterized queries to prevent SQL injection
- Validate all input data
- Encrypt sensitive data at rest
- Use SSL/TLS for database connections

## Monitoring

### Performance Metrics
```sql
-- Monitor slow queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, attname, n_distinct
FROM pg_stats 
WHERE schemaname = 'public';

-- Database size monitoring
SELECT 
    pg_database.datname,
    pg_database_size(pg_database.datname) AS size
FROM pg_database;
```

---

This schema provides a solid foundation for the FlowbitAI analytics platform with room for future expansion and optimization.