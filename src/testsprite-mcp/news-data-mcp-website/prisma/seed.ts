import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 Starting database seed...')

  // Create test admin user
  const adminPassword = await bcrypt.hash('admin123', 12)
  const admin = await prisma.user.upsert({
    where: { email: 'admin@newsdatamcp.com' },
    update: {},
    create: {
      email: 'admin@newsdatamcp.com',
      name: 'Admin User',
      password: adminPassword,
      role: 'ADMIN',
      plan: 'YEARLY',
      tokenLimit: 1000000,
      tokensUsed: 5000,
      apiKeys: {
        create: {
          key: 'mcp_admin_key_123456789abcdef',
          name: 'Admin API Key'
        }
      }
    }
  })

  // Create test regular user
  const userPassword = await bcrypt.hash('user123', 12)
  const user = await prisma.user.upsert({
    where: { email: 'user@example.com' },
    update: {},
    create: {
      email: 'user@example.com',
      name: 'Test User',
      password: userPassword,
      role: 'USER',
      plan: 'MONTHLY',
      tokenLimit: 100000,
      tokensUsed: 2500,
      apiKeys: {
        create: [
          {
            key: 'mcp_user_key_abcdef123456789',
            name: 'Default API Key'
          },
          {
            key: 'mcp_user_key_fedcba987654321',
            name: 'Development Key'
          }
        ]
      }
    }
  })

  // Create some usage records for the test user
  const usageRecords = await prisma.usageRecord.createMany({
    data: [
      {
        userId: user.id,
        tokens: 150,
        endpoint: 'search_articles',
        createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) // 1 week ago
      },
      {
        userId: user.id,
        tokens: 200,
        endpoint: 'get_article',
        createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000) // 5 days ago
      },
      {
        userId: user.id,
        tokens: 120,
        endpoint: 'get_facts_about',
        createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000) // 3 days ago
      },
      {
        userId: user.id,
        tokens: 180,
        endpoint: 'get_latest_news',
        createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000) // 1 day ago
      }
    ]
  })

  console.log('✅ Database seeded successfully!')
  console.log(`Created admin user: ${admin.email}`)
  console.log(`Created test user: ${user.email}`)
  console.log('Login credentials:')
  console.log('  Admin: admin@newsdatamcp.com / admin123')
  console.log('  User: user@example.com / user123')
}

main()
  .catch((e) => {
    console.error('❌ Error seeding database:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  }) 