import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import { generateApiKey } from '@/lib/utils'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json(
        { message: 'Unauthorized' },
        { status: 401 }
      )
    }

    const { name } = await request.json()

    if (!name) {
      return NextResponse.json(
        { message: 'API key name is required' },
        { status: 400 }
      )
    }

    const apiKey = await prisma.apiKey.create({
      data: {
        key: generateApiKey(),
        name,
        userId: session.user.id
      }
    })

    return NextResponse.json(apiKey, { status: 201 })

  } catch (error) {
    console.error('API key creation error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json(
        { message: 'Unauthorized' },
        { status: 401 }
      )
    }

    const { searchParams } = new URL(request.url)
    const keyId = searchParams.get('id')

    if (!keyId) {
      return NextResponse.json(
        { message: 'API key ID is required' },
        { status: 400 }
      )
    }

    const apiKey = await prisma.apiKey.findUnique({
      where: { id: keyId }
    })

    if (!apiKey || apiKey.userId !== session.user.id) {
      return NextResponse.json(
        { message: 'API key not found' },
        { status: 404 }
      )
    }

    await prisma.apiKey.delete({
      where: { id: keyId }
    })

    return NextResponse.json({ message: 'API key deleted successfully' })

  } catch (error) {
    console.error('API key deletion error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 