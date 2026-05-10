import React, { useState } from 'react'
import { api } from '../lib/api'
import { Plus, Package, DollarSign, Tag, FileText, Loader2, Globe, CheckCircle, AlertCircle } from 'lucide-react'

export function ProductManager() {
  const [showCreate, setShowCreate] = useState(false)
  const [loading, setLoading] = useState(false)
  const [publishing, setPublishing] = useState<string | null>(null)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)
  const [form, setForm] = useState({ title: '', description: '', price: 9.99, category: '', tags: '' })

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)
    try {
      await api.products.create({
        title: form.title,
        description: form.description,
        price: form.price,
        category: form.category,
        tags: form.tags,
      })
      setMessage({ type: 'success', text: 'تم إنشاء المنتج بنجاح!' })
      setShowCreate(false)
      setForm({ title: '', description: '', price: 9.99, category: '', tags: '' })
    } catch (err: any) {
      setMessage({ type: 'error', text: err.message })
    }
    setLoading(false)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">المنتجات</h1>
          <p className="text-gray-400 mt-1">إدارة المنتجات الرقمية والربط مع Gumroad</p>
        </div>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl font-bold hover:shadow-lg hover:shadow-primary-500/25 transition-all"
        >
          <Plus size={18} />
          منتج جديد
        </button>
      </div>

      {/* Create form */}
      {showCreate && (
        <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6">
          <h2 className="text-lg font-bold mb-4">إنشاء منتج جديد</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1.5">العنوان</label>
              <input
                type="text"
                value={form.title}
                onChange={e => setForm({ ...form, title: e.target.value })}
                className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 outline-none"
                placeholder="عنوان المنتج"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1.5">الوصف</label>
              <textarea
                value={form.description}
                onChange={e => setForm({ ...form, description: e.target.value })}
                className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 outline-none min-h-[100px]"
                placeholder="وصف المنتج..."
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">السعر ($)</label>
                <input
                  type="number"
                  step="0.01"
                  value={form.price}
                  onChange={e => setForm({ ...form, price: parseFloat(e.target.value) })}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white focus:border-primary-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">التصنيف</label>
                <input
                  type="text"
                  value={form.category}
                  onChange={e => setForm({ ...form, category: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 outline-none"
                  placeholder="تصنيف"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">الوسوم</label>
                <input
                  type="text"
                  value={form.tags}
                  onChange={e => setForm({ ...form, tags: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 outline-none"
                  placeholder="tag1, tag2"
                />
              </div>
            </div>

            {message && (
              <div className={`flex items-center gap-2 px-4 py-3 rounded-xl text-sm ${
                message.type === 'success' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'
              }`}>
                {message.type === 'success' ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
                {message.text}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl font-bold hover:shadow-lg transition-all disabled:opacity-50"
            >
              {loading ? <Loader2 size={18} className="animate-spin" /> : <Package size={18} />}
              {loading ? 'جاري الإنشاء...' : 'إنشاء المنتج'}
            </button>
          </form>
        </div>
      )}

      {/* Products list placeholder */}
      <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-12">
        <div className="text-center">
          <Package size={48} className="mx-auto text-gray-600 mb-4" />
          <h3 className="text-lg font-bold text-gray-400 mb-2">لا توجد منتجات بعد</h3>
          <p className="text-gray-500">أنشئ أول منتج رقمي لك باستخدام الذكاء الاصطناعي</p>
        </div>
      </div>
    </div>
  )
}
