import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Brain, Activity, Server, Database, Wifi, Cpu, Clock, Zap, Mail, Globe, Rocket, Share2, Target, Link, Users, Search, TrendingUp, MessageCircle, Sparkles, Play, Square, RefreshCw, AlertCircle, CheckCircle, BarChart3, ArrowUp, ArrowDown } from 'lucide-react'
import { api } from '../lib/api'

const AGENT_ICONS: Record<string, React.ReactNode> = {
  market_research: <Search size={16} />, email_3d: <Mail size={16} />, seo_empire: <Globe size={16} />,
  launch: <Rocket size={16} />, viral_referral: <Share2 size={16} />, interactive: <Activity size={16} />,
  partnership: <Link size={16} />, community: <Users size={16} />, pricing: <Target size={16} />,
  content: <Sparkles size={16} />, trend_jacker: <TrendingUp size={16} />, neuromarketing: <Brain size={16} />,
}

const AGENT_COLORS: Record<string, string> = {
  market_research: 'from-blue-500/20 to-cyan-500/20', email_3d: 'from-indigo-500/20 to-purple-500/20',
  seo_empire: 'from-green-500/20 to-emerald-500/20', launch: 'from-purple-500/20 to-pink-500/20',
  viral_referral: 'from-orange-500/20 to-amber-500/20', interactive: 'from-red-500/20 to-rose-500/20',
  partnership: 'from-indigo-500/20 to-violet-500/20', community: 'from-teal-500/20 to-cyan-500/20',
  pricing: 'from-yellow-500/20 to-orange-500/20', content: 'from-pink-500/20 to-rose-500/20',
  trend_jacker: 'from-cyan-500/20 to-blue-500/20', neuromarketing: 'from-violet-500/20 to-purple-500/20',
}

const MARKETING_CHANNELS = [
  { key: 'email_3d', label: 'Email 3D', icon: Mail, color: 'from-blue-500/20 to-indigo-500/20' },
  { key: 'seo_empire', label: 'SEO Empire', icon: Globe, color: 'from-green-500/20 to-emerald-500/20' },
  { key: 'launch', label: 'Launch', icon: Rocket, color: 'from-purple-500/20 to-pink-500/20' },
  { key: 'viral_referral', label: 'Viral Referral', icon: Share2, color: 'from-orange-500/20 to-amber-500/20' },
  { key: 'interactive', label: 'Interactive', icon: Activity, color: 'from-red-500/20 to-rose-500/20' },
  { key: 'partnership', label: 'Partnership', icon: Link, color: 'from-indigo-500/20 to-violet-500/20' },
  { key: 'community_flywheel', label: 'Community', icon: MessageCircle, color: 'from-teal-500/20 to-cyan-500/20' },
]

interface SystemStatus {
  system: { status: string; uptime_seconds: number; version: string; platform: string; python_version: string }
  database: { status: string; type: string }
  ai: { status: string; provider: string; model: string }
  websocket_connections: number
  total_activities: number
  scheduler_active: boolean
}

interface AgentInfo {
  name: string; label: string; icon: string; description: string
  is_running: boolean; total_runs: number; total_errors: number; last_started_at: string | null
}

interface ActivityLog {
  id: number; agent_name: string; action: string; status: string
  output_preview: string; error_message: string | null; duration_ms: number | null; created_at: string | null
}

export function Dashboard({ user }: { user: any }) {
  const [status, setStatus] = useState<SystemStatus | null>(null)
  const [agents, setAgents] = useState<AgentInfo[]>([])
  const [logs, setLogs] = useState<ActivityLog[]>([])
  const [liveFeed, setLiveFeed] = useState<any[]>([])
  const [wsConnected, setWsConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [marketingResult, setMarketingResult] = useState<any>(null)
  const [marketingLoading, setMarketingLoading] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const feedEndRef = useRef<HTMLDivElement>(null)

  const loadData = useCallback(async () => {
    try {
      const token = localStorage.getItem('token')
      const headers = { Authorization: `Bearer ${token}` }
      const [statusRes, agentsRes, logsRes] = await Promise.all([
        fetch('/api/v1/system/status', { headers }).then(r => r.json()).catch(() => null),
        api.agents.listAll().catch(() => ({ agents: [] })),
        api.agents.getLogs(undefined, 20).catch(() => ({ logs: [] })),
      ])
      setStatus(statusRes)
      setAgents(agentsRes?.agents || [])
      setLogs(logsRes?.logs || [])
    } catch { } finally { setLoading(false) }
  }, [])

  useEffect(() => { loadData() }, [loadData])

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const ws = new WebSocket(`${protocol}//localhost:8000/api/v1/agents/ws`)
    wsRef.current = ws
    ws.onopen = () => setWsConnected(true)
    ws.onclose = () => setWsConnected(false)
    ws.onerror = () => setWsConnected(false)
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLiveFeed(prev => [data, ...prev].slice(0, 50))
        if (data.type === 'activity') {
          setLogs(prev => [{
            id: data.activity_id || Date.now(), agent_name: data.agent_name,
            action: data.action || '', status: data.status || '',
            output_preview: data.preview || '', error_message: null, duration_ms: null, created_at: data.timestamp,
          }, ...prev].slice(0, 100))
        }
      } catch { }
    }
    return () => ws.close()
  }, [])

  useEffect(() => { feedEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [liveFeed])

  const handleAgentAction = async (name: string, action: 'start' | 'stop') => {
    try {
      if (action === 'start') await api.agents.start(name, {})
      else await api.agents.stop(name)
      await loadData()
    } catch { }
  }

  const handleMarketingChannel = async (channel: string) => {
    setMarketingLoading(channel)
    setMarketingResult(null)
    try {
      const token = localStorage.getItem('token')
      const r = await fetch('/api/v1/marketing/channel/' + channel, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ product: { name: 'AI Empire Product', price: 29.99 } }),
      })
      const data = await r.json()
      setMarketingResult({ channel, data: data.result || data })
    } catch { setMarketingResult({ error: 'Failed' }) }
    setMarketingLoading(null)
  }

  const getStatusColor = (s: string) => {
    switch (s) {
      case 'running': return 'text-yellow-400'
      case 'completed': return 'text-green-400'
      case 'failed': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  const formatUptime = (seconds: number) => {
    const d = Math.floor(seconds / 86400); const h = Math.floor((seconds % 86400) / 3600)
    const m = Math.floor((seconds % 3600) / 60); const s = seconds % 60
    return `${d}d ${h}h ${m}m ${s}s`
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <RefreshCw size={32} className="animate-spin text-primary-400" />
    </div>
  )

  const runningCount = agents.filter(a => a.is_running).length
  const activeCount = status?.websocket_connections || 0

  return (
    <div className="space-6">
      {/* System Status Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3 mb-6">
        <div className={`col-span-2 flex items-center gap-3 px-4 py-3 rounded-2xl border ${status?.system.status === 'operational' ? 'bg-green-500/5 border-green-500/20' : 'bg-red-500/5 border-red-500/20'}`}>
          <div className={`w-3 h-3 rounded-full ${status?.system.status === 'operational' ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
          <div>
            <p className="text-xs text-gray-400">حالة النظام</p>
            <p className="text-sm font-bold">{status?.system.status === 'operational' ? 'نشط بالكامل' : 'مشاكل'}</p>
          </div>
        </div>
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <Server size={16} className="text-primary-400 mb-1" />
          <p className="text-xs text-gray-400">وقت التشغيل</p>
          <p className="text-sm font-bold">{status?.system.uptime_seconds ? formatUptime(status.system.uptime_seconds) : '-'}</p>
        </div>
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <Cpu size={16} className="text-cyan-400 mb-1" />
          <p className="text-xs text-gray-400">الوكلاء</p>
          <p className="text-sm font-bold">{runningCount}/{agents.length} <span className="text-xs text-green-400">نشط</span></p>
        </div>
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <Wifi size={16} className="text-purple-400 mb-1" />
          <p className="text-xs text-gray-400">WebSocket</p>
          <p className="text-sm font-bold">{activeCount} <span className="text-xs text-gray-400">متصل</span></p>
        </div>
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <Database size={16} className={`mb-1 ${status?.database.status === 'ok' ? 'text-green-400' : 'text-red-400'}`} />
          <p className="text-xs text-gray-400">قاعدة البيانات</p>
          <p className={`text-sm font-bold ${status?.database.status === 'ok' ? 'text-green-400' : 'text-red-400'}`}>
            {status?.database.status === 'ok' ? 'متصل' : 'منقطع'}
          </p>
        </div>
      </div>

      {/* Main Grid: Agents + Live Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Agents */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-bold flex items-center gap-2"><Brain size={18} className="text-primary-400" /> وكلاء AI</h2>
            <button onClick={loadData} className="p-2 bg-gray-800 rounded-xl hover:bg-gray-700 transition-colors"><RefreshCw size={14} /></button>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {agents.map(agent => (
              <div key={agent.name} className={`bg-gradient-to-br ${AGENT_COLORS[agent.name] || 'from-gray-800/50 to-gray-900/50'} rounded-xl border border-white/5 p-3`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5">
                    <div className="w-6 h-6 rounded-lg bg-white/5 flex items-center justify-center">
                      {AGENT_ICONS[agent.name] || <Brain size={12} />}
                    </div>
                    <div>
                      <p className="text-xs font-bold">{agent.label}</p>
                      <p className="text-[10px] text-gray-500">{agent.description}</p>
                    </div>
                  </div>
                  <div className={`w-1.5 h-1.5 rounded-full ${agent.is_running ? 'bg-green-400 animate-pulse' : 'bg-gray-500'}`} />
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex gap-1">
                    <button onClick={() => handleAgentAction(agent.name, 'start')} disabled={agent.is_running}
                      className="p-1 bg-green-500/20 hover:bg-green-500/30 disabled:opacity-30 rounded-lg transition-all">
                      <Play size={12} className="text-green-400" />
                    </button>
                    <button onClick={() => handleAgentAction(agent.name, 'stop')} disabled={!agent.is_running}
                      className="p-1 bg-red-500/20 hover:bg-red-500/30 disabled:opacity-30 rounded-lg transition-all">
                      <Square size={12} className="text-red-400" />
                    </button>
                  </div>
                  <span className="text-[10px] text-gray-500">{agent.total_runs} تشغيلات</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Live Activity Feed */}
        <div>
          <h2 className="text-lg font-bold mb-3 flex items-center gap-2">
            <Activity size={18} className="text-accent-400" /> النشاط المباشر
            {wsConnected && <span className="text-[10px] text-green-400 animate-pulse">● مباشر</span>}
          </h2>
          <div className="bg-gray-900/50 rounded-2xl border border-gray-800 p-3 h-[400px] overflow-y-auto">
            {liveFeed.length === 0 && <p className="text-xs text-gray-500 text-center py-8">في انتظار النشاط...</p>}
            {liveFeed.map((act, i) => (
              <div key={i} className="flex items-center gap-1.5 px-2 py-1.5 bg-gray-800/20 rounded-lg mb-1 text-[11px]">
                <span className="text-gray-500 w-14 shrink-0">{act.timestamp ? new Date(act.timestamp).toLocaleTimeString() : ''}</span>
                <span className="font-medium text-primary-300 truncate max-w-[80px]">{act.agent_name}</span>
                <span className="text-gray-300 truncate flex-1">{act.action || act.type}</span>
                {act.status && <span className={`${getStatusColor(act.status)} shrink-0`}>{act.status}</span>}
              </div>
            ))}
            <div ref={feedEndRef} />
          </div>
        </div>
      </div>

      {/* Marketing Channels + Recent Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Marketing Channels */}
        <div className="lg:col-span-2">
          <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Zap size={18} className="text-yellow-400" />التسويق المبتكر</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
            {MARKETING_CHANNELS.map(ch => (
              <button key={ch.key} onClick={() => handleMarketingChannel(ch.key)} disabled={!!marketingLoading}
                className={`p-3 rounded-xl bg-gradient-to-br ${ch.color} border border-white/5 hover:border-white/20 transition-all text-center disabled:opacity-50`}>
                <ch.icon size={20} className="mx-auto mb-1 text-gray-300" />
                <p className="text-xs font-medium">{ch.label}</p>
                <p className="text-[10px] text-primary-400 mt-1">{marketingLoading === ch.key ? '...' : 'تشغيل'}</p>
              </button>
            ))}
          </div>
          {marketingResult && !marketingResult.error && (
            <div className="mt-3 bg-gray-900/50 rounded-xl border border-gray-800 p-3 max-h-48 overflow-y-auto">
              <p className="text-xs text-gray-400 mb-1">نتائج {marketingResult.channel}:</p>
              <pre className="text-[10px] text-gray-500">{JSON.stringify(marketingResult.data, null, 1).slice(0, 500)}</pre>
            </div>
          )}
          {marketingResult?.error && <p className="text-xs text-red-400 mt-2">{marketingResult.error}</p>}
        </div>

        {/* Recent Logs */}
        <div>
          <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><BarChart3 size={18} className="text-primary-400" /> آخر السجلات</h2>
          <div className="bg-gray-900/50 rounded-2xl border border-gray-800 p-3 h-[300px] overflow-y-auto">
            {logs.length === 0 && <p className="text-xs text-gray-500 text-center py-8">لا توجد سجلات</p>}
            {logs.slice(0, 15).map(log => (
              <div key={log.id} className="px-2 py-1.5 bg-gray-800/20 rounded-lg mb-1">
                <div className="flex items-center gap-1.5 text-[11px]">
                  {log.status === 'running' ? <Clock size={10} className="animate-spin text-yellow-400" /> :
                   log.status === 'completed' ? <CheckCircle size={10} className="text-green-400" /> :
                   log.status === 'failed' ? <AlertCircle size={10} className="text-red-400" /> :
                   <Clock size={10} className="text-gray-400" />}
                  <span className="font-medium text-primary-300">{log.agent_name}</span>
                  <span className="text-gray-300 truncate flex-1">{log.action}</span>
                  <span className={`text-[10px] ${getStatusColor(log.status)}`}>{log.status}</span>
                </div>
                {log.output_preview && <p className="text-[10px] text-gray-500 mt-0.5 truncate">{log.output_preview}</p>}
                {log.error_message && <p className="text-[10px] text-red-400 mt-0.5">{log.error_message}</p>}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* System Details */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <p className="text-xs text-gray-400">الإصدار</p>
          <p className="text-sm font-bold">{status?.system.version || '-'}</p>
        </div>
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <p className="text-xs text-gray-400">AI Provider</p>
          <p className="text-sm font-bold">{status?.ai.provider || '-'} <span className="text-xs text-gray-400">{status?.ai.model || ''}</span></p>
        </div>
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <p className="text-xs text-gray-400">المنصة</p>
          <p className="text-sm font-bold">{status?.system.platform || '-'}</p>
        </div>
        <div className="px-4 py-3 rounded-2xl bg-gray-900/50 border border-gray-800">
          <p className="text-xs text-gray-400">إجمالي الأنشطة</p>
          <p className="text-sm font-bold">{status?.total_activities || 0}</p>
        </div>
      </div>
    </div>
  )
}