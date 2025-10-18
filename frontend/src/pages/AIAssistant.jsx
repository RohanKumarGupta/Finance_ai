import { useState } from 'react'
import { api } from '../utils/api'
import { Bot, FileText, Lightbulb, Sparkles, Upload } from 'lucide-react'

export default function AIAssistant() {
  const [documentText, setDocumentText] = useState('')
  const [selectedFile, setSelectedFile] = useState(null)
  const [summary, setSummary] = useState('')
  const [advice, setAdvice] = useState('')
  const [loadingSummary, setLoadingSummary] = useState(false)
  const [loadingAdvice, setLoadingAdvice] = useState(false)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
      setDocumentText('') // Clear text when file is selected
    }
  }

  const handleSummarize = async (e) => {
    e.preventDefault()
    setLoadingSummary(true)
    setSummary('')

    try {
      if (selectedFile) {
        // Upload file
        const formData = new FormData()
        formData.append('file', selectedFile)
        
        const token = localStorage.getItem('token')
        const response = await fetch('/api/ai/summarize', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })
        
        if (!response.ok) {
          throw new Error('Failed to summarize file')
        }
        
        const data = await response.json()
        setSummary(data.summary)
      } else {
        // Use text
        const formData = new FormData()
        formData.append('text', documentText)
        
        const token = localStorage.getItem('token')
        const response = await fetch('/api/ai/summarize', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })
        
        if (!response.ok) {
          throw new Error('Failed to summarize text')
        }
        
        const data = await response.json()
        setSummary(data.summary)
      }
    } catch (error) {
      console.error('Summarization failed:', error)
      setSummary(`Error: ${error.message}`)
    } finally {
      setLoadingSummary(false)
    }
  }

  const handleGetAdvice = async () => {
    setLoadingAdvice(true)
    setAdvice('')

    try {
      const data = await api.get('/ai/advice')
      setAdvice(data.advice)
    } catch (error) {
      console.error('Failed to get advice:', error)
      setAdvice(`Error: ${error.message}`)
    } finally {
      setLoadingAdvice(false)
    }
  }

  const sampleDocument = `STUDENT FEE INVOICE
Academic Year 2024-2025

Student: Jamie Martin
Class: 8-A

Fee Breakdown:
- Tuition Fee: ₹50,000
- Hostel Fee: ₹30,000
- Transport Fee: ₹10,000
- Total: ₹90,000

Scholarships Applied:
- Merit Scholarship: ₹8,000

Net Amount Due: ₹82,000
Due Date: October 31, 2024

Please ensure payment is made before the due date to avoid late fees.`

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
        <p className="text-gray-600 mt-2">Powered by Gemini AI via LangChain</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Document Summarizer */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-6">
            <FileText className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">Document Summarizer</h2>
          </div>

          <form onSubmit={handleSummarize} className="space-y-4">
            {/* File Upload */}
            <div>
              <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700 mb-2">
                Upload Document (PDF, Image, DOC)
              </label>
              <div className="flex items-center space-x-2">
                <label className="flex-1 flex items-center justify-center px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-primary-500 transition-colors">
                  <Upload className="w-5 h-5 text-gray-400 mr-2" />
                  <span className="text-sm text-gray-600">
                    {selectedFile ? selectedFile.name : 'Choose file or drag here'}
                  </span>
                  <input
                    id="file-upload"
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,image/*"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                </label>
                {selectedFile && (
                  <button
                    type="button"
                    onClick={() => setSelectedFile(null)}
                    className="btn btn-secondary"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>

            {/* Text Input (alternative) */}
            {!selectedFile && (
              <div>
                <label htmlFor="document" className="block text-sm font-medium text-gray-700 mb-2">
                  Or Paste Text
                </label>
                <textarea
                  id="document"
                  value={documentText}
                  onChange={(e) => setDocumentText(e.target.value)}
                  className="input min-h-[150px] font-mono text-sm"
                  placeholder="Paste your fee invoice, receipt, or financial document here..."
                />
              </div>
            )}

            <div className="flex space-x-2">
              <button
                type="submit"
                disabled={loadingSummary || (!documentText && !selectedFile)}
                className="btn btn-primary flex-1"
              >
                {loadingSummary ? (
                  <span className="flex items-center justify-center">
                    <Sparkles className="w-4 h-4 mr-2 animate-pulse" />
                    Analyzing...
                  </span>
                ) : (
                  'Summarize'
                )}
              </button>
              {!selectedFile && (
                <button
                  type="button"
                  onClick={() => setDocumentText(sampleDocument)}
                  className="btn btn-secondary"
                >
                  Load Sample
                </button>
              )}
            </div>
          </form>

          {summary && (
            <div className="mt-6 p-4 bg-primary-50 border border-primary-200 rounded-lg">
              <div className="flex items-center space-x-2 mb-3">
                <Bot className="w-5 h-5 text-primary-600" />
                <h3 className="font-semibold text-gray-900">AI Summary</h3>
              </div>
              <p className="text-gray-700 whitespace-pre-wrap">{summary}</p>
            </div>
          )}
        </div>

        {/* Financial Advice */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-6">
            <Lightbulb className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">Financial Planning Advice</h2>
          </div>

          <p className="text-gray-600 mb-6">
            Get personalized financial planning advice based on your student's fee breakdown and payment history.
          </p>

          <button
            onClick={handleGetAdvice}
            disabled={loadingAdvice}
            className="btn btn-primary w-full"
          >
            {loadingAdvice ? (
              <span className="flex items-center justify-center">
                <Sparkles className="w-4 h-4 mr-2 animate-pulse" />
                Generating Advice...
              </span>
            ) : (
              <span className="flex items-center justify-center">
                <Lightbulb className="w-4 h-4 mr-2" />
                Get AI Advice
              </span>
            )}
          </button>

          {advice && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center space-x-2 mb-3">
                <Bot className="w-5 h-5 text-green-600" />
                <h3 className="font-semibold text-gray-900">Personalized Advice</h3>
              </div>
              <p className="text-gray-700 whitespace-pre-wrap">{advice}</p>
            </div>
          )}
        </div>
      </div>

      {/* Info Card */}
      <div className="card bg-gradient-to-br from-purple-50 to-blue-50 border-purple-200">
        <div className="flex items-start space-x-4">
          <div className="flex-shrink-0">
            <Sparkles className="w-8 h-8 text-purple-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">About AI Features</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Document Summarizer:</strong> Paste any financial document (fee invoice, receipt, etc.) and get a concise summary highlighting key information.</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Financial Advice:</strong> Receive personalized planning recommendations based on your student's fee structure and payment patterns.</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span><strong>Powered by Gemini:</strong> All AI features use Google's Gemini AI model via LangChain for accurate and helpful responses.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
