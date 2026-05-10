const API_BASE = '/api/v1'

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem('token')
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options?.headers as Record<string, string>,
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(error.detail || `HTTP ${res.status}`)
  }

  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  auth: {
    login: (email: string, password: string) =>
      request<{ access_token: string; user: any }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),
    register: (data: { email: string; username: string; password: string; full_name?: string }) =>
      request<{ access_token: string; user: any }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    me: () => request<any>('/auth/me'),
  },

  products: {
    list: (page = 1) => request<any>(`/products?page=${page}`),
    get: (id: string) => request<any>(`/products/${id}`),
    create: (data: any) =>
      request<any>('/products', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    update: (id: string, data: any) =>
      request<any>(`/products/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/products/${id}`, { method: 'DELETE' }),
  },

  marketing: {
    campaigns: () => request<any[]>('/marketing/campaigns'),
    createCampaign: (data: any) =>
      request<any>('/marketing/campaigns', { method: 'POST', body: JSON.stringify(data) }),
    launchCampaign: (id: string) =>
      request<any>(`/marketing/campaigns/${id}/launch`, { method: 'POST' }),
    masterPlan: (data: any) =>
      request<any>('/marketing/master-plan', { method: 'POST', body: JSON.stringify(data) }),
    emailCampaign: (data: any) =>
      request<any>('/marketing/email-campaign', { method: 'POST', body: JSON.stringify(data) }),
    seoStrategy: (data: any) =>
      request<any>('/marketing/seo-strategy', { method: 'POST', body: JSON.stringify(data) }),
    launchPlan: (data: any) =>
      request<any>('/marketing/launch-plan', { method: 'POST', body: JSON.stringify(data) }),
    referralProgram: (data: any) =>
      request<any>('/marketing/referral-program', { method: 'POST', body: JSON.stringify(data) }),
    interactiveContent: (data: any) =>
      request<any>('/marketing/interactive-content', { method: 'POST', body: JSON.stringify(data) }),
    partnerships: (data: any) =>
      request<any>('/marketing/partnerships', { method: 'POST', body: JSON.stringify(data) }),
    community: (data: any) =>
      request<any>('/marketing/community', { method: 'POST', body: JSON.stringify(data) }),
    executeChannel: (channel: string, data: any) =>
      request<any>(`/marketing/channel/${channel}`, { method: 'POST', body: JSON.stringify(data) }),
  },

  agents: {
    research: (data: any) =>
      request<any>('/agents/research', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    generateStrategy: (productId: string) =>
      request<any>(`/agents/generate-strategy?product_id=${productId}`, {
        method: 'POST',
      }),
    executeCampaign: (campaignId: string) =>
      request<any>(`/agents/execute-campaign/${campaignId}`, {
        method: 'POST',
      }),
    viralContent: (productId: string, platform = 'twitter') =>
      request<any>(`/agents/viral-content?product_id=${productId}&platform=${platform}`, {
        method: 'POST',
      }),
    launchPlan: (productId: string) =>
      request<any>(`/agents/launch-plan?product_id=${productId}`, {
        method: 'POST',
      }),
    listAll: () => request<any>('/agents/list'),
    getLogs: (agentName?: string, limit = 50) =>
      request<any>(`/agents/logs${agentName ? `?agent_name=${agentName}` : `?limit=${limit}`}`),
    start: (agentName: string, data: any) =>
      request<any>(`/agents/${agentName}/start`, { method: 'POST', body: JSON.stringify(data) }),
    stop: (agentName: string) =>
      request<any>(`/agents/${agentName}/stop`, { method: 'POST' }),
  },

  gumroad: {
    verify: () => request<any>('/gumroad/verify'),
    products: () => request<any>('/gumroad/products'),
    sales: (productId?: string) =>
      request<any[]>(`/gumroad/sales${productId ? `?product_id=${productId}` : ''}`),
    sync: () =>
      request<any>('/gumroad/sync', { method: 'POST' }),
    publish: (productId: string) =>
      request<any>(`/gumroad/publish/${productId}`, { method: 'POST' }),
  },
}
