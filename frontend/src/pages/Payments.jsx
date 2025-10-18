import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { CreditCard, Receipt, CheckCircle, XCircle } from 'lucide-react'

export default function Payments() {
  const [student, setStudent] = useState(null)
  const [feeBreakdown, setFeeBreakdown] = useState(null)
  const [amount, setAmount] = useState('')
  const [category, setCategory] = useState('tuition')
  const [simulate, setSimulate] = useState('success')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [receipt, setReceipt] = useState(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [studentData, feeData] = await Promise.all([
        api.get('/dashboard/fee-breakdown'),
        api.get('/dashboard/fee-breakdown')
      ])
      setStudent(studentData)
      setFeeBreakdown(feeData)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    }
  }

  // Auto-populate amount when category changes
  useEffect(() => {
    if (feeBreakdown && feeBreakdown.fee_breakdown) {
      const categoryFee = feeBreakdown.fee_breakdown[category]
      if (categoryFee) {
        setAmount(categoryFee.toString())
      }
    }
  }, [category, feeBreakdown])

  const handlePayment = async (e) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)
    setReceipt(null)

    try {
      const data = await api.post('/payments/initiate', {
        student_id: student.student_id,
        amount: parseFloat(amount),
        category,
        simulate,
      })
      setResult(data.payment)

      if (data.payment.status === 'success') {
        const receiptData = await api.get(`/payments/receipt/${data.payment._id}`)
        setReceipt(receiptData.receipt)

        // Refresh fee breakdown data after successful payment
        await fetchData()
      }
    } catch (error) {
      console.error('Payment failed:', error)
      setResult({ status: 'failed', error: error.message })
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const getCategoryFee = (cat) => {
    if (feeBreakdown && feeBreakdown.fee_breakdown && feeBreakdown.fee_breakdown[cat]) {
      return formatCurrency(feeBreakdown.fee_breakdown[cat])
    }
    return 'Not available'
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Payments</h1>
        <p className="text-gray-600 mt-2">Initiate dummy payment transactions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Payment Form */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-6">
            <CreditCard className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">Initiate Payment</h2>
          </div>

          {student && (
            <form onSubmit={handlePayment} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Student
                </label>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="font-medium text-gray-900">{student.name}</p>
                  <p className="text-sm text-gray-600">Class: {student.class_id}</p>
                </div>
              </div>

              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  id="category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="input"
                  required
                >
                  <option value="tuition">Tuition ({getCategoryFee('tuition')})</option>
                  <option value="hostel">Hostel ({getCategoryFee('hostel')})</option>
                  <option value="transport">Transport ({getCategoryFee('transport')})</option>
                  <option value="other">Other ({getCategoryFee('other')})</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  Fee will be auto-populated when category is selected
                </p>
              </div>

              <div>
                <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
                  Amount (₹)
                </label>
                <input
                  id="amount"
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="input"
                  placeholder="10000"
                  min="1"
                  required
                />
                {feeBreakdown && feeBreakdown.fee_breakdown && feeBreakdown.fee_breakdown[category] && (
                  <p className="text-xs text-gray-500 mt-1">
                    Auto-filled from category fee: {formatCurrency(feeBreakdown.fee_breakdown[category])}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="simulate" className="block text-sm font-medium text-gray-700 mb-2">
                  Simulate Result (Demo Only)
                </label>
                <select
                  id="simulate"
                  value={simulate}
                  onChange={(e) => setSimulate(e.target.value)}
                  className="input"
                >
                  <option value="success">Success</option>
                  <option value="failed">Failed</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  This simulates the payment gateway response
                </p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary w-full"
              >
                {loading ? 'Processing...' : 'Initiate Payment'}
              </button>
            </form>
          )}
        </div>

        {/* Result */}
        <div className="space-y-6">
          {result && (
            <div className={`card ${result.status === 'success' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
              <div className="flex items-center space-x-3 mb-4">
                {result.status === 'success' ? (
                  <CheckCircle className="w-8 h-8 text-green-600" />
                ) : (
                  <XCircle className="w-8 h-8 text-red-600" />
                )}
                <h2 className="text-xl font-semibold text-gray-900">
                  Payment {result.status === 'success' ? 'Successful' : 'Failed'}
                </h2>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-700">Amount:</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(result.amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Category:</span>
                  <span className="font-semibold text-gray-900 capitalize">{result.category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700">Status:</span>
                  <span className={`font-semibold ${result.status === 'success' ? 'text-green-600' : 'text-red-600'}`}>
                    {result.status}
                  </span>
                </div>
                {result.receipt_id && (
                  <div className="flex justify-between">
                    <span className="text-gray-700">Receipt ID:</span>
                    <span className="font-mono text-sm text-gray-900">{result.receipt_id}</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {receipt && (
            <div className="card">
              <div className="flex items-center space-x-3 mb-6">
                <Receipt className="w-6 h-6 text-primary-600" />
                <h2 className="text-xl font-semibold text-gray-900">Receipt</h2>
              </div>

              <div className="space-y-4">
                <div className="p-4 bg-gray-50 rounded-lg space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Receipt ID:</span>
                    <span className="font-mono text-gray-900">{receipt.receipt_id}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Payment ID:</span>
                    <span className="font-mono text-gray-900">{receipt.payment_id}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Date:</span>
                    <span className="text-gray-900">
                      {new Date(receipt.paid_at).toLocaleString('en-IN')}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Category:</span>
                    <span className="text-gray-900 capitalize">{receipt.category}</span>
                  </div>
                  <div className="flex justify-between pt-2 border-t border-gray-200">
                    <span className="font-semibold text-gray-900">Amount Paid:</span>
                    <span className="font-bold text-lg text-green-600">
                      {formatCurrency(receipt.amount)}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => window.print()}
                  className="btn btn-secondary w-full"
                >
                  Print Receipt
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
