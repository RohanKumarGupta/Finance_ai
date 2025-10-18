import { Outlet, NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { LayoutDashboard, CreditCard, Receipt, Bot, Bell, LogOut, Sparkles } from 'lucide-react'

export default function Layout() {
  const { user, logout } = useAuth()

  const navItems = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/payments', icon: CreditCard, label: 'Payments' },
    { to: '/receipts', icon: Receipt, label: 'Receipts' },
    { to: '/ai-assistant', icon: Bot, label: 'AI Assistant' },
    { to: '/reminders', icon: Bell, label: 'Reminders' },
  ]

  return (
    <div className="min-h-screen">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-300/30 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent-300/30 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Glass Header */}
      <header className="bg-white/70 backdrop-blur-xl border-b border-white/20 sticky top-0 z-50 shadow-glass">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center space-x-4">
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-primary rounded-2xl blur-md opacity-75 group-hover:opacity-100 transition-opacity"></div>
                <div className="relative w-14 h-14 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-primary">
                  <Sparkles className="w-7 h-7 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">Finance AI</h1>
                <p className="text-xs text-gray-600 font-medium">Smart Financial Management</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="hidden md:block text-right bg-white/60 backdrop-blur-sm rounded-xl px-4 py-2 border border-white/40">
                <p className="text-sm font-semibold text-gray-900">{user?.full_name}</p>
                <p className="text-xs text-gray-600">{user?.email}</p>
              </div>
              <button
                onClick={logout}
                className="p-3 text-gray-600 hover:text-primary-600 hover:bg-white/80 rounded-xl transition-all duration-300 hover:scale-110 group"
                title="Logout"
              >
                <LogOut className="w-5 h-5 group-hover:rotate-12 transition-transform" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Modern Navigation */}
      <nav className="bg-white/60 backdrop-blur-xl border-b border-white/20 sticky top-20 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-2 overflow-x-auto">
            {navItems.map(({ to, icon: Icon, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center space-x-2 px-5 py-4 rounded-t-xl text-sm font-semibold transition-all duration-300 whitespace-nowrap ${
                    isActive
                      ? 'bg-gradient-primary text-white shadow-primary transform scale-105'
                      : 'text-gray-600 hover:text-primary-600 hover:bg-white/80'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon className={`w-5 h-5 ${isActive ? 'animate-pulse' : ''}`} />
                    <span>{label}</span>
                  </>
                )}
              </NavLink>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="mt-auto py-6 border-t border-white/20 bg-white/40 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-600">
            © 2024 Finance AI Assistant. Powered by{' '}
            <span className="gradient-text">AI Technology</span>
          </p>
        </div>
      </footer>
    </div>
  )
}
