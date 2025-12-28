import { NextRequest, NextResponse } from 'next/server'
import sharp from 'sharp'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const files = formData.getAll('files') as File[]
    const targetWidth = parseFloat(formData.get('targetWidth') as string) || 8.0

    if (!files || files.length === 0) {
      return NextResponse.json(
        { status: 'error', message: 'No files provided' },
        { status: 400 }
      )
    }

    const results = await Promise.all(
      files.map(async (file) => {
        try {
          const arrayBuffer = await file.arrayBuffer()
          const buffer = Buffer.from(arrayBuffer)

          const metadata = await sharp(buffer).metadata()
          const width_px = metadata.width || 0
          const height_px = metadata.height || 0
          const min_pixels = 480

          // Check pixel dimensions (using the larger dimension)
          const max_dimension = Math.max(width_px, height_px)

          let message = ''
          let quality: 'high' | 'low' = 'low'

          if (max_dimension >= min_pixels) {
            message = `✅ Image dimensions are within acceptable range (${width_px} × ${height_px} pixels) - High Quality!`
            quality = 'high'
          } else {
            message = `⚠️ Image too small. Maximum dimension is ${max_dimension} pixels (minimum: ${min_pixels} pixels) - Low Quality`
            quality = 'low'
          }

          return {
            status: 'success',
            filename: file.name,
            width_px,
            height_px,
            max_dimension,
            message,
            quality,
          }
        } catch (error: any) {
          return {
            status: 'error',
            filename: file.name,
            message: error.message || 'Error processing file',
          }
        }
      })
    )

    return NextResponse.json({ results })
  } catch (error: any) {
    return NextResponse.json(
      { status: 'error', message: error.message || 'Error processing batch' },
      { status: 500 }
    )
  }
}




