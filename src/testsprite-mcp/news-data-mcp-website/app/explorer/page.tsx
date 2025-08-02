'use client'

import { useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Search, ArrowLeft, Play, Copy, Check } from 'lucide-react'

interface MCPTool {
  name: string
  description: string
  parameters: Array<{
    name: string
    type: string
    required: boolean
    description: string
  }>
  example: {
    request: any
    response: any
  }
}

const mcpTools: MCPTool[] = [
  {
    name: 'search_articles',
    description: 'Search for news articles based on a query string with optional filters',
    parameters: [
      { name: 'query', type: 'string', required: true, description: 'Search query for news articles' },
      { name: 'date_range', type: 'string', required: false, description: 'Date range filter (e.g., "last_week", "last_month")' },
      { name: 'limit', type: 'number', required: false, description: 'Maximum number of articles to return (default: 10)' }
    ],
    example: {
      request: {
        query: 'artificial intelligence',
        date_range: 'last_week',
        limit: 5
      },
      response: {
        articles: [
          {
            id: 'art_123',
            title: 'Breakthrough in AI Research',
            summary: 'Scientists announce major breakthrough in artificial intelligence...',
            date: '2024-01-15',
            source: 'Tech News',
            relevance_score: 0.95
          }
        ],
        total_results: 1,
        tokens_used: 25
      }
    }
  },
  {
    name: 'get_article',
    description: 'Retrieve full article content and metadata by article ID',
    parameters: [
      { name: 'article_id', type: 'string', required: true, description: 'Unique identifier for the article' }
    ],
    example: {
      request: {
        article_id: 'art_123'
      },
      response: {
        article: {
          id: 'art_123',
          title: 'Breakthrough in AI Research',
          content: 'Full article content here...',
          metadata: {
            author: 'Jane Smith',
            published_date: '2024-01-15T10:30:00Z',
            word_count: 850,
            facts: ['AI models now achieve 95% accuracy', 'Research funded by major tech companies'],
            entities: ['OpenAI', 'Stanford University', 'Machine Learning']
          },
          source: {
            name: 'Tech News',
            url: 'https://technews.com/article/123',
            credibility_score: 0.92
          }
        },
        tokens_used: 45
      }
    }
  },
  {
    name: 'get_facts_about',
    description: 'Get verified facts about a specific entity, person, organization, or topic',
    parameters: [
      { name: 'entity', type: 'string', required: true, description: 'Entity, person, organization, or topic to get facts about' },
      { name: 'fact_type', type: 'string', required: false, description: 'Type of facts to retrieve (e.g., "recent", "biographical", "financial")' }
    ],
    example: {
      request: {
        entity: 'OpenAI',
        fact_type: 'recent'
      },
      response: {
        entity: 'OpenAI',
        facts: [
          {
            fact: 'Released GPT-4 in March 2023',
            confidence: 0.98,
            sources: ['OpenAI Blog', 'TechCrunch'],
            verified_date: '2024-01-15'
          },
          {
            fact: 'Valued at $29 billion as of 2023',
            confidence: 0.92,
            sources: ['Forbes', 'Reuters'],
            verified_date: '2024-01-10'
          }
        ],
        tokens_used: 30
      }
    }
  },
  {
    name: 'get_latest_news',
    description: 'Get the most recent news articles, optionally filtered by topic',
    parameters: [
      { name: 'topic', type: 'string', required: false, description: 'Topic to filter news by (e.g., "technology", "politics", "business")' },
      { name: 'count', type: 'number', required: false, description: 'Number of articles to return (default: 10, max: 50)' }
    ],
    example: {
      request: {
        topic: 'technology',
        count: 3
      },
      response: {
        articles: [
          {
            id: 'art_456',
            title: 'New Smartphone Released',
            summary: 'Latest flagship phone features advanced AI capabilities...',
            date: '2024-01-16T08:00:00Z',
            source: 'Mobile Tech',
            topic: 'technology'
          }
        ],
        count: 3,
        tokens_used: 20
      }
    }
  }
]

export default function Explorer() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [selectedTool, setSelectedTool] = useState<MCPTool | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [copySuccess, setCopySuccess] = useState<string | null>(null)

  if (status === 'loading') {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (status === 'unauthenticated') {
    router.push('/auth/signin')
    return null
  }

  const filteredTools = mcpTools.filter(tool =>
    tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    tool.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const copyToClipboard = async (text: string, key: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopySuccess(key)
      setTimeout(() => setCopySuccess(null), 2000)
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Link href="/dashboard" className="mr-4 p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">
                <ArrowLeft className="h-5 w-5" />
              </Link>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">MCP Route Explorer</h1>
                <p className="text-gray-600 dark:text-gray-400">Browse and test available news data endpoints</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Search */}
        <div className="mb-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search MCP tools..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Tools List */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Available Tools</h2>
            {filteredTools.map((tool) => (
              <div
                key={tool.name}
                className={`bg-white dark:bg-gray-800 rounded-lg shadow p-6 cursor-pointer transition-colors ${
                  selectedTool?.name === tool.name
                    ? 'ring-2 ring-blue-500 border-blue-500'
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                }`}
                onClick={() => setSelectedTool(tool)}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white font-mono">
                    {tool.name}
                  </h3>
                  {selectedTool?.name === tool.name && (
                    <Play className="h-5 w-5 text-blue-500" />
                  )}
                </div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  {tool.description}
                </p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {tool.parameters.map((param) => (
                    <span
                      key={param.name}
                      className={`px-2 py-1 text-xs rounded-full ${
                        param.required
                          ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                      }`}
                    >
                      {param.name}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Tool Details */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            {selectedTool ? (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {selectedTool.name}
                  </h3>
                  <button
                    onClick={() => copyToClipboard(JSON.stringify(selectedTool.example.request, null, 2), 'request')}
                    className="flex items-center px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
                  >
                    {copySuccess === 'request' ? (
                      <Check className="h-4 w-4 mr-1" />
                    ) : (
                      <Copy className="h-4 w-4 mr-1" />
                    )}
                    Copy Example
                  </button>
                </div>

                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  {selectedTool.description}
                </p>

                {/* Parameters */}
                <div className="mb-6">
                  <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-3">Parameters</h4>
                  <div className="space-y-3">
                    {selectedTool.parameters.map((param) => (
                      <div key={param.name} className="border dark:border-gray-700 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-mono text-sm text-gray-900 dark:text-white">
                            {param.name}
                          </span>
                          <div className="flex items-center space-x-2">
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {param.type}
                            </span>
                            {param.required && (
                              <span className="text-xs bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 px-2 py-1 rounded">
                                required
                              </span>
                            )}
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {param.description}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Example */}
                <div>
                  <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-3">Example</h4>
                  
                  <div className="mb-4">
                    <h5 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Request:</h5>
                    <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg text-sm overflow-x-auto">
                      <code className="text-gray-900 dark:text-gray-100">
                        {JSON.stringify(selectedTool.example.request, null, 2)}
                      </code>
                    </pre>
                  </div>

                  <div>
                    <h5 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Response:</h5>
                    <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg text-sm overflow-x-auto">
                      <code className="text-gray-900 dark:text-gray-100">
                        {JSON.stringify(selectedTool.example.response, null, 2)}
                      </code>
                    </pre>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  Select a tool to explore
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Choose a tool from the list to see its parameters and example usage
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Getting Started */}
        <div className="mt-12 bg-blue-50 dark:bg-blue-900 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Getting Started with MCP
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">1. Get Your API Key</h4>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Copy your API key from the dashboard and include it in your requests
              </p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">2. Make Requests</h4>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Use the Model Context Protocol to interact with our news data endpoints
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
} 