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
          const dpi = metadata.density || null
          const metadata_dpi = dpi ? Math.round(dpi) : null
          const effective_dpi = width_px / targetWidth

          let message = ''
          let quality: 'high' | 'low' = 'low'

          if (metadata_dpi && metadata_dpi >= 300) {
            message = `✅ Metadata confirms ${metadata_dpi} DPI - High Quality!`
            quality = 'high'
          } else if (effective_dpi >= 300) {
            message = `✅ Pixel density is high enough (${Math.round(effective_dpi)} effective DPI) - High Quality!`
            quality = 'high'
          } else {
            message = `⚠️ Image too small. Only ${Math.round(effective_dpi)} DPI at ${targetWidth}" - Low Quality`
            quality = 'low'
          }

          return {
            status: 'success',
            filename: file.name,
            metadata_dpi,
            effective_dpi,
            width_px,
            height_px,
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
