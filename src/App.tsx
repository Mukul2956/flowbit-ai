import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { StatCard } from './components/StatCard';
import { InvoiceVolumeChart } from './components/InvoiceVolumeChart';
import { VendorSpendChart } from './components/VendorSpendChart';
import { CategorySpendChart } from './components/CategorySpendChart';
import { CashOutflowChart } from './components/CashOutflowChart';
import { InvoicesTable } from './components/InvoicesTable';
import { ChatWithData } from './components/ChatWithData';

// Mock data for stat cards
const totalSpendSparkline = [
  { value: 10 }, { value: 12 }, { value: 11 }, { value: 13 }, 
  { value: 15 }, { value: 14 }, { value: 16 }
];

const invoicesSparkline = [
  { value: 50 }, { value: 55 }, { value: 52 }, { value: 58 }, 
  { value: 62 }, { value: 60 }, { value: 64 }
];

const documentsSparkline = [
  { value: 20 }, { value: 18 }, { value: 19 }, { value: 17 }, 
  { value: 16 }, { value: 17 }, { value: 17 }
];

const avgValueSparkline = [
  { value: 2200 }, { value: 2300 }, { value: 2250 }, { value: 2350 }, 
  { value: 2400 }, { value: 2380 }, { value: 2455 }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Sidebar - Desktop */}
      <div className="hidden lg:block">
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      </div>

      {/* Sidebar - Mobile */}
      {sidebarOpen && (
        <>
          <div 
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
          <div className="fixed left-0 top-0 bottom-0 z-50 lg:hidden">
            <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
          </div>
        </>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          onMenuClick={() => setSidebarOpen(!sidebarOpen)} 
          title={activeTab === 'chat' ? 'Chat with Data' : 'Dashboard'}
        />
        
        <main className="flex-1 overflow-y-auto">
          {activeTab === 'dashboard' ? (
            <div className="p-4 sm:p-6 lg:p-8 max-w-[1600px] mx-auto">
              {/* Stats Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <StatCard
                  title="Total Spend"
                  subtitle="(YTD)"
                  value="€ 12.679,25"
                  comparison="+12% from last month"
                  trend="up"
                  sparklineData={totalSpendSparkline}
                />
                <StatCard
                  title="Total Invoices Processed"
                  subtitle=""
                  value="64"
                  comparison="+8% from last month"
                  trend="up"
                  sparklineData={invoicesSparkline}
                />
                <StatCard
                  title="Documents Uploaded"
                  subtitle="This Month"
                  value="17"
                  comparison="-3% from last month"
                  trend="down"
                  sparklineData={documentsSparkline}
                />
                <StatCard
                  title="Average Invoice Value"
                  subtitle=""
                  value="€ 2.455,00"
                  comparison="+5% from last month"
                  trend="up"
                  sparklineData={avgValueSparkline}
                />
              </div>

              {/* Charts Row 1 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <InvoiceVolumeChart />
                <VendorSpendChart />
              </div>

              {/* Charts Row 2 */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <CategorySpendChart />
                <CashOutflowChart />
                <div className="lg:col-span-1">
                  <InvoicesTable />
                </div>
              </div>

              {/* Full Width Invoices Table */}
              <div className="mt-6">
                <InvoicesTable />
              </div>
            </div>
          ) : activeTab === 'chat' ? (
            <div className="h-full p-4 sm:p-6 lg:p-8 max-w-[1400px] mx-auto">
              <div className="h-full">
                <ChatWithData />
              </div>
            </div>
          ) : (
            <div className="p-4 sm:p-6 lg:p-8 max-w-[1600px] mx-auto">
              <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
                <h2 className="text-xl text-gray-600 mb-2">Coming Soon</h2>
                <p className="text-gray-500">This section is under development</p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
