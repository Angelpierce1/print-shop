'use client'

import { useState } from 'react'

export default function HEICConverter() {
  const [files, setFiles] = useState<File[]>([])
  const [quality, setQuality] = useState(95)
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleFilesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || [])
    setFiles(selectedFiles.filter(f => 
      f.name.toLowerCase().endsWith('.heic') || 
      f.name.toLowerCase().endsWith('.heif')
    ))
    setResults([])
  }

  const handleConvert = async () => {
    if (files.length === 0) return

    setLoading(true)
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })
    formData.append('quality', quality.toString())

    try {
      const response = await fetch('/api/convert-heic', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      setResults(data.results || [])
    } catch (error) {
      console.error('Error converting HEIC:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">🔄 HEIC to JPG Converter</h2>
      <p className="text-gray-600 mb-6">
        Convert HEIC/HEIF images to JPG format for better compatibility
      </p>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload HEIC/HEIF files to convert
        </label>
        <input
          type="file"
          accept=".heic,.heif"
          multiple
          onChange={handleFilesChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-opacity-90"
        />
      </div>

      {files.length > 0 && (
        <>
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                JPG Quality
              </label>
              <input
                type="range"
                min="50"
                max="100"
                value={quality}
                onChange={(e) => setQuality(parseInt(e.target.value))}
                className="w-full"
              />
              <p className="text-sm text-gray-500 mt-1">
                {quality} - Higher quality = larger file size (95 is recommended)
              </p>
            </div>
          </div>

          <button
            onClick={handleConvert}
            disabled={loading}
            className="w-full mb-6 px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 disabled:opacity-50"
          >
            {loading ? 'Converting...' : '🚀 Convert All HEIC Files'}
          </button>
        </>
      )}

      {results.length > 0 && (
        <div>
          <div className="mb-4 p-4 bg-green-50 text-green-800 rounded-lg">
            ✅ Successfully converted {results.length} file(s)
          </div>

          <div className="space-y-4">
            {results.map((result, idx) => (
              <details
                key={idx}
                className="bg-gray-50 p-4 rounded-lg cursor-pointer"
              >
                <summary className="font-medium">
                  ✅ {result.original} → {result.converted}
                </summary>
                <div className="mt-4 grid grid-cols-3 gap-4">
                  <div className="bg-white p-3 rounded-lg text-center">
                    <p className="text-xs text-gray-500">Original Size</p>
                    <p className="text-lg font-semibold">
                      {(result.original_size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <div className="bg-white p-3 rounded-lg text-center">
                    <p className="text-xs text-gray-500">JPG Size</p>
                    <p className="text-lg font-semibold">
                      {(result.converted_size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <div className="bg-white p-3 rounded-lg text-center">
                    <p className="text-xs text-gray-500">Size Change</p>
                    <p className="text-lg font-semibold">
                      {(
                        ((result.converted_size - result.original_size) /
                          result.original_size) *
                        100
                      ).toFixed(1)}
                      %
                    </p>
                  </div>
                </div>
                {result.download_url && (
                  <a
                    href={result.download_url}
                    download
                    className="mt-4 inline-block px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90"
                  >
                    📥 Download {result.converted}
                  </a>
                )}
              </details>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}



