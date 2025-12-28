import { NextRequest, NextResponse } from 'next/server'
import sharp from 'sharp'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File
    const targetWidth = parseFloat(formData.get('targetWidth') as string) || 8.0

    if (!file) {
      return NextResponse.json(
        { status: 'error', message: 'No file provided' },
        { status: 400 }
      )
    }

    const arrayBuffer = await file.arrayBuffer()
    const buffer = Buffer.from(arrayBuffer)

    // Get image metadata using sharp
    const metadata = await sharp(buffer).metadata()
    
    const width_px = metadata.width || 0
    const height_px = metadata.height || 0
    const min_pixels = 480

    // Check pixel dimensions (using the larger dimension)
    const max_dimension = Math.max(width_px, height_px)

    const result = {
      status: 'success',
      width_px,
      height_px,
      max_dimension,
      target_width_inch: targetWidth,
      message: '',
      quality: '' as 'high' | 'low',
    }

    if (max_dimension >= min_pixels) {
      result.message = `✅ Image dimensions are within acceptable range (${width_px} × ${height_px} pixels) - High Quality!`
      result.quality = 'high'
    } else {
      result.message = `⚠️ Image too small. Maximum dimension is ${max_dimension} pixels (minimum: ${min_pixels} pixels) - Low Quality`
      result.quality = 'low'
    }

    return NextResponse.json(result)
  } catch (error: any) {
    return NextResponse.json(
      { status: 'error', message: error.message || 'Error processing image' },
      { status: 500 }
    )
  }
}




