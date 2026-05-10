import React, { useState, useEffect } from 'react'
import { Dashboard } from './components/Dashboard'
import { MarketingPanel } from './components/MarketingPanel'
import { ProductManager } from './components/ProductManager'
import { AgentConsole } from './components/AgentConsole'
import { AnalyticsView } from './components/AnalyticsView'
import { LoginPage } from './components/LoginPage'
import { Brain, Package, BarChart3, Users, Settings, LogOut, Menu, X, Zap, Sparkles } from 'lucide-react'

type Page = 'dashboard' | 'products' | 'marketing' | 'agents' | 'analytics' | 'settings'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentPage, setCurrentPage] = useState<Page>('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setIsLoggedIn(true)
      fetch('/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then(r => r.json())
        .then(u => setUser(u))
        .catch(() => {
          localStorage.removeItem('token')
          setIsLoggedIn(false)
        })
    }
  }, [])

  const handleLogin = (token: string, userData: any) => {
    localStorage.setItem('token', token)
    setUser(userData)
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setIsLoggedIn(false)
    setUser(null)
  }

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />
  }

  const navItems: { id: Page; label: string; icon: React.ReactNode }[] = [
    { id: 'dashboard', label: 'لوحة التحكم', icon: <Brain size={20} /> },
    { id: 'products', label: 'المنتجات', icon: <Package size={20} /> },
    { id: 'marketing', label: 'التسويق الذكي', icon: <Zap size={20} /> },
    { id: 'agents', label: 'الوكلاء AI', icon: <Sparkles size={20} /> },
    { id: 'analytics', label: 'التحليلات', icon: <BarChart3 size={20} /> },
  ]

  return (
    <div className="flex h-screen bg-gray-950" dir="rtl">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/60 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:static inset-y-0 right-0 z-50 w-72 bg-gray-900/80 backdrop-blur-xl
        border-l border-gray-800 transform transition-transform duration-300
        ${sidebarOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'}
      `}>
        <div className="flex flex-col h-full p-4">
          <div className="flex items-center gap-3 mb-8 px-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
              <Brain size={22} className="text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold gradient-text">AI Empire</h1>
              <p className="text-xs text-gray-400">نظام التسويق الذكي</p>
            </div>
          </div>

          <nav className="flex-1 space-y-1">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => { setCurrentPage(item.id); setSidebarOpen(false) }}
                className={`
                  w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium
                  transition-all duration-200
                  ${currentPage === item.id
                    ? 'bg-gradient-to-r from-primary-500/20 to-accent-500/20 text-white border border-primary-500/30'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }
                `}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            ))}
          </nav>

          <div className="border-t border-gray-800 pt-4 mt-4">
            <div className="flex items-center gap-3 px-3 mb-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-xs font-bold">
                {user?.username?.[0]?.toUpperCase() || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user?.username || 'User'}</p>
                <p className="text-xs text-gray-400">{user?.email || ''}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm text-red-400 hover:bg-red-500/10 transition-all"
            >
              <LogOut size={18} />
              <span>تسجيل الخروج</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <header className="sticky top-0 z-30 bg-gray-950/80 backdrop-blur-xl border-b border-gray-800">
          <div className="flex items-center justify-between px-4 lg:px-8 h-16">
            <button
              className="lg:hidden p-2 rounded-lg hover:bg-gray-800"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu size={24} />
            </button>

            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-primary-500/10 to-accent-500/10 border border-primary-500/20">
                <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                <span className="text-xs text-green-400 font-medium">النظام نشط</span>
              </div>
            </div>
          </div>
        </header>

        <div className="p-4 lg:p-8">
          {currentPage === 'dashboard' && <Dashboard user={user} />}
          {currentPage === 'products' && <ProductManager />}
          {currentPage === 'marketing' && <MarketingPanel />}
          {currentPage === 'agents' && <AgentConsole />}
          {currentPage === 'analytics' && <AnalyticsView />}
        </div>
      </main>
    </div>
  )
}
