'use client'

import { useState } from 'react'
import ImageUploader from '../components/ImageUploader'
import BatchProcessor from '../components/BatchProcessor'
import HEICConverter from '../components/HEICConverter'

export default function Home() {
  const [activeTab, setActiveTab] = useState('upload')
  const [targetWidth, setTargetWidth] = useState(8.0)

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-2">
            🖨️ Print Shop
          </h1>
          <p className="text-lg text-gray-600">
            Image Quality Checker - Verify print quality standards (300 DPI minimum)
          </p>
        </div>

        {/* Settings Sidebar */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">⚙️ Settings</h2>
          <label className="block mb-2 text-sm font-medium text-gray-700">
            Target Print Width (inches)
          </label>
          <input
            type="number"
            min="0.1"
            max="100"
            step="0.5"
            value={targetWidth}
            onChange={(e) => setTargetWidth(parseFloat(e.target.value))}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <p className="mt-2 text-sm text-gray-500">
            The width you want to print the image at
          </p>
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold mb-2">📊 Quality Standards</h3>
            <p className="text-sm">
              <strong>High Quality:</strong> ≥ 300 DPI<br />
              <strong>Low Quality:</strong> &lt; 300 DPI
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6" aria-label="Tabs">
              <button
                onClick={() => setActiveTab('upload')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'upload'
                    ? 'border-primary text-primary'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                📤 Upload & Check
              </button>
              <button
                onClick={() => setActiveTab('batch')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'batch'
                    ? 'border-primary text-primary'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                📁 Batch Process
              </button>
              <button
                onClick={() => setActiveTab('heic')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'heic'
                    ? 'border-primary text-primary'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                🔄 HEIC Converter
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'upload' && (
              <ImageUploader targetWidth={targetWidth} />
            )}
            {activeTab === 'batch' && (
              <BatchProcessor targetWidth={targetWidth} />
            )}
            {activeTab === 'heic' && <HEICConverter />}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <h3 className="font-semibold mb-2">📝 How it works</h3>
          <ol className="list-decimal list-inside space-y-1">
            <li>Upload an image using the file uploader</li>
            <li>The app checks the image&apos;s DPI (dots per inch) at your target print width</li>
            <li>High quality images have ≥ 300 DPI (standard for professional printing)</li>
            <li>Low quality images have &lt; 300 DPI and may appear pixelated when printed</li>
          </ol>
        </div>
      </div>
    </main>
  )
}
