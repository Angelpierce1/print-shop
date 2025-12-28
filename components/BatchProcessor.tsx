'use client'

import { useState } from 'react'

interface BatchProcessorProps {
  targetWidth: number
}

export default function BatchProcessor({ targetWidth }: BatchProcessorProps) {
  const [files, setFiles] = useState<File[]>([])
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleFilesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || [])
    setFiles(selectedFiles)
    setResults([])
  }

  const handleProcess = async () => {
    if (files.length === 0) return

    setLoading(true)
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })
    formData.append('targetWidth', targetWidth.toString())

    try {
      const response = await fetch('/api/batch-check', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      setResults(data.results || [])
    } catch (error) {
      console.error('Error processing batch:', error)
    } finally {
      setLoading(false)
    }
  }

  const highQuality = results.filter((r) => r.quality === 'high').length
  const lowQuality = results.filter((r) => r.quality === 'low').length

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Batch Process Images</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Choose multiple image files
        </label>
        <input
          type="file"
          accept="image/*"
          multiple
          onChange={handleFilesChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-opacity-90"
        />
      </div>

      {files.length > 0 && (
        <div className="mb-4 p-4 bg-blue-50 rounded-lg">
          <p>📁 {files.length} file(s) selected</p>
        </div>
      )}

      {files.length > 0 && (
        <button
          onClick={handleProcess}
          disabled={loading}
          className="w-full mb-6 px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 disabled:opacity-50"
        >
          {loading ? 'Processing...' : '🚀 Process All Images'}
        </button>
      )}

      {results.length > 0 && (
        <div>
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-green-50 p-4 rounded-lg text-center">
              <p className="text-2xl font-bold text-green-800">
                ✅ {highQuality}
              </p>
              <p className="text-sm text-green-600">High Quality</p>
            </div>
            <div className="bg-yellow-50 p-4 rounded-lg text-center">
              <p className="text-2xl font-bold text-yellow-800">
                ⚠️ {lowQuality}
              </p>
              <p className="text-sm text-yellow-600">Low Quality</p>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold">📋 Detailed Results</h3>
            {results.map((result, idx) => (
              <details
                key={idx}
                className="bg-gray-50 p-4 rounded-lg cursor-pointer"
              >
                <summary className="font-medium">
                  📷 {result.filename}
                </summary>
                <div className="mt-4 space-y-2">
                  {result.status === 'success' ? (
                    <>
                      <div
                        className={`p-3 rounded-lg ${
                          result.quality === 'high'
                            ? 'bg-green-50 text-green-800'
                            : 'bg-yellow-50 text-yellow-800'
                        }`}
                      >
                        {result.message}
                      </div>
                      <div className="text-sm space-y-1">
                        <p>
                          <strong>Dimensions:</strong> {result.width_px} ×{' '}
                          {result.height_px} pixels
                        </p>
                        <p>
                          <strong>Max Dimension:</strong> {result.max_dimension} pixels
                        </p>
                        <p>
                          <strong>Range:</strong> 480+ pixels
                        </p>
                      </div>
                    </>
                  ) : (
                    <div className="p-3 bg-red-50 text-red-800 rounded-lg">
                      {result.message}
                    </div>
                  )}
                </div>
              </details>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}




