import React from 'react'
import { BarChart3, TrendingUp, DollarSign, Activity, ArrowUp, ArrowDown } from 'lucide-react'

export function AnalyticsView() {
  const metrics = [
    { label: 'إجمالي الإيرادات', value: '$0.00', change: '+0%', icon: DollarSign, trend: 'up' },
    { label: 'معدل التحويل', value: '0%', change: '0%', icon: TrendingUp, trend: 'up' },
    { label: 'متوسط قيمة الطلب', value: '$0.00', change: '+0%', icon: Activity, trend: 'up' },
    { label: 'زوار فريدون', value: '0', change: '0%', icon: BarChart3, trend: 'up' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">التحليلات</h1>
        <p className="text-gray-400 mt-1">لوحة بيانات شاملة لأداء المبيعات والتسويق</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map(m => (
          <div key={m.label} className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-5">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500/20 to-accent-500/20 flex items-center justify-center">
                <m.icon size={18} className="text-primary-300" />
              </div>
              <span className="text-sm text-gray-400">{m.label}</span>
            </div>
            <p className="text-2xl font-bold mb-1">{m.value}</p>
            <div className="flex items-center gap-1">
              {m.trend === 'up' ? <ArrowUp size={14} className="text-green-400" /> : <ArrowDown size={14} className="text-red-400" />}
              <span className={`text-sm ${m.trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>{m.change}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Charts placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6">
          <h3 className="font-bold mb-4">المبيعات على مدار الشهر</h3>
          <div className="h-64 flex items-center justify-center bg-gray-950/50 rounded-xl">
            <p className="text-gray-500">بيانات المبيعات ستظهر هنا بعد بدء التشغيل</p>
          </div>
        </div>
        <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6">
          <h3 className="font-bold mb-4">أداء القنوات التسويقية</h3>
          <div className="h-64 flex items-center justify-center bg-gray-950/50 rounded-xl">
            <p className="text-gray-500">تحليلات القنوات ستظهر هنا بعد بدء التشغيل</p>
          </div>
        </div>
      </div>
    </div>
  )
}
