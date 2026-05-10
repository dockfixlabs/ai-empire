import React, { useState } from 'react'
import { api } from '../lib/api'
import { Zap, Target, Mail, Globe, Rocket, Share2, Activity, Link, Users, Brain, AlertCircle, Loader2, Sparkles, MessageCircle } from 'lucide-react'

const CHANNELS = [
  { key: 'email_3d', label: 'Email 3D', icon: Mail, desc: 'إيميلات سلوكية عميقة', color: 'from-blue-500/20 to-indigo-500/20' },
  { key: 'seo_empire', label: 'SEO Empire', icon: Globe, desc: 'إمبراطورية محتوى SEO', color: 'from-green-500/20 to-emerald-500/20' },
  { key: 'launch', label: 'Launch', icon: Rocket, desc: 'إطلاق متعدد المنصات', color: 'from-purple-500/20 to-pink-500/20' },
  { key: 'viral_referral', label: 'Viral Referral', icon: Share2, desc: 'إحالة فيروسية', color: 'from-orange-500/20 to-amber-500/20' },
  { key: 'interactive', label: 'Interactive', icon: Activity, desc: 'محتوى تفاعلي', color: 'from-red-500/20 to-rose-500/20' },
  { key: 'partnership', label: 'Partnership', icon: Link, desc: 'شراكات تلقائية', color: 'from-indigo-500/20 to-violet-500/20' },
  { key: 'community_flywheel', label: 'Community', icon: MessageCircle, desc: 'مجتمع نابض', color: 'from-teal-500/20 to-cyan-500/20' },
]

export function MarketingPanel() {
  const [activeTab, setActiveTab] = useState<'channels' | 'master-plan'>('channels')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [productName, setProductName] = useState('')
  const [productPrice, setProductPrice] = useState('29.99')
  const [productDesc, setProductDesc] = useState('')

  const handleChannelExecute = async (channel: string) => {
    if (!productName) return
    setLoading(true)
    setResult(null)
    try {
      const res = await api.marketing.executeChannel(channel, {
        product: { name: productName, price: parseFloat(productPrice) || 29.99, description: productDesc || productName }
      })
      setResult({ channel, data: res.result || res })
    } catch (err: any) {
      setResult({ error: err.message })
    }
    setLoading(false)
  }

  const handleMasterPlan = async () => {
    if (!productName) return
    setLoading(true)
    setResult(null)
    try {
      const res = await api.marketing.masterPlan({
        product: { name: productName, price: parseFloat(productPrice) || 29.99, description: productDesc || productName }
      })
      setResult({ type: 'master_plan', data: res })
    } catch (err: any) {
      setResult({ error: err.message })
    }
    setLoading(false)
  }

  const tabs = [
    { id: 'channels', label: 'القنوات التسويقية', icon: Zap },
    { id: 'master-plan', label: 'الخطة المتكاملة', icon: Brain },
  ] as const

  return (
    <div className="space-6">
      <div>
        <h1 className="text-3xl font-bold">التسويق المبتكر</h1>
        <p className="text-gray-400 mt-1">7 قنوات تسويق بدون سوشيال ميديا — مدعومة بـ AI</p>
      </div>

      <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6">
        <h2 className="text-lg font-bold mb-4">بيانات المنتج</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <input type="text" value={productName} onChange={e => setProductName(e.target.value)}
            placeholder="اسم المنتج" className="px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 outline-none" />
          <input type="text" value={productPrice} onChange={e => setProductPrice(e.target.value)}
            placeholder="السعر $" className="px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 outline-none" />
          <input type="text" value={productDesc} onChange={e => setProductDesc(e.target.value)}
            placeholder="وصف المنتج (اختياري)" className="px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:border-primary-500 outline-none" />
        </div>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        {tabs.map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
              activeTab === tab.id
                ? 'bg-gradient-to-r from-primary-500/20 to-accent-500/20 text-white border border-primary-500/30'
                : 'bg-gray-800/50 text-gray-400 hover:text-white border border-gray-700/50'
            }`}
          >
            <tab.icon size={16} /> {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'channels' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {CHANNELS.map(ch => (
            <button key={ch.key} onClick={() => handleChannelExecute(ch.key)} disabled={loading || !productName}
              className={`bg-gradient-to-br ${ch.color} backdrop-blur-xl rounded-2xl border border-white/5 p-5 hover:border-white/20 transition-all text-right disabled:opacity-50`}
            >
              <ch.icon size={24} className="mb-2 text-gray-300" />
              <p className="text-sm font-bold">{ch.label}</p>
              <p className="text-xs text-gray-400 mt-1">{ch.desc}</p>
              <p className="text-xs text-primary-400 mt-2">{loading ? 'جاري...' : 'شغّل الوكيل →'}</p>
            </button>
          ))}
        </div>
      )}

      {activeTab === 'master-plan' && (
        <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6">
          <h2 className="text-lg font-bold mb-4">الخطة التسويقية المتكاملة</h2>
          <p className="text-gray-400 mb-4">يجمع كل القنوات الـ7 في خطة واحدة متكاملة مع جدول زمني 12 أسبوع</p>
          <button onClick={handleMasterPlan} disabled={loading || !productName}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl font-bold hover:shadow-lg transition-all disabled:opacity-50"
          >
            {loading ? <Loader2 size={18} className="animate-spin" /> : <Brain size={18} />}
            {loading ? 'جاري التوليد...' : 'توليد الخطة المتكاملة'}
          </button>
        </div>
      )}

      {result && !result.error && (
        <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6">
          <h3 className="font-bold mb-4 text-lg flex items-center gap-2">
            <Sparkles size={20} className="text-yellow-400" />
            {result.type === 'master_plan' ? 'الخطة المتكاملة' : `نتائج ${result.channel}`}
            {result.data?.master_plan && <span className="text-xs text-gray-400">({Object.keys(result.data.channels || {}).length} قنوات)</span>}
          </h3>
          <pre className="text-sm text-gray-300 overflow-auto max-h-96 bg-gray-950/50 rounded-xl p-4" dir="ltr">
            {JSON.stringify(result.data, null, 2)}
          </pre>
        </div>
      )}

      {result?.error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-6">
          <div className="flex items-center gap-2 text-red-400">
            <AlertCircle size={18} />
            <span>{result.error}</span>
          </div>
        </div>
      )}
    </div>
  )
}
