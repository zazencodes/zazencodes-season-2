# Product Requirements Document (PRD)

## 1. Overview

Build a **Next.js (React)** web app that lets developers subscribe to **News Data MCP** and retrieve fresh news articles for LLMs via their own **Model Context Protocol** endpoints. This PRD covers **the customer-facing frontend and its companion backend only** (the MCP data service itself is a separate product). The site must run end-to-end on a single laptop with one command (`npm dev`) and zero manual configuration.

## 2. User Stories

### 2.1 Visitor

* I can read a product pitch, compare plans, and sign up.

### 2.2 User

* I can create an account with email + password or OAuth (Google/GitHub) and magic-link login.
* I can view my plan, generate an MCP API key, monthly token allowance, and real-time usage.
* I can explore news "routes" (pre-built topic/feed endpoints) with search & filters.
* I can upgrade, downgrade, or cancel my subscription.
* I can change my email, export my data, or delete my account (GDPR).

### 2.3 Admin

* I can see high-level metrics (MRR, active users, total tokens served).
* I can view, suspend, or delete any user and adjust token allowances.

## 3. Functional Requirements

### 3.1 Authentication

* Email/password (bcrypt) - test database for initial demo version
* OAuth 2.0 (Google, GitHub) - not required for initial demo version
* Magic-link (one-time JWT) - not required for initial demo version

### 3.2 Marketing / Landing

* Hero pitch, feature grid, 3-tier pricing (Free, Monthly, Yearly)
* "Get API Key" CTA → Auth flow

### 3.3 Dashboard (auth-protected)

* Welcome banner: current plan, MCP API key (generate once then hidden, can generate multiple, copy button), monthly quota vs. used
* Token-usage chart: backend fetches `/usage?period=month` from the separate MCP Admin API and streams to frontend (Recharts)
* Quick-links: "Explore Routes", "Upgrade Plan", "Docs"

### 3.4 Route Explorer

- Lists MCP tools:

    1. **`search_articles`**
       - Parameters: query (string), date_range (optional), limit (optional)
       - Returns: List of relevant articles with metadata (title, summary, date, source, relevance_score)

    2. **`get_article`**
       - Parameters: article_id (string)
       - Returns: Full article content with structured metadata (facts, entities, sources)

    3. **`get_facts_about`**
       - Parameters: entity/topic (string), fact_type (optional)
       - Returns: Verified facts about a person, organization, event, or topic with source citations

    4. **`get_latest_news`**
       - Parameters: topic (optional), count (optional)
       - Returns: Most recent articles, optionally filtered by topic

### 3.5 Subscription / Billing

* Stripe via Checkout for subscribe/upgrade/downgrade/cancel - test database for initial demo version
* Stripe webhooks hit local backend to sync user plans and token limits - not required for initial demo version

### 3.6 Settings

* Change email (re-verify)
* Export personal data (JSON download)
* Delete account → cascade delete in local DB + Stripe (30-day grace) - not required for initial demo version

### 3.7 Admin Panel

* Metrics dashboard (tokens/day, revenue, new users)
* User table with CRUD, plan override, manual token reset

## 4. Non-Functional Requirements

- Starts Next.js on http://localhost:3000, spins up SQLite via Prisma, seeds test data.*
* Responsive (mobile-first Tailwind)
* Dark-mode support (automatic via `prefers-color-scheme` + manual toggle)
* Server-Side Rendering (SSR) & Incremental Static Regeneration (ISR) for SEO
* Secure cookies (`httponly`, `secure`, `samesite=lax`) for JWTs


## 5. Technical Stack

| Layer                      | Choice                                                      | Notes                                                          |
| -------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| **Frontend**               | Next.js (App Router), React, TypeScript, Tailwind CSS | The only server to run is `next dev`                           |
| **State / Data**           | React Query + Zustand                                       | Handles dashboard & explorer data                              |
| **Charts**                 | Recharts                                                    | Used for token-usage visualization                             |
| **Auth**                   | NextAuth.js (Email, Google, GitHub providers)               | Magic-link via email provider - not required for initial demo                                  |
| **Payments**               | Stripe                                        |  not required for initial demo     |
| **Backend** | Next.js API routes (Node)                                | Proxies Admin API, CRUD for users |
| **Database**               | SQLite (file-based) via Prisma ORM                          | Auto-migrates & seeds on first run; no external DB needed      |
| **Admin UI**               | Route group `/admin` with role-based guard                  | Uses same Next.js instance                                     |


