import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Database, Table as TableIcon } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sql?: string;
  results?: any[];
  timestamp: Date;
}

// Mock responses - replace with actual API call to /chat-with-data
const mockResponses: Record<string, { sql: string; results: any[] }> = {
  'total spend': {
    sql: 'SELECT SUM(amount) as total_spend FROM invoices WHERE date >= CURRENT_DATE - INTERVAL \'90 days\'',
    results: [{ total_spend: 64748.81 }],
  },
  'top 5 vendors': {
    sql: 'SELECT vendor, SUM(amount) as total_spend FROM invoices GROUP BY vendor ORDER BY total_spend DESC LIMIT 5',
    results: [
      { vendor: 'OmegaLtd', total_spend: 15000.00 },
      { vendor: 'Test Solution', total_spend: 12300.00 },
      { vendor: 'Global Supply', total_spend: 8679.25 },
      { vendor: 'Infomedics', total_spend: 6200.00 },
      { vendor: 'DataServices', total_spend: 13000.00 },
    ],
  },
  'overdue': {
    sql: 'SELECT id, vendor, date, amount FROM invoices WHERE status = \'Overdue\' AND date < CURRENT_DATE',
    results: [
      { id: 'INV-004', vendor: 'Infomedics', date: '2025-10-22', amount: 6200.00 },
      { id: 'INV-010', vendor: 'Test Solution', date: '2025-11-07', amount: 3800.00 },
    ],
  },
};

export function ChatWithData() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Simulate API call to /chat-with-data
    setTimeout(() => {
      // Find matching mock response
      let response = null;
      const query = inputValue.toLowerCase();
      
      if (query.includes('total spend') || query.includes('90 days')) {
        response = mockResponses['total spend'];
      } else if (query.includes('top') && query.includes('vendor')) {
        response = mockResponses['top 5 vendors'];
      } else if (query.includes('overdue')) {
        response = mockResponses['overdue'];
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response 
          ? 'I\'ve executed your query and found the following results:'
          : 'I couldn\'t find specific data for that query. Please try asking about total spend, top vendors, or overdue invoices.',
        sql: response?.sql,
        results: response?.results,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const suggestedQueries = [
    "What's the total spend in the last 90 days?",
    "List top 5 vendors by spend",
    "Show overdue invoices as of today",
  ];

  return (
    <div className="flex flex-col h-full bg-white rounded-lg border border-gray-200">
      {/* Header */}
      <div className="p-4 sm:p-6 border-b border-gray-200">
        <h2 className="mb-1">Chat with Data</h2>
        <p className="text-xs text-gray-500">
          Ask questions about your invoices and get instant insights powered by AI
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <Database className="w-12 h-12 text-gray-300 mb-4" />
            <h3 className="text-gray-600 mb-2">Start asking questions</h3>
            <p className="text-sm text-gray-500 mb-6">
              Try one of these example queries:
            </p>
            <div className="space-y-2 w-full max-w-md">
              {suggestedQueries.map((query, index) => (
                <button
                  key={index}
                  onClick={() => setInputValue(query)}
                  className="w-full px-4 py-3 text-sm text-left bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors border border-gray-200"
                >
                  {query}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-4 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>

              {/* SQL Display */}
              {message.sql && (
                <div className="mt-4 pt-4 border-t border-gray-300">
                  <div className="flex items-center gap-2 mb-2">
                    <Database className="w-4 h-4 text-gray-600" />
                    <span className="text-xs text-gray-600">Generated SQL:</span>
                  </div>
                  <pre className="bg-gray-900 text-green-400 p-3 rounded text-xs overflow-x-auto">
                    {message.sql}
                  </pre>
                </div>
              )}

              {/* Results Table */}
              {message.results && message.results.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-300">
                  <div className="flex items-center gap-2 mb-2">
                    <TableIcon className="w-4 h-4 text-gray-600" />
                    <span className="text-xs text-gray-600">Results:</span>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs border border-gray-300 rounded">
                      <thead className="bg-gray-200">
                        <tr>
                          {Object.keys(message.results[0]).map((key) => (
                            <th key={key} className="px-3 py-2 text-left border-b border-gray-300">
                              {key.replace(/_/g, ' ').toUpperCase()}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="bg-white">
                        {message.results.map((row, idx) => (
                          <tr key={idx} className="border-b border-gray-200 last:border-0">
                            {Object.values(row).map((value: any, colIdx) => (
                              <td key={colIdx} className="px-3 py-2">
                                {typeof value === 'number' 
                                  ? value.toLocaleString('en-US', { 
                                      minimumFractionDigits: 2,
                                      maximumFractionDigits: 2 
                                    })
                                  : value}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              <div className="mt-2 text-xs opacity-70">
                {message.timestamp.toLocaleTimeString('en-US', {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-4 flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
              <span className="text-sm text-gray-600">Analyzing your query...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 sm:p-6 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about your data..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
