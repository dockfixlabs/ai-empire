export interface User {
  id: string
  email: string
  username: string
  full_name: string | null
  avatar_url: string | null
  is_active: boolean
  subscription_tier: string
  total_revenue: number
  total_products: number
  total_sales: number
  created_at: string
}

export interface Product {
  id: string
  title: string
  description: string | null
  short_description: string | null
  price: number
  original_price: number | null
  currency: string
  category: string | null
  tags: string | null
  content_type: string
  cover_image_url: string | null
  sales_count: number
  revenue: number
  rating: number | null
  is_published: boolean
  status: string
  gumroad_product_id: string | null
  ai_generated: boolean
  created_at: string
  updated_at: string
}

export interface Campaign {
  id: string
  name: string
  campaign_type: string
  status: string
  total_spent: number
  total_revenue: number
  total_clicks: number
  total_conversions: number
  total_impressions: number
  conversion_rate: number
  viral_score: number
  engagement_score: number
  is_automated: boolean
  start_date: string | null
  end_date: string | null
  created_at: string
}

export interface Agent {
  id: string
  name: string
  type: string
  status: 'idle' | 'running' | 'completed' | 'error'
  description: string
  icon: string
  lastRun?: string
  tasksCompleted?: number
}

export interface MarketOpportunity {
  product_idea: string
  description: string
  target_audience: string
  estimated_demand: string
  competition_level: string
  suggested_price: number
  recommended_format: string
  keywords: string[]
  confidence_score: number
}

export interface DashboardStats {
  total_revenue: number
  total_sales: number
  total_products: number
  active_campaigns: number
  conversion_rate: number
  viral_score: number
  revenue_today: number
  revenue_growth: number
}
