import { TrendingUp, TrendingDown } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';

interface StatCardProps {
  title: string;
  subtitle: string;
  value: string;
  comparison?: string;
  trend?: 'up' | 'down';
  sparklineData?: Array<{ value: number }>;
}

export function StatCard({ 
  title, 
  subtitle, 
  value, 
  comparison, 
  trend,
  sparklineData 
}: StatCardProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 sm:p-6">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="text-sm text-gray-600 mb-1">{title}</div>
          <div className="text-xs text-gray-400">{subtitle}</div>
        </div>
        {sparklineData && (
          <div className="w-16 h-8">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={sparklineData}>
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke={trend === 'up' ? '#10b981' : '#ef4444'}
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
      
      <div className="flex items-end justify-between">
        <div className="text-2xl sm:text-3xl">{value}</div>
        
        {comparison && (
          <div className={`flex items-center gap-1 text-sm ${
            trend === 'up' ? 'text-green-600' : 'text-red-600'
          }`}>
            {trend === 'up' ? (
              <TrendingUp className="w-4 h-4" />
            ) : (
              <TrendingDown className="w-4 h-4" />
            )}
            <span>{comparison}</span>
          </div>
        )}
      </div>
    </div>
  );
}
