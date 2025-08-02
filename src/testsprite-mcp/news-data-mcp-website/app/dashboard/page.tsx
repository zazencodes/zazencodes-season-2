'use client'

import { useSession, signOut } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Key, Copy, BarChart3, Settings, LogOut, Plus, Eye, EyeOff } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface ApiKey {
  id: string
  key: string
  name: string
  isActive: boolean
  createdAt: string
  lastUsed: string | null
}

interface UserData {
  id: string
  name: string
  email: string
  plan: string
  tokenLimit: number
  tokensUsed: number
  apiKeys: ApiKey[]
}

export default function Dashboard() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [userData, setUserData] = useState<UserData | null>(null)
  const [loading, setLoading] = useState(true)
  const [showApiKeys, setShowApiKeys] = useState<{[key: string]: boolean}>({})
  const [copySuccess, setCopySuccess] = useState<string | null>(null)

  // Mock usage data for the chart
  const usageData = [
    { name: 'Week 1', tokens: 120 },
    { name: 'Week 2', tokens: 250 },
    { name: 'Week 3', tokens: 400 },
    { name: 'Week 4', tokens: 380 },
  ]

  useEffect(() => {
    if (status === 'loading') return
    if (status === 'unauthenticated') {
      router.push('/auth/signin')
      return
    }

    fetchUserData()
  }, [status, router])

  const fetchUserData = async () => {
    try {
      const response = await fetch('/api/user/profile')
      if (response.ok) {
        const data = await response.json()
        setUserData(data)
      }
    } catch (error) {
      console.error('Failed to fetch user data:', error)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = async (text: string, keyId: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopySuccess(keyId)
      setTimeout(() => setCopySuccess(null), 2000)
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
    }
  }

  const toggleApiKeyVisibility = (keyId: string) => {
    setShowApiKeys(prev => ({
      ...prev,
      [keyId]: !prev[keyId]
    }))
  }

  const generateNewApiKey = async () => {
    try {
      const response = await fetch('/api/user/api-keys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: `API Key ${new Date().toLocaleDateString()}` }),
      })

      if (response.ok) {
        fetchUserData() // Refresh data
      }
    } catch (error) {
      console.error('Failed to generate API key:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (!userData) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-400">Failed to load user data</p>
          <button 
            onClick={fetchUserData}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  const usagePercentage = (userData.tokensUsed / userData.tokenLimit) * 100

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
              <p className="text-gray-600 dark:text-gray-400">Welcome back, {userData.name}</p>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/explorer')}
                className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white"
              >
                Route Explorer
              </button>
              <button
                onClick={() => router.push('/settings')}
                className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
              >
                <Settings className="h-5 w-5" />
              </button>
              <button
                onClick={() => signOut()}
                className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Welcome Banner */}
        <div className="mb-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
          <h2 className="text-2xl font-bold mb-2">Current Plan: {userData.plan}</h2>
          <p className="mb-4">You're using {userData.tokensUsed} of {userData.tokenLimit} monthly tokens</p>
          <div className="w-full bg-blue-300 rounded-full h-2">
            <div 
              className="bg-white h-2 rounded-full transition-all duration-300" 
              style={{ width: `${Math.min(usagePercentage, 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* API Keys Section */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <Key className="h-5 w-5 mr-2" />
                API Keys
              </h3>
              <button
                onClick={generateNewApiKey}
                className="flex items-center px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
              >
                <Plus className="h-4 w-4 mr-1" />
                New Key
              </button>
            </div>

            <div className="space-y-3">
              {userData.apiKeys.map((apiKey) => (
                <div key={apiKey.id} className="border dark:border-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-900 dark:text-white">{apiKey.name}</span>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => toggleApiKeyVisibility(apiKey.id)}
                        className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        {showApiKeys[apiKey.id] ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                      <button
                        onClick={() => copyToClipboard(apiKey.key, apiKey.id)}
                        className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        <Copy className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  <div className="font-mono text-sm bg-gray-100 dark:bg-gray-700 p-2 rounded">
                    {showApiKeys[apiKey.id] ? apiKey.key : '••••••••••••••••••••••••••••••••'}
                  </div>
                  {copySuccess === apiKey.id && (
                    <p className="text-green-600 text-sm mt-1">Copied to clipboard!</p>
                  )}
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    Created: {new Date(apiKey.createdAt).toLocaleDateString()}
                    {apiKey.lastUsed && ` • Last used: ${new Date(apiKey.lastUsed).toLocaleDateString()}`}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Usage Chart */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center mb-6">
              <BarChart3 className="h-5 w-5 mr-2" />
              Token Usage (Last 4 Weeks)
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={usageData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: 'none', 
                      borderRadius: '8px',
                      color: '#F9FAFB'
                    }} 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="tokens" 
                    stroke="#3B82F6" 
                    strokeWidth={2}
                    dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <button
            onClick={() => router.push('/explorer')}
            className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left"
          >
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Explore MCP Routes</h4>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Browse available news data endpoints and test your API keys
            </p>
          </button>

          <button
            onClick={() => router.push('/settings')}
            className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left"
          >
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Account Settings</h4>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Manage your account, billing, and preferences
            </p>
          </button>

          <button
            onClick={() => window.open('/docs', '_blank')}
            className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left"
          >
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Documentation</h4>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Learn how to integrate News Data MCP with your applications
            </p>
          </button>
        </div>
      </main>
    </div>
  )
} 