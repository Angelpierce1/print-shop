import { NextRequest, NextResponse } from 'next/server'
import sharp from 'sharp'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const files = formData.getAll('files') as File[]
    const quality = parseInt(formData.get('quality') as string) || 95

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

          // Convert HEIC to JPG using sharp
          const jpgBuffer = await sharp(buffer)
            .jpeg({ quality })
            .toBuffer()

          const original_size = buffer.length
          const converted_size = jpgBuffer.length

          // In a real app, you'd save this to storage and return a URL
          // For now, we'll return base64 or handle differently
          const base64 = jpgBuffer.toString('base64')
          const dataUrl = `data:image/jpeg;base64,${base64}`

          return {
            original: file.name,
            converted: file.name.replace(/\.(heic|heif)$/i, '.jpg'),
            original_size,
            converted_size,
            download_url: dataUrl, // In production, use actual file storage
          }
        } catch (error: any) {
          return {
            original: file.name,
            error: error.message || 'Error converting file',
          }
        }
      })
    )

    return NextResponse.json({ results })
  } catch (error: any) {
    return NextResponse.json(
      { status: 'error', message: error.message || 'Error converting HEIC' },
      { status: 500 }
    )
  }
}



