'use client'

import { useState } from 'react'

interface ImageUploaderProps {
  targetWidth: number
}

export default function ImageUploader({ targetWidth }: ImageUploaderProps) {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(selectedFile)
      setResult(null)
    }
  }

  const handleCheck = async () => {
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
    formData.append('targetWidth', targetWidth.toString())

    try {
      const response = await fetch('/api/check-image', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({ status: 'error', message: 'Failed to check image' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Upload Single Image</h2>
      
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
            <h3 className="text-lg font-semibold mb-2">📷 Image Preview</h3>
            <img
              src={preview}
              alt="Preview"
              className="w-full rounded-lg shadow-md mb-4"
            />
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm">
                <strong>Filename:</strong> {file?.name}
              </p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-2">🔍 Quality Analysis</h3>
            <button
              onClick={handleCheck}
              disabled={loading}
              className="w-full mb-4 px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 disabled:opacity-50"
            >
              {loading ? 'Checking...' : 'Check Quality'}
            </button>

            {result && (
              <div className="space-y-4">
                {result.status === 'success' ? (
                  <>
                    <div
                      className={`p-4 rounded-lg ${
                        result.quality === 'high'
                          ? 'bg-green-50 text-green-800'
                          : 'bg-yellow-50 text-yellow-800'
                      }`}
                    >
                      {result.message}
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="bg-gray-50 p-3 rounded-lg text-center">
                        <p className="text-xs text-gray-500">Width (pixels)</p>
                        <p className="text-lg font-semibold">
                          {result.width_px}
                        </p>
                      </div>
                      <div className="bg-gray-50 p-3 rounded-lg text-center">
                        <p className="text-xs text-gray-500">Height (pixels)</p>
                        <p className="text-lg font-semibold">
                          {result.height_px}
                        </p>
                      </div>
                      <div className="bg-gray-50 p-3 rounded-lg text-center">
                        <p className="text-xs text-gray-500">Max Dimension</p>
                        <p className="text-lg font-semibold">
                          {result.max_dimension}
                        </p>
                      </div>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm">
                        <strong>Pixel range:</strong> 480 - 1824 pixels
                      </p>
                    </div>
                  </>
                ) : (
                  <div className="p-4 bg-red-50 text-red-800 rounded-lg">
                    {result.message}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}




