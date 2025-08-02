import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id || session.user.role !== 'ADMIN') {
      return NextResponse.json(
        { message: 'Unauthorized' },
        { status: 401 }
      )
    }

    // Reset user's token usage to 0
    const updatedUser = await prisma.user.update({
      where: { id: params.id },
      data: { tokensUsed: 0 },
      include: {
        _count: {
          select: {
            apiKeys: true,
            usageRecords: true
          }
        }
      }
    })

    // Remove password from response
    const { password, ...userWithoutPassword } = updatedUser

    return NextResponse.json({
      message: 'User tokens reset successfully',
      user: userWithoutPassword
    })

  } catch (error) {
    console.error('Admin token reset error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 