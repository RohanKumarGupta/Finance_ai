import { useState, useEffect } from 'react'
import { api } from '../utils/api'
import { Bell, Plus, Calendar } from 'lucide-react'

export default function Reminders() {
  const [reminders, setReminders] = useState([])
  const [student, setStudent] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [message, setMessage] = useState('')
  const [dueDate, setDueDate] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [remindersData, studentData] = await Promise.all([
        api.get('/reminders/'),
        api.get('/dashboard/fee-breakdown'),
      ])
      setReminders(remindersData.reminders)
      setStudent(studentData)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/reminders/', {
        student_id: student.student_id,
        message,
        due_date: new Date(dueDate).toISOString(),
      })
      setMessage('')
      setDueDate('')
      setShowForm(false)
      await fetchData()
    } catch (error) {
      console.error('Failed to create reminder:', error)
      alert('Failed to create reminder: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  const isOverdue = (dateString) => {
    return new Date(dateString) < new Date()
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Payment Reminders</h1>
          <p className="text-gray-600 mt-2">Manage your payment reminders and due dates</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>New Reminder</span>
        </button>
      </div>

      {/* Create Reminder Form */}
      {showForm && student && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Create New Reminder</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
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
              <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                Reminder Message
              </label>
              <textarea
                id="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="input min-h-[100px]"
                placeholder="e.g., Pay tuition fee for Q2"
                required
              />
            </div>

            <div>
              <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-2">
                Due Date
              </label>
              <input
                id="dueDate"
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="input"
                min={new Date().toISOString().split('T')[0]}
                required
              />
            </div>

            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary flex-1"
              >
                {loading ? 'Creating...' : 'Create Reminder'}
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Reminders List */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <Bell className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">Your Reminders</h2>
        </div>

        {reminders.length === 0 ? (
          <div className="text-center py-12">
            <Bell className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No reminders yet</p>
            <p className="text-gray-400 text-sm mt-2">Create your first reminder to stay on track</p>
          </div>
        ) : (
          <div className="space-y-4">
            {reminders.map((reminder) => {
              const overdue = isOverdue(reminder.due_date)
              return (
                <div
                  key={reminder._id}
                  className={`p-4 rounded-lg border-2 ${
                    overdue
                      ? 'bg-red-50 border-red-200'
                      : 'bg-white border-gray-200 hover:border-primary-300'
                  } transition-colors`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-gray-900 font-medium mb-2">{reminder.message}</p>
                      <div className="flex items-center space-x-2 text-sm text-gray-600">
                        <Calendar className="w-4 h-4" />
                        <span>Due: {formatDate(reminder.due_date)}</span>
                        {overdue && (
                          <span className="ml-2 px-2 py-0.5 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                            Overdue
                          </span>
                        )}
                      </div>
                    </div>
                    <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                      overdue ? 'bg-red-100' : 'bg-primary-100'
                    }`}>
                      <Bell className={`w-5 h-5 ${overdue ? 'text-red-600' : 'text-primary-600'}`} />
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
