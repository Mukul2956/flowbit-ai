const { createClient } = require('@supabase/supabase-js');

// Test Supabase client connection
const testSupabaseConnection = async () => {
  // You'll need to provide your Supabase URL and anon key
  const supabaseUrl = 'https://ogohcxuwjtfpwnxejpey.supabase.co';
  const supabaseKey = 'YOUR_ANON_KEY'; // Get this from Supabase dashboard → Settings → API
  
  const supabase = createClient(supabaseUrl, supabaseKey);
  
  try {
    console.log('Testing Supabase client connection...');
    
    // Test a simple query
    const { data, error } = await supabase
      .from('invoices')
      .select('count(*)', { count: 'exact', head: true });
    
    if (error) {
      console.error('❌ Supabase query failed:', error);
    } else {
      console.log('✅ Successfully connected to Supabase!');
      console.log('Invoice count:', data);
    }
    
  } catch (error) {
    console.error('❌ Supabase connection failed:', error.message);
  }
};

testSupabaseConnection();