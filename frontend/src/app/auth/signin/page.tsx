// src/app/auth/signin/page.tsx
'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabaseClient'
import { useRouter } from 'next/navigation'

export default function SignIn() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) return setError(error.message)
    router.push('/pantry') // אחרי התחברות – נעבור לפאנטרי/עמוד מוגן
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-3 max-w-sm">
      <h1 className="text-xl font-semibold">Sign in</h1>
      <input className="border p-2 rounded" placeholder="Email"
             value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="border p-2 rounded" type="password" placeholder="Password"
             value={password} onChange={e=>setPassword(e.target.value)} />
      <button className="bg-black text-white rounded p-2">Sign in</button>
      {error && <p className="text-red-600 text-sm">{error}</p>}
    </form>
  )
}
