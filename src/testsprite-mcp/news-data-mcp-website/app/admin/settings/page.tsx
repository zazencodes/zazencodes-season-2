'use client'

import { useState } from 'react'
import { Save, AlertTriangle, Server, Database, Key } from 'lucide-react'

export default function AdminSettings() {
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  const handleSystemMaintenance = async () => {
    setSaving(true)
    try {
      // In a real app, this would trigger maintenance mode
      setTimeout(() => {
        setMessage({ type: 'success', text: 'System maintenance mode toggled' })
        setSaving(false)
      }, 2000)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to toggle maintenance mode' })
      setSaving(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Admin Settings</h2>
        <p className="text-gray-600 dark:text-gray-400">System configuration and maintenance</p>
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${
          message.type === 'success' 
            ? 'bg-green-50 dark:bg-green-900 text-green-700 dark:text-green-200 border border-green-200 dark:border-green-700'
            : 'bg-red-50 dark:bg-red-900 text-red-700 dark:text-red-200 border border-red-200 dark:border-red-700'
        }`}>
          {message.text}
        </div>
      )}

      {/* System Status */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex items-center mb-6">
          <Server className="h-6 w-6 text-blue-600 dark:text-blue-400 mr-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">System Status</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-4 bg-green-50 dark:bg-green-900 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span className="text-green-800 dark:text-green-200 font-medium">API Service</span>
            </div>
            <p className="text-green-700 dark:text-green-300 text-sm mt-1">Operational</p>
          </div>

          <div className="p-4 bg-green-50 dark:bg-green-900 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span className="text-green-800 dark:text-green-200 font-medium">Database</span>
            </div>
            <p className="text-green-700 dark:text-green-300 text-sm mt-1">Connected</p>
          </div>

          <div className="p-4 bg-green-50 dark:bg-green-900 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span className="text-green-800 dark:text-green-200 font-medium">Authentication</span>
            </div>
            <p className="text-green-700 dark:text-green-300 text-sm mt-1">Active</p>
          </div>
        </div>
      </div>

      {/* Database Stats */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex items-center mb-6">
          <Database className="h-6 w-6 text-purple-600 dark:text-purple-400 mr-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Database Information</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-3">Connection Details</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Provider:</span>
                <span className="font-mono text-gray-900 dark:text-white">SQLite</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">File:</span>
                <span className="font-mono text-gray-900 dark:text-white">./dev.db</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Status:</span>
                <span className="text-green-600 dark:text-green-400">Connected</span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-3">Schema Info</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Tables:</span>
                <span className="text-gray-900 dark:text-white">6</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Models:</span>
                <span className="text-gray-900 dark:text-white">User, ApiKey, UsageRecord</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Last Migration:</span>
                <span className="text-gray-900 dark:text-white">Recent</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Security Settings */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex items-center mb-6">
          <Key className="h-6 w-6 text-yellow-600 dark:text-yellow-400 mr-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Security Configuration</h3>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white">NextAuth.js</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">Authentication provider status</p>
            </div>
            <span className="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-3 py-1 rounded-full text-sm">
              Active
            </span>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white">Password Hashing</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">bcrypt encryption enabled</p>
            </div>
            <span className="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-3 py-1 rounded-full text-sm">
              Enabled
            </span>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white">CORS Protection</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">Cross-origin request security</p>
            </div>
            <span className="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-3 py-1 rounded-full text-sm">
              Active
            </span>
          </div>
        </div>
      </div>

      {/* Maintenance Actions */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border-l-4 border-yellow-500">
        <div className="flex items-center mb-6">
          <AlertTriangle className="h-6 w-6 text-yellow-600 dark:text-yellow-400 mr-3" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">System Maintenance</h3>
        </div>

        <div className="space-y-4">
          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">Maintenance Mode</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Enable maintenance mode to prevent user access during system updates.
            </p>
            <button
              onClick={handleSystemMaintenance}
              disabled={saving}
              className="flex items-center px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              ) : (
                <AlertTriangle className="h-4 w-4 mr-2" />
              )}
              Toggle Maintenance Mode
            </button>
          </div>

          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">Environment</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600 dark:text-gray-400">Environment:</span>
                <span className="ml-2 font-mono text-gray-900 dark:text-white">Development</span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Node Version:</span>
                <span className="ml-2 font-mono text-gray-900 dark:text-white">20.x</span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Next.js Version:</span>
                <span className="ml-2 font-mono text-gray-900 dark:text-white">14.0.4</span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Uptime:</span>
                <span className="ml-2 font-mono text-gray-900 dark:text-white">2h 15m</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 