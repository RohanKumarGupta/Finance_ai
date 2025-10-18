import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { LogIn } from 'lucide-react'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-primary-100 via-accent-50 to-purple-100"></div>
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-400/30 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-400/30 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      <div className="max-w-md w-full animate-scale-in">
        <div className="text-center mb-8">
          <div className="relative inline-flex items-center justify-center mb-6 group">
            <div className="absolute inset-0 bg-gradient-primary rounded-3xl blur-xl opacity-75 group-hover:opacity-100 transition-opacity animate-glow"></div>
            <div className="relative w-20 h-20 bg-gradient-primary rounded-3xl flex items-center justify-center shadow-primary">
              <LogIn className="w-10 h-10 text-white" />
            </div>
          </div>
          <h2 className="text-4xl font-bold gradient-text mb-2">Welcome Back</h2>
          <p className="text-gray-700 text-lg font-medium">Sign in to your parent account</p>
        </div>

        <div className="card-glass shadow-glass-lg">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-danger-50 border-2 border-danger-200 text-danger-700 px-5 py-4 rounded-xl text-sm font-medium animate-scale-in">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-bold text-gray-700 mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="john.doe@example.com"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-bold text-gray-700 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary w-full text-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Signing in...
                </span>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-700 font-medium">
              Don't have an account?{' '}
              <Link to="/signup" className="gradient-text hover:underline font-bold">
                Sign up
              </Link>
            </p>
          </div>

          <div className="mt-6 pt-6 border-t-2 border-white/40">
            <div className="bg-primary-50/50 backdrop-blur-sm rounded-xl p-4 border border-primary-200/50">
              <p className="text-xs font-bold text-primary-700 text-center mb-2">🔑 Demo Credentials</p>
              <p className="text-xs text-gray-600 text-center font-mono">
                john.doe@example.com / password123
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
