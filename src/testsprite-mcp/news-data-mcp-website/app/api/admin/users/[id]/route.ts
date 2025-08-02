import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function PATCH(
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

    const { name, email, role, plan, tokenLimit } = await request.json()

    if (!name || !email || !role || !plan || typeof tokenLimit !== 'number') {
      return NextResponse.json(
        { message: 'All fields are required' },
        { status: 400 }
      )
    }

    // Check if email is already taken by another user
    const existingUser = await prisma.user.findFirst({
      where: {
        email,
        NOT: { id: params.id }
      }
    })

    if (existingUser) {
      return NextResponse.json(
        { message: 'Email is already taken' },
        { status: 400 }
      )
    }

    const updatedUser = await prisma.user.update({
      where: { id: params.id },
      data: { name, email, role, plan, tokenLimit },
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

    return NextResponse.json(userWithoutPassword)

  } catch (error) {
    console.error('Admin user update error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function DELETE(
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

    // Prevent admin from deleting themselves
    if (params.id === session.user.id) {
      return NextResponse.json(
        { message: 'Cannot delete your own account' },
        { status: 400 }
      )
    }

    // Delete user and all related data (cascading deletes handled by Prisma)
    await prisma.user.delete({
      where: { id: params.id }
    })

    return NextResponse.json({ message: 'User deleted successfully' })

  } catch (error) {
    console.error('Admin user deletion error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 