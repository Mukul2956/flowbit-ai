import { Menu, MoreVertical } from 'lucide-react';

interface HeaderProps {
  onMenuClick?: () => void;
  title?: string;
}

export function Header({ onMenuClick, title = 'Dashboard' }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button 
            onClick={onMenuClick}
            className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
          >
            <Menu className="w-6 h-6" />
          </button>
          <h1 className="text-xl">{title}</h1>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gray-200 overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop" 
              alt="Amit Jadhav"
              className="w-full h-full object-cover"
            />
          </div>
          <div className="hidden sm:block">
            <div className="text-sm">Amit Jadhav</div>
          </div>
          <button className="p-1 hover:bg-gray-100 rounded">
            <MoreVertical className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>
    </header>
  );
}
