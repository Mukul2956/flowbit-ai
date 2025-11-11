const { Client } = require('pg');

// Test with correct Supabase connection parameters
const testConnection = async () => {
  const connectionString = 'postgresql://postgres.ogohcxuwjtfpwnxejpey:mukul%40237lassi@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres';
  
  const client = new Client({
    connectionString: connectionString
  });

  try {
    console.log('🔍 Testing with correct Supabase parameters...');
    console.log('Host: aws-1-ap-southeast-1.pooler.supabase.com');
    console.log('Port: 6543 (Transaction Pooler)');
    console.log('User: postgres.ogohcxuwjtfpwnxejpey');
    console.log('Password: mukul@237lassi (URL encoded)');
    
    await client.connect();
    console.log('✅ Successfully connected to Supabase database!');
    
    const result = await client.query('SELECT version()');
    console.log('Database version:', result.rows[0].version.substring(0, 80) + '...');
    
    // Test if we can query tables
    const tableResult = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);
    console.log('\n📋 Available tables:');
    tableResult.rows.forEach(row => console.log(`  - ${row.table_name}`));
    
    // Test a simple count query
    try {
      const countResult = await client.query('SELECT COUNT(*) as count FROM invoices');
      console.log(`\n📊 Total invoices: ${countResult.rows[0].count}`);
    } catch (countError) {
      console.log('Note: Could not count invoices (table might be empty or have RLS enabled)');
    }
    
  } catch (error) {
    console.error('❌ Database connection failed:', error.message);
    console.error('Full error:', error);
  } finally {
    await client.end().catch(() => {});
  }
};

testConnection();