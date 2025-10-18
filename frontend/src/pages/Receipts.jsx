import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { Receipt, FileText, TrendingUp, Calendar, DollarSign } from 'lucide-react'

export default function Receipts() {
  const [receipts, setReceipts] = useState([])
  const [loading, setLoading] = useState(true)
  const [summary, setSummary] = useState('')
  const [prompt, setPrompt] = useState('')
  const [summarizing, setSummarizing] = useState(false)

  useEffect(() => {
    fetchReceipts()
  }, [])

  const fetchReceipts = async () => {
    try {
      const data = await api.get('/payments/all-receipts')
      setReceipts(data.receipts || [])
    } catch (error) {
      console.error('Failed to fetch receipts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSummarize = async (e) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setSummarizing(true)
    setSummary('')

    try {
      const data = await api.post('/payments/summarize-receipts', { prompt })
      setSummary(data.summary)
    } catch (error) {
      console.error('Failed to generate summary:', error)
      setSummary('Failed to generate summary. Please try again.')
    } finally {
      setSummarizing(false)
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    })
  }

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'tuition':
        return <FileText className="w-5 h-5 text-blue-600" />
      case 'hostel':
        return <TrendingUp className="w-5 h-5 text-green-600" />
      case 'transport':
        return <Calendar className="w-5 h-5 text-orange-600" />
      default:
        return <DollarSign className="w-5 h-5 text-gray-600" />
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Payment Receipts</h1>
        <p className="text-gray-600 mt-2">View all your payment receipts and get AI-powered summaries</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* All Receipts */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-6">
            <Receipt className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">All Receipts</h2>
          </div>

          {receipts.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No payment receipts found</p>
          ) : (
            <div className="space-y-4">
              {receipts.map((receipt) => (
                <div key={receipt.receipt_id} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      {getCategoryIcon(receipt.category)}
                      <div>
                        <p className="font-medium text-gray-900">{receipt.student_name}</p>
                        <p className="text-sm text-gray-600">Class {receipt.student_class}</p>
                      </div>
                    </div>
                    <span className="text-sm text-gray-500">
                      {formatDate(receipt.paid_at)}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-600 capitalize">{receipt.category}</span>
                      <span className="text-xs bg-gray-100 px-2 py-1 rounded-full">
                        {receipt.receipt_id}
                      </span>
                    </div>
                    <span className="font-semibold text-gray-900">
                      {formatCurrency(receipt.amount)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* AI Summary */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-6">
            <FileText className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">AI Receipt Summary</h2>
          </div>

          <form onSubmit={handleSummarize} className="space-y-4">
            <div>
              <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
                Ask me anything about your receipts
              </label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="input resize-none"
                rows="4"
                placeholder="Examples:
• How much did I spend on tuition this year?
• Show me payments for Jamie Martin
• What are my biggest expenses?
• Compare spending by category
• When was my last payment?"
                required
              />
            </div>

            <button
              type="submit"
              disabled={summarizing || !prompt.trim()}
              className="btn btn-primary w-full"
            >
              {summarizing ? 'Generating Summary...' : 'Generate Summary'}
            </button>
          </form>

          {summary && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-3">Summary</h3>
              <div className="prose prose-sm max-w-none">
                {summary.split('\n').map((line, index) => (
                  <p key={index} className="text-gray-700 mb-2 last:mb-0">
                    {line}
                  </p>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Summary Statistics */}
      {receipts.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Payment Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{receipts.length}</div>
              <div className="text-sm text-blue-700">Total Payments</div>
            </div>

            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatCurrency(receipts.reduce((sum, r) => sum + r.amount, 0))}
              </div>
              <div className="text-sm text-green-700">Total Amount</div>
            </div>

            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {formatCurrency(receipts.reduce((sum, r) => sum + r.amount, 0) / receipts.length)}
              </div>
              <div className="text-sm text-purple-700">Average Payment</div>
            </div>

            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {new Set(receipts.map(r => r.category)).size}
              </div>
              <div className="text-sm text-orange-700">Categories</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
