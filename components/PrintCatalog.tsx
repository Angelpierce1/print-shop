'use client'

import { useState, useEffect } from 'react'

interface PrintCatalogEntry {
  size: {
    width: number
    height: number
    label: string
  }
  best: { width: number; height: number }
  acceptable: { width: number; height: number }
}

interface SuitabilityResult {
  size: string
  status: 'excellent' | 'acceptable' | 'poor'
  message: string
}

export default function PrintCatalog() {
  const [catalog, setCatalog] = useState<PrintCatalogEntry[]>([])
  const [selectedSize, setSelectedSize] = useState<string>('')
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [results, setResults] = useState<{
    width_px: number
    height_px: number
    suitabilityResults: SuitabilityResult[]
  } | null>(null)
  const [loading, setLoading] = useState(false)
  const [loadingCatalog, setLoadingCatalog] = useState(true)

  useEffect(() => {
    // Load print catalog on mount
    fetch('/api/print-catalog')
      .then((res) => res.json())
      .then((data) => {
        setCatalog(data.catalog || [])
        setLoadingCatalog(false)
      })
      .catch((err) => {
        console.error('Error loading catalog:', err)
        setLoadingCatalog(false)
      })
  }, [])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(selectedFile)
      setResults(null)
    }
  }

  const handleCheck = async () => {
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/print-catalog', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      if (data.status === 'success') {
        setResults({
          width_px: data.width_px,
          height_px: data.height_px,
          suitabilityResults: data.suitabilityResults,
        })
      } else {
        setResults(null)
        alert(data.message || 'Error checking image')
      }
    } catch (error) {
      console.error('Error checking image:', error)
      alert('Failed to check image')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent':
        return 'bg-green-50 text-green-800 border-green-200'
      case 'acceptable':
        return 'bg-yellow-50 text-yellow-800 border-yellow-200'
      case 'poor':
        return 'bg-red-50 text-red-800 border-red-200'
      default:
        return 'bg-gray-50 text-gray-800 border-gray-200'
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Print Size Catalog</h2>

      {/* Print Catalog Dropdown */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3">📊 Standard Print Sizes & Requirements</h3>
        {loadingCatalog ? (
          <p className="text-gray-500">Loading catalog...</p>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Print Size
              </label>
              <select
                value={selectedSize}
                onChange={(e) => setSelectedSize(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-white"
              >
                <option value="">-- Select a print size --</option>
                {catalog.map((entry, idx) => (
                  <option key={idx} value={entry.size.label}>
                    {entry.size.label}
                  </option>
                ))}
              </select>
            </div>

            {selectedSize && (
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <h4 className="font-semibold mb-3 text-blue-900">
                  {selectedSize} Requirements:
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white p-3 rounded-lg">
                    <p className="text-sm font-medium text-gray-600 mb-1">
                      Best Quality (300 PPI)
                    </p>
                    <p className="text-lg font-semibold text-gray-800">
                      {catalog.find((e) => e.size.label === selectedSize)?.best.width} ×{' '}
                      {catalog.find((e) => e.size.label === selectedSize)?.best.height} px
                    </p>
                  </div>
                  <div className="bg-white p-3 rounded-lg">
                    <p className="text-sm font-medium text-gray-600 mb-1">
                      Acceptable (150 PPI)
                    </p>
                    <p className="text-lg font-semibold text-gray-800">
                      {catalog.find((e) => e.size.label === selectedSize)?.acceptable.width} ×{' '}
                      {catalog.find((e) => e.size.label === selectedSize)?.acceptable.height} px
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Image Upload Section */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3">🔍 Check Your Image</h3>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Choose an image file
          </label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-opacity-90"
          />
        </div>

        {preview && (
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-md font-semibold mb-2">📷 Image Preview</h4>
              <img
                src={preview}
                alt="Preview"
                className="w-full rounded-lg shadow-md mb-4"
              />
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm">
                  <strong>Filename:</strong> {file?.name}
                </p>
                {results && (
                  <p className="text-sm mt-2">
                    <strong>Dimensions:</strong> {results.width_px} × {results.height_px} pixels
                  </p>
                )}
              </div>
            </div>

            <div>
              <h4 className="text-md font-semibold mb-2">📋 Suitability Report</h4>
              <button
                onClick={handleCheck}
                disabled={loading}
                className="w-full mb-4 px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 disabled:opacity-50"
              >
                {loading ? 'Checking...' : 'Check Print Suitability'}
              </button>

              {results && (
                <div className="space-y-2">
                  {results.suitabilityResults.map((result, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border ${getStatusColor(result.status)}`}
                    >
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{result.size}</span>
                        <span className="text-sm">{result.message}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

