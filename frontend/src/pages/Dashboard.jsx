import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { DollarSign, TrendingUp, Clock, Award } from 'lucide-react'

export default function Dashboard() {
  const [feeBreakdown, setFeeBreakdown] = useState(null)
  const [paymentHistory, setPaymentHistory] = useState([])
  const [upcomingDues, setUpcomingDues] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [breakdown, history, dues] = await Promise.all([
        api.get('/dashboard/fee-breakdown'),
        api.get('/dashboard/payment-history'),
        api.get('/dashboard/upcoming-dues'),
      ])
      setFeeBreakdown(breakdown)
      setPaymentHistory(history.payments)
      setUpcomingDues(dues)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'bg-green-100 text-green-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Overview of your child's financial information</p>
      </div>

      {/* Student Info */}
      {feeBreakdown && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Student Information</h2>
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-2xl font-bold text-primary-600">
                {feeBreakdown.name.charAt(0)}
              </span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{feeBreakdown.name}</h3>
              <p className="text-gray-600">Class: {feeBreakdown.class_id}</p>
            </div>
          </div>
        </div>
      )}

      {/* Fee Breakdown */}
      {feeBreakdown && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Fee Breakdown</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(feeBreakdown.fee_breakdown).map(([category, amount]) => {
              const icons = {
                tuition: DollarSign,
                hostel: TrendingUp,
                transport: Clock,
                scholarships: Award,
              }
              const Icon = icons[category] || DollarSign
              const isScholarship = category === 'scholarships'

              return (
                <div
                  key={category}
                  className={`p-4 rounded-lg border-2 ${
                    isScholarship
                      ? 'bg-green-50 border-green-200'
                      : 'bg-gray-50 border-gray-200'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <Icon className={`w-5 h-5 ${isScholarship ? 'text-green-600' : 'text-gray-600'}`} />
                    <span className={`text-xs font-medium uppercase ${isScholarship ? 'text-green-600' : 'text-gray-600'}`}>
                      {category}
                    </span>
                  </div>
                  <p className={`text-2xl font-bold ${isScholarship ? 'text-green-700' : 'text-gray-900'}`}>
                    {formatCurrency(amount)}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Upcoming Dues */}
      {upcomingDues && (
        <div className="card bg-gradient-to-br from-orange-50 to-red-50 border-orange-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upcoming Dues</h2>
          <div className="space-y-3">
            {Object.entries(upcomingDues.dues_by_category).map(([category, amount]) => (
              amount > 0 && (
                <div key={category} className="flex justify-between items-center">
                  <span className="text-gray-700 capitalize">{category}</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(amount)}</span>
                </div>
              )
            ))}
            {upcomingDues.scholarships > 0 && (
              <div className="flex justify-between items-center text-green-700">
                <span>Scholarship Applied</span>
                <span className="font-semibold">-{formatCurrency(upcomingDues.scholarships)}</span>
              </div>
            )}
            <div className="pt-3 border-t-2 border-orange-200 flex justify-between items-center">
              <span className="text-lg font-semibold text-gray-900">Total Due</span>
              <span className="text-2xl font-bold text-orange-600">
                {formatCurrency(upcomingDues.total_due)}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Payment History */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Payment History</h2>
        {paymentHistory.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No payment history available</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Date</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Category</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Amount</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Status</th>
                </tr>
              </thead>
              <tbody>
                {paymentHistory.slice(0, 5).map((payment) => (
                  <tr key={payment._id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-sm text-gray-900">
                      {new Date(payment.created_at).toLocaleDateString('en-IN')}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-900 capitalize">
                      {payment.category}
                    </td>
                    <td className="py-3 px-4 text-sm font-semibold text-gray-900">
                      {formatCurrency(payment.amount)}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(payment.status)}`}>
                        {payment.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
