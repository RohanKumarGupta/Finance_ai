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
      <div className="flex flex-col items-center justify-center h-64 space-y-4">
        <div className="spinner"></div>
        <p className="text-gray-600 font-medium">Loading your dashboard...</p>
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
        return 'badge-success'
      case 'failed':
        return 'badge-danger'
      case 'pending':
        return 'badge-warning'
      default:
        return 'badge bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-8 animate-slide-up">
      <div className="relative">
        <h1 className="text-4xl font-bold gradient-text">Dashboard</h1>
        <p className="text-gray-600 mt-2 text-lg">Overview of your child's financial information</p>
        <div className="absolute -top-4 -right-4 w-24 h-24 bg-primary-200/30 rounded-full blur-2xl"></div>
      </div>

      {/* Student Info */}
      {feeBreakdown && (
        <div className="card-gradient animate-scale-in">
          <div className="flex items-center space-x-6">
            <div className="relative group">
              <div className="absolute inset-0 bg-white/50 rounded-2xl blur-lg group-hover:blur-xl transition-all"></div>
              <div className="relative w-20 h-20 bg-white/30 backdrop-blur-sm rounded-2xl flex items-center justify-center border-2 border-white/40">
                <span className="text-3xl font-bold text-white drop-shadow-lg">
                  {feeBreakdown.name.charAt(0)}
                </span>
              </div>
            </div>
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-white drop-shadow-md">{feeBreakdown.name}</h3>
              <p className="text-white/90 text-lg mt-1">Class: <span className="font-semibold">{feeBreakdown.class_id}</span></p>
            </div>
          </div>
        </div>
      )}

      {/* Fee Breakdown */}
      {feeBreakdown && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <span className="gradient-text">Fee Breakdown</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(feeBreakdown.fee_breakdown).map(([category, amount], index) => {
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
                  className={`stat-card group hover:scale-105 transition-all duration-300 ${
                    isScholarship
                      ? 'bg-gradient-to-br from-success-50 to-success-100 border-success-200'
                      : 'bg-gradient-to-br from-white to-gray-50'
                  }`}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className={`icon-container w-10 h-10 ${
                      isScholarship ? 'bg-gradient-success' : 'bg-gradient-accent'
                    }`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className={`text-xs font-bold uppercase tracking-wider ${
                      isScholarship ? 'text-success-700' : 'text-gray-600'
                    }`}>
                      {category}
                    </span>
                  </div>
                  <p className={`text-3xl font-bold ${
                    isScholarship ? 'text-success-700' : 'text-gray-900'
                  }`}>
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
        <div className="card relative overflow-hidden bg-gradient-to-br from-warning-50 via-orange-50 to-danger-50 border-warning-200 shadow-lg">
          <div className="absolute top-0 right-0 w-40 h-40 bg-warning-300/20 rounded-full blur-3xl"></div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6 relative z-10">
            <span className="bg-gradient-to-r from-warning-600 to-danger-600 bg-clip-text text-transparent">Upcoming Dues</span>
          </h2>
          <div className="space-y-4 relative z-10">
            {Object.entries(upcomingDues.dues_by_category).map(([category, amount]) => (
              amount > 0 && (
                <div key={category} className="flex justify-between items-center p-3 bg-white/60 backdrop-blur-sm rounded-xl hover:bg-white/80 transition-all">
                  <span className="text-gray-700 capitalize font-semibold">{category}</span>
                  <span className="font-bold text-gray-900 text-lg">{formatCurrency(amount)}</span>
                </div>
              )
            ))}
            {upcomingDues.scholarships > 0 && (
              <div className="flex justify-between items-center p-3 bg-success-100/60 backdrop-blur-sm rounded-xl border border-success-200">
                <span className="text-success-700 font-semibold">Scholarship Applied</span>
                <span className="font-bold text-success-700 text-lg">-{formatCurrency(upcomingDues.scholarships)}</span>
              </div>
            )}
            <div className="pt-4 border-t-2 border-warning-300 flex justify-between items-center p-4 bg-white/80 backdrop-blur-sm rounded-xl">
              <span className="text-xl font-bold text-gray-900">Total Due</span>
              <span className="text-3xl font-bold bg-gradient-to-r from-warning-600 to-danger-600 bg-clip-text text-transparent">
                {formatCurrency(upcomingDues.total_due)}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Payment History */}
      <div className="card">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          <span className="gradient-text">Recent Payment History</span>
        </h2>
        {paymentHistory.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Receipt className="w-8 h-8 text-gray-400" />
            </div>
            <p className="text-gray-500 font-medium">No payment history available</p>
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl">
            <table className="table-modern">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Category</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {paymentHistory.slice(0, 5).map((payment, index) => (
                  <tr key={payment._id} style={{ animationDelay: `${index * 50}ms` }} className="animate-fade-in">
                    <td className="font-medium">
                      {new Date(payment.created_at).toLocaleDateString('en-IN')}
                    </td>
                    <td className="capitalize font-medium">
                      {payment.category}
                    </td>
                    <td className="font-bold text-gray-900">
                      {formatCurrency(payment.amount)}
                    </td>
                    <td>
                      <span className={`badge ${getStatusColor(payment.status)}`}>
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
