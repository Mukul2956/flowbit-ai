-- Enable Row Level Security (RLS) for all tables
-- This should be run in your Supabase SQL Editor

-- Enable RLS for categories table
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;

-- Enable RLS for invoices table  
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;

-- Enable RLS for vendors table
ALTER TABLE public.vendors ENABLE ROW LEVEL SECURITY;

-- Create policies to allow access (adjust as needed for your use case)

-- Policy for categories (allow all operations for now)
CREATE POLICY "Allow all access to categories" ON public.categories
FOR ALL USING (true);

-- Policy for invoices (allow all operations for now)  
CREATE POLICY "Allow all access to invoices" ON public.invoices
FOR ALL USING (true);

-- Policy for vendors (allow all operations for now)
CREATE POLICY "Allow all access to vendors" ON public.vendors  
FOR ALL USING (true);

-- Note: The above policies allow unrestricted access
-- In production, you should implement proper user-based policies