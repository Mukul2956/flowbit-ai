const { Client } = require('pg');

// Test departments using direct SQL instead of Prisma
const testDepartmentsSQL = async () => {
  const connectionString = 'postgresql://postgres.ogohcxuwjtfpwnxejpey:mukul%40237lassi@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres';
  
  const client = new Client({
    connectionString: connectionString
  });

  try {
    await client.connect();
    console.log('🔍 Testing department analytics with SQL...');
    
    // Get all invoices using actual column names
    const invoicesResult = await client.query(`
      SELECT id, "invoiceId" as invoice_number, "totalAmount" as total_amount 
      FROM invoices 
      ORDER BY id
    `);
    
    const allInvoices = invoicesResult.rows;
    console.log(`� Retrieved ${allInvoices.length} invoices`);
    
    if (allInvoices.length > 0) {
      console.log('Sample invoice:', allInvoices[0]);
    }
    
    // Create department mapping
    const departments = [
      { name: 'IT', invoices: [] },
      { name: 'Finance', invoices: [] },
      { name: 'Operations', invoices: [] },
      { name: 'Marketing', invoices: [] },
      { name: 'HR', invoices: [] }
    ];

    // Distribute invoices across departments
    allInvoices.forEach((invoice, index) => {
      const deptIndex = index % departments.length;
      departments[deptIndex].invoices.push(invoice);
    });

    // Calculate department analytics
    const departmentAnalytics = departments.map((dept) => {
      const totalSpend = dept.invoices.reduce((sum, inv) => 
        sum + Number(inv.total_amount), 0);
      const invoiceCount = dept.invoices.length;
      const avgInvoiceValue = invoiceCount > 0 ? totalSpend / invoiceCount : 0;
      const budgetAllocated = totalSpend * 1.3;
      const budgetUtilized = budgetAllocated > 0 ? (totalSpend / budgetAllocated) * 100 : 0;

      return {
        department: dept.name,
        total_spend: totalSpend,
        invoice_count: invoiceCount,
        avg_invoice_value: avgInvoiceValue,
        budget_allocated: budgetAllocated,
        budget_utilized: budgetUtilized
      };
    });

    console.log('\n🏢 Department Analytics Results:');
    departmentAnalytics.forEach(dept => {
      console.log(`${dept.department}: ${dept.invoice_count} invoices, €${dept.total_spend.toFixed(2)} total`);
    });
    
    console.log('\n✅ Department analytics works with SQL queries!');
    console.log('\n📋 Full result for API:');
    console.log(JSON.stringify(departmentAnalytics, null, 2));
    
  } catch (error) {
    console.error('❌ Error testing departments:', error);
  } finally {
    await client.end();
  }
};

testDepartmentsSQL();