import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function generateApiKey(): string {
  return 'mcp_' + Math.random().toString(36).substring(2) + Math.random().toString(36).substring(2)
} 