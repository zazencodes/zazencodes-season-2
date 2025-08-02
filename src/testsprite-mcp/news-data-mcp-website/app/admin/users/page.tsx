'use client'

import { useState, useEffect } from 'react'
import { Search, Edit, Trash2, Plus, Eye, EyeOff, Save, X } from 'lucide-react'

interface User {
  id: string
  name: string
  email: string
  role: string
  plan: string
  tokenLimit: number
  tokensUsed: number
  createdAt: string
  updatedAt: string
  _count: {
    apiKeys: number
    usageRecords: number
  }
}

interface EditUser {
  name: string
  email: string
  role: string
  plan: string
  tokenLimit: number
}

export default function UserManagement() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [editingUser, setEditingUser] = useState<string | null>(null)
  const [editForm, setEditForm] = useState<EditUser>({
    name: '',
    email: '',
    role: 'USER',
    plan: 'FREE',
    tokenLimit: 1000
  })
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/admin/users')
      if (response.ok) {
        const data = await response.json()
        setUsers(data)
      }
    } catch (error) {
      console.error('Failed to fetch users:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEditUser = (user: User) => {
    setEditingUser(user.id)
    setEditForm({
      name: user.name,
      email: user.email,
      role: user.role,
      plan: user.plan,
      tokenLimit: user.tokenLimit
    })
  }

  const handleSaveUser = async () => {
    if (!editingUser) return
    
    setSaving(true)
    try {
      const response = await fetch(`/api/admin/users/${editingUser}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editForm),
      })

      if (response.ok) {
        setMessage({ type: 'success', text: 'User updated successfully' })
        setEditingUser(null)
        fetchUsers()
      } else {
        const data = await response.json()
        setMessage({ type: 'error', text: data.message || 'Failed to update user' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Something went wrong. Please try again.' })
    } finally {
      setSaving(false)
    }
  }

  const handleDeleteUser = async (userId: string) => {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      return
    }

    try {
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        setMessage({ type: 'success', text: 'User deleted successfully' })
        fetchUsers()
      } else {
        const data = await response.json()
        setMessage({ type: 'error', text: data.message || 'Failed to delete user' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Something went wrong. Please try again.' })
    }
  }

  const handleResetTokens = async (userId: string) => {
    try {
      const response = await fetch(`/api/admin/users/${userId}/reset-tokens`, {
        method: 'POST',
      })

      if (response.ok) {
        setMessage({ type: 'success', text: 'User tokens reset successfully' })
        fetchUsers()
      } else {
        const data = await response.json()
        setMessage({ type: 'error', text: data.message || 'Failed to reset tokens' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Something went wrong. Please try again.' })
    }
  }

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.plan.toLowerCase().includes(searchQuery.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">User Management</h2>
          <p className="text-gray-600 dark:text-gray-400">Manage user accounts, plans, and permissions</p>
        </div>
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

      {/* Search */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          placeholder="Search users..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {/* Users Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Role & Plan
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Token Usage
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Activity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {filteredUsers.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap">
                    {editingUser === user.id ? (
                      <div className="space-y-2">
                        <input
                          type="text"
                          value={editForm.name}
                          onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                          className="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                          placeholder="Name"
                        />
                        <input
                          type="email"
                          value={editForm.email}
                          onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                          className="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                          placeholder="Email"
                        />
                      </div>
                    ) : (
                      <div>
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{user.name}</div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">{user.email}</div>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {editingUser === user.id ? (
                      <div className="space-y-2">
                        <select
                          value={editForm.role}
                          onChange={(e) => setEditForm({ ...editForm, role: e.target.value })}
                          className="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <option value="USER">User</option>
                          <option value="ADMIN">Admin</option>
                        </select>
                        <select
                          value={editForm.plan}
                          onChange={(e) => setEditForm({ ...editForm, plan: e.target.value })}
                          className="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <option value="FREE">Free</option>
                          <option value="MONTHLY">Monthly</option>
                          <option value="YEARLY">Yearly</option>
                        </select>
                      </div>
                    ) : (
                      <div>
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          user.role === 'ADMIN' 
                            ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                            : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                        }`}>
                          {user.role}
                        </span>
                        <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">{user.plan}</div>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {editingUser === user.id ? (
                      <input
                        type="number"
                        value={editForm.tokenLimit}
                        onChange={(e) => setEditForm({ ...editForm, tokenLimit: parseInt(e.target.value) || 0 })}
                        className="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        placeholder="Token Limit"
                      />
                    ) : (
                      <div>
                        <div className="text-sm text-gray-900 dark:text-white">
                          {user.tokensUsed.toLocaleString()} / {user.tokenLimit.toLocaleString()}
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-1">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${Math.min((user.tokensUsed / user.tokenLimit) * 100, 100)}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    <div>{user._count.apiKeys} API keys</div>
                    <div>{user._count.usageRecords} requests</div>
                    <div>Created {new Date(user.createdAt).toLocaleDateString()}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    {editingUser === user.id ? (
                      <div className="flex space-x-2">
                        <button
                          onClick={handleSaveUser}
                          disabled={saving}
                          className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                        >
                          <Save className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => setEditingUser(null)}
                          className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300"
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </div>
                    ) : (
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleEditUser(user)}
                          className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleResetTokens(user.id)}
                          className="text-yellow-600 hover:text-yellow-900 dark:text-yellow-400 dark:hover:text-yellow-300"
                        >
                          Reset
                        </button>
                        <button
                          onClick={() => handleDeleteUser(user.id)}
                          className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredUsers.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">No users found matching your search.</p>
          </div>
        )}
      </div>

      {/* Summary */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-gray-500 dark:text-gray-400">Total Users:</span>
            <span className="ml-2 font-semibold text-gray-900 dark:text-white">{users.length}</span>
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Admin Users:</span>
            <span className="ml-2 font-semibold text-gray-900 dark:text-white">
              {users.filter(u => u.role === 'ADMIN').length}
            </span>
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Paid Users:</span>
            <span className="ml-2 font-semibold text-gray-900 dark:text-white">
              {users.filter(u => u.plan !== 'FREE').length}
            </span>
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Active Users:</span>
            <span className="ml-2 font-semibold text-gray-900 dark:text-white">
              {users.filter(u => u._count.usageRecords > 0).length}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
} 