# API Documentation - FlowbitAI

## Base URLs

- **Development**: `http://localhost:3001`
- **Production**: `https://flowbit-ai.vercel.app`

## Authentication

Currently, the API uses IP-based rate limiting. No authentication required for public endpoints.

## Rate Limiting

- **Window**: 15 minutes
- **Limit**: 100 requests per IP
- **Headers**: Rate limit info included in response headers

## Common Headers

```bash
Content-Type: application/json
Access-Control-Allow-Origin: *
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1234567890
```

---

## Analytics Endpoints

### GET /api/analytics/summary

Returns overall financial summary statistics.

**Response:**
```json
{
  "total_amount": 115670.38,
  "paid_invoices": 39,
  "pending_invoices": 11,
  "total_invoices": 50,
  "average_amount": 2313.41,
  "paid_amount": 89234.50,
  "pending_amount": 26435.88
}
```

### GET /api/analytics/category-spend

Returns spending breakdown by category.

**Response:**
```json
[
  {
    "name": "General",
    "value": 111000.50,
    "count": 42,
    "percentage": 96.0
  },
  {
    "name": "Document", 
    "value": 4669.88,
    "count": 8,
    "percentage": 4.0
  }
]
```

### GET /api/analytics/vendor-spend

Returns spending breakdown by vendor.

**Parameters:**
- `limit` (optional): Number of results to return (default: 10)
- `sort` (optional): Sort order - 'desc' or 'asc' (default: 'desc')

**Response:**
```json
[
  {
    "vendor_name": "TechCorp Solutions",
    "total_amount": 15250.00,
    "invoice_count": 8,
    "average_amount": 1906.25,
    "last_invoice_date": "2024-11-05"
  }
]
```

### GET /api/analytics/monthly-trend

Returns monthly spending trends.

**Parameters:**
- `year` (optional): Year to filter by (default: current year)
- `months` (optional): Number of months to include (default: 12)

**Response:**
```json
[
  {
    "month": "2024-01",
    "total_amount": 9800.00,
    "invoice_count": 5,
    "paid_amount": 9800.00,
    "pending_amount": 0
  }
]
```

---

## Chat Endpoints

### POST /api/chat

Processes natural language queries and returns SQL results.

**Request:**
```json
{
  "question": "What is our total spending this year?",
  "context": {
    "user_id": "optional",
    "session_id": "optional"
  }
}
```

**Response:**
```json
{
  "query": "SELECT SUM(totalAmount) as total FROM invoices WHERE EXTRACT(YEAR FROM issueDate) = 2024",
  "result": [
    {
      "total": "115670.38"
    }
  ],
  "explanation": "The total spending for 2024 is €115,670.38 across 50 invoices.",
  "execution_time": 0.045,
  "rows_affected": 1
}
```

**Error Response:**
```json
{
  "error": "Unable to process query",
  "details": "Could not generate valid SQL from the question",
  "suggestion": "Try rephrasing your question or asking about invoices, vendors, or categories"
}
```

### Example Chat Queries

#### Financial Analytics
```json
{
  "question": "Show me invoices over €2000 that are still pending"
}
```

#### Vendor Analysis
```json
{
  "question": "Which vendor has sent us the most invoices this quarter?"
}
```

#### Time-based Queries
```json
{
  "question": "Compare our spending between Q3 and Q4 2024"
}
```

---

## Invoice Endpoints

### GET /api/invoices

Returns paginated list of invoices.

**Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `status` (optional): Filter by status ('paid', 'pending')
- `vendor_id` (optional): Filter by vendor ID
- `category_id` (optional): Filter by category ID
- `date_from` (optional): Filter from date (YYYY-MM-DD)
- `date_to` (optional): Filter to date (YYYY-MM-DD)
- `sort` (optional): Sort field ('date', 'amount', 'vendor')
- `order` (optional): Sort order ('asc', 'desc')

**Response:**
```json
{
  "invoices": [
    {
      "id": 1,
      "invoiceId": "INV-2024-001",
      "vendor": {
        "id": 1,
        "name": "TechCorp Solutions"
      },
      "category": {
        "id": 1,
        "name": "General"
      },
      "totalAmount": 1250.00,
      "issueDate": "2024-01-15",
      "dueDate": "2024-02-14",
      "paymentDate": "2024-02-10",
      "status": "paid",
      "description": "Software development services"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 3,
    "total_items": 50,
    "items_per_page": 20
  }
}
```

### GET /api/invoices/:id

Returns specific invoice details.

**Response:**
```json
{
  "id": 1,
  "invoiceId": "INV-2024-001",
  "vendor": {
    "id": 1,
    "name": "TechCorp Solutions",
    "email": "billing@techcorp.com",
    "phone": "+49 30 12345678"
  },
  "category": {
    "id": 1,
    "name": "General",
    "description": "General business expenses"
  },
  "totalAmount": 1250.00,
  "issueDate": "2024-01-15",
  "dueDate": "2024-02-14", 
  "paymentDate": "2024-02-10",
  "status": "paid",
  "description": "Software development services",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Vendor Endpoints

### GET /api/vendors

Returns list of all vendors.

**Response:**
```json
[
  {
    "id": 1,
    "name": "TechCorp Solutions",
    "email": "billing@techcorp.com",
    "phone": "+49 30 12345678",
    "address": "Friedrichstraße 123, 10117 Berlin, Germany",
    "invoice_count": 8,
    "total_amount": 15250.00
  }
]
```

### GET /api/vendors/:id/invoices

Returns invoices for a specific vendor.

**Parameters:**
- Same pagination and filtering options as `/api/invoices`

**Response:**
```json
{
  "vendor": {
    "id": 1,
    "name": "TechCorp Solutions"
  },
  "invoices": [...],
  "summary": {
    "total_amount": 15250.00,
    "invoice_count": 8,
    "paid_amount": 12750.00,
    "pending_amount": 2500.00
  }
}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": "Detailed error description",
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/invoices/999"
}
```

### Common Error Codes

- **400 Bad Request**: Invalid parameters or request format
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: AI service unavailable

### Error Examples

**Invalid Invoice ID:**
```json
{
  "error": "Invoice not found",
  "code": "INVOICE_NOT_FOUND",
  "details": "No invoice exists with ID 999"
}
```

**Rate Limit Exceeded:**
```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED", 
  "details": "Too many requests. Try again in 15 minutes."
}
```

---

## Health Check

### GET /health

Returns API health status.

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2024-01-15T10:30:00Z",
  "uptime": 12345,
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "ai_service": "connected"
  }
}
```

---

## Testing with cURL

### Get Analytics Summary
```bash
curl -X GET https://flowbit-ai.vercel.app/api/analytics/summary
```

### Chat Query
```bash
curl -X POST https://flowbit-ai.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is our total spending this year?"}'
```

### Get Invoices with Filters
```bash
curl -X GET "https://flowbit-ai.vercel.app/api/invoices?status=pending&limit=10"
```