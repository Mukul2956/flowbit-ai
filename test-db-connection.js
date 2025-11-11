const { Client } = require('pg');

const connectionString = 'postgresql://postgres:mukul%40237lassi@db.ogohcxuwjtfpwnxejpey.supabase.co:5432/postgres';

async function testConnection() {
  const client = new Client({
    connectionString: connectionString
  });

  try {
    console.log('Attempting to connect to database...');
    await client.connect();
    console.log('✅ Database connection successful!');
    
    const result = await client.query('SELECT NOW()');
    console.log('Database time:', result.rows[0].now);
    
  } catch (error) {
    console.error('❌ Database connection failed:', error.message);
  } finally {
    await client.end();
  }
}

testConnection();