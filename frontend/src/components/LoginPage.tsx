import React, { useState } from 'react'
import { Brain, Rocket, Shield, Sparkles, Eye, EyeOff } from 'lucide-react'
import { api } from '../lib/api'

interface LoginPageProps {
  onLogin: (token: string, user: any) => void
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [isRegister, setIsRegister] = useState(false)
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (isRegister) {
        const result = await api.auth.register({ email, username, password, full_name: fullName || undefined })
        onLogin(result.access_token, result.user)
      } else {
        const result = await api.auth.login(email, password)
        onLogin(result.access_token, result.user)
      }
    } catch (err: any) {
      setError(err.message || 'حدث خطأ')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-500/5 via-transparent to-accent-500/5" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl" />

      <div className="relative w-full max-w-md mx-4">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 mb-4 shadow-lg shadow-primary-500/25">
            <Brain size={36} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold gradient-text">Gumroad AI Empire</h1>
          <p className="text-gray-400 mt-1">نظام التسويق الذكي المتكامل</p>
        </div>

        {/* Features */}
        <div className="flex justify-center gap-6 mb-8 text-center">
          {[
            { icon: Rocket, label: 'تسويق ذكي' },
            { icon: Sparkles, label: 'وكلاء AI' },
            { icon: Shield, label: 'أتمتة كاملة' },
          ].map(({ icon: Icon, label }) => (
            <div key={label} className="flex flex-col items-center gap-1.5">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500/20 to-accent-500/20 flex items-center justify-center">
                <Icon size={18} className="text-primary-300" />
              </div>
              <span className="text-xs text-gray-400">{label}</span>
            </div>
          ))}
        </div>

        {/* Form */}
        <div className="bg-gray-900/60 backdrop-blur-xl rounded-2xl border border-gray-800 p-6 shadow-xl">
          <h2 className="text-xl font-bold mb-6 text-center">
            {isRegister ? 'إنشاء حساب جديد' : 'تسجيل الدخول'}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {isRegister && (
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">الاسم الكامل (اختياري)</label>
                <input
                  type="text"
                  value={fullName}
                  onChange={e => setFullName(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 outline-none transition-all"
                  placeholder="محمد أحمد"
                  dir="auto"
                />
              </div>
            )}

            <div>
              <label className="block text-sm text-gray-400 mb-1.5">البريد الإلكتروني</label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 outline-none transition-all"
                placeholder="you@example.com"
                required
                dir="auto"
              />
            </div>

            {isRegister && (
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">اسم المستخدم</label>
                <input
                  type="text"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 outline-none transition-all"
                  placeholder="username"
                  required
                  dir="auto"
                />
              </div>
            )}

            <div>
              <label className="block text-sm text-gray-400 mb-1.5">كلمة المرور</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 focus:ring-1 focus:ring-primary-500 outline-none transition-all"
                  placeholder="••••••••"
                  required
                  dir="auto"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {error && (
              <div className="px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl font-bold text-white hover:shadow-lg hover:shadow-primary-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'جاري التحميل...' : isRegister ? 'إنشاء الحساب' : 'تسجيل الدخول'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => { setIsRegister(!isRegister); setError('') }}
              className="text-sm text-gray-400 hover:text-primary-300 transition-colors"
            >
              {isRegister ? 'لديك حساب بالفعل؟ سجل دخول' : 'ليس لديك حساب؟ أنشئ واحدًا'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
