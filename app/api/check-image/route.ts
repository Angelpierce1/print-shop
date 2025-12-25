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
    const dpi = metadata.density || null
    const metadata_dpi = dpi ? Math.round(dpi) : null

    // Calculate effective DPI
    const effective_dpi = width_px / targetWidth

    const result = {
      status: 'success',
      metadata_dpi,
      effective_dpi,
      width_px,
      height_px,
      target_width_inch: targetWidth,
      message: '',
      quality: '' as 'high' | 'low',
    }

    if (metadata_dpi && metadata_dpi >= 300) {
      result.message = `✅ Metadata confirms ${metadata_dpi} DPI - High Quality!`
      result.quality = 'high'
    } else if (effective_dpi >= 300) {
      result.message = `✅ Pixel density is high enough (${Math.round(effective_dpi)} effective DPI) - High Quality!`
      result.quality = 'high'
    } else {
      result.message = `⚠️ Image too small. Only ${Math.round(effective_dpi)} DPI at ${targetWidth}" - Low Quality`
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
