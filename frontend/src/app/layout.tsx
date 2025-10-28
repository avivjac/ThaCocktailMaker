// src/app/layout.tsx
import './globals.css'
import { ReactNode } from 'react'
import { AuthProvider } from '@/components/AuthProvider'
import NavBar from '@/components/NavBar'

export const metadata = { title: 'HomeBar — Auth', description: 'Supabase Auth starter' }

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-neutral-50 text-neutral-900">
        <AuthProvider>
          <NavBar />
          <main className="max-w-4xl mx-auto p-4">{children}</main>
        </AuthProvider>
      </body>
    </html>
  )
}
