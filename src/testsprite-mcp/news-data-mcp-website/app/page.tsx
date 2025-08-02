import { ArrowRight, Check, Zap, Shield, Globe } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-blue-900">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Zap className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900 dark:text-white">News Data MCP</span>
          </div>
          <div className="hidden md:flex items-center space-x-6">
            <a href="/docs" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Docs</a>
            <a href="#features" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Features</a>
            <a href="#pricing" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Pricing</a>
            <Link href="/auth/signin" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Sign In</Link>
            <Link href="/dashboard" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Get API Key
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            AI-Powered News for Your
            <span className="text-blue-600"> LLMs</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            Subscribe to News Data MCP and retrieve fresh, structured news articles for your Large Language Models via our Model Context Protocol endpoints.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/auth/signup" className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center">
              Start Free Trial
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
            <Link href="#features" className="border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              Learn More
            </Link>
          </div>
        </div>
      </main>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white dark:bg-gray-800">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Powerful Features for Modern AI
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Everything you need to integrate fresh news data into your LLM applications
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="bg-blue-100 dark:bg-blue-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Real-time News</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Access fresh news articles updated in real-time from hundreds of trusted sources worldwide.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="bg-green-100 dark:bg-green-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Structured Data</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Get news in structured formats perfect for LLMs with metadata, facts, and entity extraction.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="bg-purple-100 dark:bg-purple-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Globe className="h-8 w-8 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">MCP Protocol</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Native support for Model Context Protocol for seamless integration with your AI applications.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Choose the plan that fits your needs. Start free, scale as you grow.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free Plan */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg">
              <div className="text-center">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Free</h3>
                <div className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                  $0<span className="text-lg text-gray-500">/month</span>
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-6">Perfect for testing and small projects</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">1,000 tokens/month</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Basic news search</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Standard rate limits</span>
                </li>
              </ul>
              <Link href="/auth/signup" className="w-full bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white py-3 rounded-lg font-semibold hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors block text-center">
                Get Started
              </Link>
            </div>

            {/* Monthly Plan */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg border-2 border-blue-500 relative">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                  Most Popular
                </span>
              </div>
              <div className="text-center">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Monthly</h3>
                <div className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                  $29<span className="text-lg text-gray-500">/month</span>
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-6">Ideal for growing applications</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">100,000 tokens/month</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Advanced search & filters</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Priority support</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Higher rate limits</span>
                </li>
              </ul>
              <Link href="/auth/signup" className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors block text-center">
                Start Monthly Plan
              </Link>
            </div>

            {/* Yearly Plan */}
            <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg">
              <div className="text-center">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Yearly</h3>
                <div className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                  $290<span className="text-lg text-gray-500">/year</span>
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-6">Best value for established apps</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">1,200,000 tokens/year</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">All Monthly features</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">2 months free</span>
                </li>
                <li className="flex items-center">
                  <Check className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Dedicated support</span>
                </li>
              </ul>
              <Link href="/auth/signup" className="w-full bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white py-3 rounded-lg font-semibold hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors block text-center">
                Start Yearly Plan
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Zap className="h-6 w-6 text-blue-600" />
              <span className="text-lg font-semibold text-gray-900 dark:text-white">News Data MCP</span>
            </div>
            <div className="flex space-x-6">
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">Terms</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">Privacy</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">Support</a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              © 2024 News Data MCP. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
