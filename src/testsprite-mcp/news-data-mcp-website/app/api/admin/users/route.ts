import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id || session.user.role !== 'ADMIN') {
      return NextResponse.json(
        { message: 'Unauthorized' },
        { status: 401 }
      )
    }

    const users = await prisma.user.findMany({
      include: {
        _count: {
          select: {
            apiKeys: true,
            usageRecords: true
          }
        }
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    // Remove passwords from response
    const usersWithoutPasswords = users.map(({ password, ...user }: any) => user)

    return NextResponse.json(usersWithoutPasswords)

  } catch (error) {
    console.error('Admin users fetch error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 