const { Client } = require('pg');

// Check the actual structure of the invoices table
const checkInvoicesStructure = async () => {
  const connectionString = 'postgresql://postgres.ogohcxuwjtfpwnxejpey:mukul%40237lassi@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres';
  
  const client = new Client({
    connectionString: connectionString
  });

  try {
    await client.connect();
    console.log('✅ Connected to database');
    
    // Check column names in invoices table
    const columnResult = await client.query(`
      SELECT column_name, data_type 
      FROM information_schema.columns 
      WHERE table_name = 'invoices' 
      AND table_schema = 'public'
      ORDER BY ordinal_position
    `);
    
    console.log('\n📋 Columns in invoices table:');
    columnResult.rows.forEach(row => console.log(`  - ${row.column_name}: ${row.data_type}`));
    
    // Try to get a sample invoice to see the actual data
    const sampleResult = await client.query('SELECT * FROM invoices LIMIT 1');
    if (sampleResult.rows.length > 0) {
      console.log('\n📄 Sample invoice:');
      console.log(JSON.stringify(sampleResult.rows[0], null, 2));
    }
    
  } catch (error) {
    console.error('❌ Database operation failed:', error.message);
  } finally {
    await client.end().catch(() => {});
  }
};

checkInvoicesStructure();

// Fix users table to match Prisma schema
const fixUsersTable = async () => {
  const connectionString = 'postgresql://postgres.ogohcxuwjtfpwnxejpey:mukul%40237lassi@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres';
  
  const client = new Client({
    connectionString: connectionString
  });

  try {
    await client.connect();
    console.log('✅ Connected to database');
    
    // Drop existing users table if it has wrong structure
    await client.query('DROP TABLE IF EXISTS public.users CASCADE');
    console.log('�️ Dropped existing users table');
    
    // Create users table matching Prisma schema
    await client.query(`
      CREATE TABLE public.users (
        id VARCHAR(30) PRIMARY KEY DEFAULT gen_random_uuid()::text,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        "passwordHash" VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'VIEWER' CHECK (role IN ('ADMIN', 'MANAGER', 'ACCOUNTANT', 'VIEWER')),
        department VARCHAR(100),
        "isActive" BOOLEAN DEFAULT true,
        "lastLoginAt" TIMESTAMP,
        "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    console.log('📋 Created users table with Prisma schema structure');
    
    // Insert sample users with proper structure
    await client.query(`
      INSERT INTO public.users (id, name, email, "passwordHash", role, department, "isActive") VALUES
      ('usr_' || substring(gen_random_uuid()::text, 1, 8), 'John Doe', 'john.doe@company.com', '$2a$10$dummyhash1', 'ADMIN', 'IT', true),
      ('usr_' || substring(gen_random_uuid()::text, 1, 8), 'Jane Smith', 'jane.smith@company.com', '$2a$10$dummyhash2', 'MANAGER', 'Finance', true),
      ('usr_' || substring(gen_random_uuid()::text, 1, 8), 'Mike Johnson', 'mike.johnson@company.com', '$2a$10$dummyhash3', 'ACCOUNTANT', 'Operations', true),
      ('usr_' || substring(gen_random_uuid()::text, 1, 8), 'Sarah Wilson', 'sarah.wilson@company.com', '$2a$10$dummyhash4', 'VIEWER', 'Marketing', true),
      ('usr_' || substring(gen_random_uuid()::text, 1, 8), 'David Brown', 'david.brown@company.com', '$2a$10$dummyhash5', 'MANAGER', 'HR', true)
      ON CONFLICT (email) DO NOTHING
    `);
    
    console.log('✅ Inserted sample users with proper Prisma format');
    
    // Verify the table
    const userCount = await client.query('SELECT COUNT(*) as count FROM users');
    console.log(`� Total users in database: ${userCount.rows[0].count}`);
    
  } catch (error) {
    console.error('❌ Database operation failed:', error.message);
  } finally {
    await client.end().catch(() => {});
  }
};

fixUsersTable();