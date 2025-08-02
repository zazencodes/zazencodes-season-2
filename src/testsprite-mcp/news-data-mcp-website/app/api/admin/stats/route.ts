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

    // Get user counts
    const totalUsers = await prisma.user.count()
    const activeUsers = await prisma.user.count({
      where: {
        usageRecords: {
          some: {
            createdAt: {
              gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) // Last 30 days
            }
          }
        }
      }
    })

    // Get new users this month
    const startOfMonth = new Date()
    startOfMonth.setDate(1)
    startOfMonth.setHours(0, 0, 0, 0)
    
    const newUsersThisMonth = await prisma.user.count({
      where: {
        createdAt: {
          gte: startOfMonth
        }
      }
    })

    // Get total tokens served
    const tokenStats = await prisma.usageRecord.aggregate({
      _sum: {
        tokens: true
      }
    })
    const totalTokens = tokenStats._sum.tokens || 0

    // Get users by plan
    const usersByPlan = await prisma.user.groupBy({
      by: ['plan'],
      _count: {
        id: true
      }
    })

    const planColors = {
      'FREE': '#6B7280',
      'MONTHLY': '#3B82F6',
      'YEARLY': '#10B981'
    }

    const formattedUsersByPlan = usersByPlan.map((plan: any) => ({
      name: plan.plan,
      value: plan._count.id,
      color: planColors[plan.plan as keyof typeof planColors] || '#6B7280'
    }))

    // Mock revenue data (in real app, would come from Stripe)
    const monthlyRevenue = usersByPlan.reduce((total: number, plan: any) => {
      const price = plan.plan === 'MONTHLY' ? 29 : plan.plan === 'YEARLY' ? 290 : 0
      return total + (plan._count.id * price)
    }, 0)

    // Get token usage for last 7 days
    const last7Days = Array.from({ length: 7 }, (_, i) => {
      const date = new Date()
      date.setDate(date.getDate() - i)
      return date
    }).reverse()

    const tokensUsageData = await Promise.all(
      last7Days.map(async (date) => {
        const startOfDay = new Date(date)
        startOfDay.setHours(0, 0, 0, 0)
        const endOfDay = new Date(date)
        endOfDay.setHours(23, 59, 59, 999)

        const dayUsage = await prisma.usageRecord.aggregate({
          where: {
            createdAt: {
              gte: startOfDay,
              lte: endOfDay
            }
          },
          _sum: {
            tokens: true
          }
        })

        return {
          name: date.toLocaleDateString('en-US', { weekday: 'short' }),
          tokens: dayUsage._sum.tokens || 0
        }
      })
    )

    // Mock revenue trend data (last 6 months)
    const revenueData = [
      { name: 'Jul', revenue: 12400 },
      { name: 'Aug', revenue: 15600 },
      { name: 'Sep', revenue: 18200 },
      { name: 'Oct', revenue: 22100 },
      { name: 'Nov', revenue: 26800 },
      { name: 'Dec', revenue: monthlyRevenue }
    ]

    const stats = {
      totalUsers,
      activeUsers,
      totalTokens,
      monthlyRevenue,
      newUsersThisMonth,
      usersByPlan: formattedUsersByPlan,
      tokensUsageData,
      revenueData
    }

    return NextResponse.json(stats)

  } catch (error) {
    console.error('Admin stats error:', error)
    return NextResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }
} 