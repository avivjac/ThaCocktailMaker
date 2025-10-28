// src/components/NavBar.tsx
'use client'

import Link from 'next/link'
import { useAuth } from '@/components/AuthProvider'

export default function NavBar() {
  const { user, signOut } = useAuth()

  return (
    <nav className="w-full border-b bg-white">
      <div className="max-w-4xl mx-auto p-3 flex items-center gap-4">
        <Link href="/" className="font-semibold">HomeBar</Link>
        <Link href="/auth/signin" className="ml-auto">Sign in</Link>
        <Link href="/auth/signup">Sign up</Link>
        <Link href="/pantry">Pantry</Link>
        {user && (
          <button onClick={signOut} className="border rounded px-2 py-1">Sign out</button>
        )}
      </div>
    </nav>
  )
}
