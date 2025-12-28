import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Print Shop - Image Quality Checker',
  description: 'Upload images to check if they meet print quality standards (480-1824 pixels)',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}




