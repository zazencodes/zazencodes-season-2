# News Data MCP Website

A Next.js web application for the News Data MCP service, allowing developers to subscribe to news data endpoints for their LLM applications via the Model Context Protocol.

## Features

- **Landing Page**: Marketing site with hero section, features, and pricing tiers
- **Authentication**: Email/password authentication with NextAuth.js + role-based access control
- **User Dashboard**: API key management, usage tracking, and token monitoring
- **Route Explorer**: Interactive documentation of MCP tools and endpoints
- **Settings**: Account management, data export, and GDPR compliance
- **Admin Panel**: Full admin dashboard with user management, metrics, and system monitoring
- **Security**: Middleware-protected routes, bcrypt password hashing, secure session management

## Tech Stack

- **Frontend**: Next.js 14 (App Router), React, TypeScript, Tailwind CSS
- **Authentication**: NextAuth.js with credentials provider
- **Database**: SQLite with Prisma ORM
- **Charts**: Recharts for usage visualization
- **State Management**: React Query + Zustand
- **UI Icons**: Lucide React

## Quick Start

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd news-data-mcp-website
   npm install
   ```

2. **Create environment file:**
   ```bash
   # Copy the example environment file
   cp .env.example .env.local
   
   # Generate a secure NextAuth secret
   openssl rand -base64 32
   # OR: node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
   
   # Edit .env.local and replace NEXTAUTH_SECRET with the generated value
   ```

3. **Set up the database:**
   ```bash
   npx prisma generate
   npx prisma db push
   npx prisma db seed
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Test Accounts

The application comes pre-seeded with test accounts:

- **Admin**: `admin@newsdatamcp.com` / `admin123`
- **User**: `user@example.com` / `user123`

### Admin Panel Access

Admin users can access the admin panel at `/admin` which includes:
- **Dashboard**: System metrics, user analytics, and revenue tracking
- **User Management**: Full CRUD operations on user accounts, plan management, token resets
- **Settings**: System status monitoring and maintenance controls

## Available MCP Tools

The application showcases four main MCP tools:

1. **`search_articles`** - Search for news articles with filters
2. **`get_article`** - Retrieve full article content by ID
3. **`get_facts_about`** - Get verified facts about entities
4. **`get_latest_news`** - Get recent news articles by topic

## Project Structure

```
├── app/                    # Next.js app directory
│   ├── admin/             # Admin panel (role-protected)
│   ├── api/               # API routes
│   ├── auth/              # Authentication pages
│   ├── dashboard/         # User dashboard
│   ├── explorer/          # Route explorer
│   ├── settings/          # User settings
│   └── layout.tsx         # Root layout
├── lib/                   # Utility libraries
│   ├── auth.ts           # NextAuth configuration
│   ├── prisma.ts         # Prisma client
│   └── utils.ts          # Helper functions
├── prisma/               # Database schema and migrations
│   ├── schema.prisma     # Database schema
│   └── seed.ts           # Seed script
├── types/                # TypeScript type definitions
└── components/           # Reusable components (planned)
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/[...nextauth]` - NextAuth handlers

### User Management
- `GET /api/user/profile` - Get user profile
- `PATCH /api/user/profile` - Update user profile
- `DELETE /api/user/profile` - Delete user account
- `GET /api/user/export` - Export user data
- `POST /api/user/api-keys` - Create new API key
- `DELETE /api/user/api-keys` - Delete API key

### Admin Management
- `GET /api/admin/stats` - Get system statistics and metrics
- `GET /api/admin/users` - List all users with admin view
- `PATCH /api/admin/users/[id]` - Update any user account
- `DELETE /api/admin/users/[id]` - Delete any user account
- `POST /api/admin/users/[id]/reset-tokens` - Reset user token usage

## Development

### Database Commands

```bash
# Generate Prisma client
npx prisma generate

# Push schema changes to database
npx prisma db push

# Seed database with test data
npx prisma db seed

# Open Prisma Studio
npx prisma studio
```

### Environment Variables

Copy `.env.example` to `.env.local` and configure. You **must** generate a secure `NEXTAUTH_SECRET`:

```bash
# Generate a secure secret
openssl rand -base64 32

# Or using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

Then update `.env.local`:

```env
DATABASE_URL="file:./dev.db"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-generated-secret-here"
```

**Important**: Never commit your actual secrets to version control!

## Deployment

The application is designed to run with zero configuration. For production:

1. Set proper environment variables
2. Configure OAuth providers (optional)
3. Set up Stripe for payments (optional)
4. Deploy to your preferred platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open a GitHub issue or contact the development team. 