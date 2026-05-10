import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Brain, Play, Square, RefreshCw, AlertCircle, CheckCircle, Clock, Activity, Zap, Mail, Globe, Rocket, Share2, Target, Link, Users, Search, TrendingUp, MessageCircle, DollarSign, Sparkles } from 'lucide-react'
import { api } from '../lib/api'

const AGENT_ICONS: Record<string, React.ReactNode> = {
  market_research: <Search size={18} />,
  email_3d: <Mail size={18} />,
  seo_empire: <Globe size={18} />,
  launch: <Rocket size={18} />,
  viral_referral: <Share2 size={18} />,
  interactive: <Activity size={18} />,
  partnership: <Link size={18} />,
  community: <Users size={18} />,
  pricing: <DollarSign size={18} />,
  content: <Sparkles size={18} />,
  trend_jacker: <TrendingUp size={18} />,
  neuromarketing: <Brain size={18} />,
}

const AGENT_COLORS: Record<string, string> = {
  market_research: 'from-blue-500/20 to-cyan-500/20',
  email_3d: 'from-indigo-500/20 to-purple-500/20',
  seo_empire: 'from-green-500/20 to-emerald-500/20',
  launch: 'from-purple-500/20 to-pink-500/20',
  viral_referral: 'from-orange-500/20 to-amber-500/20',
  interactive: 'from-red-500/20 to-rose-500/20',
  partnership: 'from-indigo-500/20 to-violet-500/20',
  community: 'from-teal-500/20 to-cyan-500/20',
  pricing: 'from-yellow-500/20 to-orange-500/20',
  content: 'from-pink-500/20 to-rose-500/20',
  trend_jacker: 'from-cyan-500/20 to-blue-500/20',
  neuromarketing: 'from-violet-500/20 to-purple-500/20',
}

interface AgentInfo {
  name: string
  label: string
  icon: string
  description: string
  is_running: boolean
  total_runs: number
  total_errors: number
  last_started_at: string | null
}

interface ActivityLog {
  id: number
  agent_name: string
  action: string
  status: string
  input_data: any
  output_preview: string
  error_message: string | null
  duration_ms: number | null
  created_at: string | null
}

interface LiveActivity {
  type: string
  agent_name: string
  action?: string
  status?: string
  timestamp: string
  preview?: string
  activity_id?: number
}

export function AgentConsole() {
  const [agents, setAgents] = useState<AgentInfo[]>([])
  const [logs, setLogs] = useState<ActivityLog[]>([])
  const [liveFeed, setLiveFeed] = useState<LiveActivity[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const [wsConnected, setWsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const feedEndRef = useRef<HTMLDivElement>(null)

  // Load agents and logs
  const loadData = useCallback(async () => {
    try {
      const [agentsRes, logsRes] = await Promise.all([
        api.agents.listAll(),
        api.agents.getLogs(selectedAgent || undefined),
      ])
      setAgents(agentsRes?.agents || [])
      setLogs(logsRes?.logs || [])
    } catch (e) {
      console.error('Failed to load agent data')
    } finally {
      setLoading(false)
    }
  }, [selectedAgent])

  useEffect(() => { loadData() }, [loadData])

  // WebSocket connection for live feed
  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const ws = new WebSocket(`${protocol}//${window.location.host}/api/v1/agents/ws`)
    wsRef.current = ws

    ws.onopen = () => setWsConnected(true)
    ws.onclose = () => setWsConnected(false)
    ws.onerror = () => setWsConnected(false)
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLiveFeed(prev => [data, ...prev].slice(0, 100))
        // Refresh logs when new activity
        if (data.type === 'activity') {
          setLogs(prev => {
            const newLog: ActivityLog = {
              id: data.activity_id || Date.now(),
              agent_name: data.agent_name,
              action: data.action || '',
              status: data.status || '',
              input_data: null,
              output_preview: data.preview || '',
              error_message: null,
              duration_ms: null,
              created_at: data.timestamp,
            }
            return [newLog, ...prev].slice(0, 100)
          })
        }
      } catch { }
    }

    return () => ws.close()
  }, [])

  useEffect(() => {
    feedEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [liveFeed])

  const startAgent = async (name: string) => {
    try {
      await api.agents.start(name, {})
      await loadData()
    } catch (e) { console.error(e) }
  }

  const stopAgent = async (name: string) => {
    try {
      await api.agents.stop(name)
      await loadData()
    } catch (e) { console.error(e) }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-yellow-400'
      case 'completed': return 'text-green-400'
      case 'failed': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Clock size={14} className="animate-spin text-yellow-400" />
      case 'completed': return <CheckCircle size={14} className="text-green-400" />
      case 'failed': return <AlertCircle size={14} className="text-red-400" />
      default: return <Clock size={14} className="text-gray-400" />
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw size={32} className="animate-spin text-primary-400" />
      </div>
    )
  }

  return (
    <div className="space-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Command Center</h1>
          <p className="text-gray-400 mt-1">التحكم الكامل بجميع الوكلاء — راقب، تحكم، وشغّل</p>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
          <span className="text-xs text-gray-400">{wsConnected ? 'متصل' : 'غير متصل'}</span>
          <button onClick={loadData} className="p-2 bg-gray-800 rounded-xl hover:bg-gray-700 transition-colors">
            <RefreshCw size={16} />
          </button>
        </div>
      </div>

      {/* Live Activity Feed */}
      <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6 mb-6">
        <h2 className="text-lg font-bold mb-3 flex items-center gap-2">
          <Activity size={18} className="text-accent-400" />
          النشاط المباشر
          {wsConnected && <span className="text-xs text-green-400 animate-pulse">● مباشر</span>}
        </h2>
        <div className="max-h-48 overflow-y-auto space-y-1">
          {liveFeed.length === 0 && (
            <p className="text-sm text-gray-500 text-center py-4">في انتظار النشاط...</p>
          )}
          {liveFeed.map((act, i) => (
            <div key={i} className="flex items-center gap-2 px-3 py-1.5 bg-gray-800/20 rounded-lg text-xs">
              <span className="text-gray-500">{new Date(act.timestamp).toLocaleTimeString()}</span>
              <span className="font-medium text-primary-300">{act.agent_name}</span>
              <span className="text-gray-300">{act.action || act.type}</span>
              {act.status && (
                <span className={`${getStatusColor(act.status)}`}>{act.status}</span>
              )}
              {act.preview && <span className="text-gray-500 truncate max-w-[200px]">— {act.preview}</span>}
            </div>
          ))}
          <div ref={feedEndRef} />
        </div>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-6">
        {agents.map(agent => (
          <div
            key={agent.name}
            className={`bg-gradient-to-br ${AGENT_COLORS[agent.name] || 'from-gray-800/50 to-gray-900/50'} backdrop-blur-xl rounded-2xl border border-white/5 p-5 hover:border-white/20 transition-all`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                  {AGENT_ICONS[agent.name] || <Brain size={16} />}
                </div>
                <div>
                  <p className="text-sm font-bold">{agent.label}</p>
                  <p className="text-xs text-gray-400">{agent.description}</p>
                </div>
              </div>
              <div className={`w-2 h-2 rounded-full ${agent.is_running ? 'bg-green-400 animate-pulse' : 'bg-gray-500'}`} />
            </div>

            <div className="flex items-center gap-3 text-xs text-gray-400 mb-3">
              <span>🏃 {agent.total_runs}</span>
              <span>❌ {agent.total_errors}</span>
              {agent.last_started_at && <span>🕐 {new Date(agent.last_started_at).toLocaleTimeString()}</span>}
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => startAgent(agent.name)}
                disabled={agent.is_running}
                className="flex-1 px-3 py-2 bg-green-500/20 hover:bg-green-500/30 disabled:opacity-30 rounded-xl text-xs font-medium text-green-400 transition-all flex items-center justify-center gap-1"
              >
                <Play size={14} /> تشغيل
              </button>
              <button
                onClick={() => stopAgent(agent.name)}
                disabled={!agent.is_running}
                className="flex-1 px-3 py-2 bg-red-500/20 hover:bg-red-500/30 disabled:opacity-30 rounded-xl text-xs font-medium text-red-400 transition-all flex items-center justify-center gap-1"
              >
                <Square size={14} /> إيقاف
              </button>
              <button
                onClick={() => setSelectedAgent(selectedAgent === agent.name ? null : agent.name)}
                className={`px-3 py-2 rounded-xl text-xs font-medium transition-all ${selectedAgent === agent.name ? 'bg-primary-500/30 text-primary-300' : 'bg-gray-800/50 text-gray-400 hover:bg-gray-700'}`}
              >
                {selectedAgent === agent.name ? 'إخفاء' : 'سجلات'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Detailed Logs */}
      <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6">
        <h2 className="text-lg font-bold mb-3 flex items-center gap-2">
          <Activity size={18} className="text-primary-400" />
          سجلات النشاط {selectedAgent && `— ${agents.find(a => a.name === selectedAgent)?.label}`}
        </h2>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {logs.length === 0 && (
            <p className="text-sm text-gray-500 text-center py-8">لا توجد سجلات بعد. شغّل وكيلاً للبدء.</p>
          )}
          {logs.map(log => (
            <div key={log.id} className="px-4 py-3 bg-gray-800/30 rounded-xl text-sm">
              <div className="flex items-center gap-2 mb-1">
                {getStatusIcon(log.status)}
                <span className="font-medium text-primary-300">{log.agent_name}</span>
                <span className="text-gray-300">{log.action}</span>
                <span className={`text-xs ${getStatusColor(log.status)}`}>{log.status}</span>
                {log.duration_ms && <span className="text-xs text-gray-500">{log.duration_ms.toFixed(0)}ms</span>}
                {log.created_at && <span className="text-xs text-gray-500 mr-auto">{new Date(log.created_at).toLocaleString()}</span>}
              </div>
              {log.output_preview && (
                <p className="text-xs text-gray-400 mt-1 truncate">{log.output_preview}</p>
              )}
              {log.error_message && (
                <p className="text-xs text-red-400 mt-1">{log.error_message}</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
