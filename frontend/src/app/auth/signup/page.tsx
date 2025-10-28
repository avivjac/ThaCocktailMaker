// src/app/auth/signup/page.tsx
'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabaseClient'

export default function SignUp() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null); setMsg(null)
    const { error } = await supabase.auth.signUp({ email, password })
    if (error) return setError(error.message)
    setMsg('Check your email to confirm your account, then sign in.')
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-3 max-w-sm">
      <h1 className="text-xl font-semibold">Create account</h1>
      <input className="border p-2 rounded" placeholder="Email"
             value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="border p-2 rounded" type="password" placeholder="Password"
             value={password} onChange={e=>setPassword(e.target.value)} />
      <button className="bg-black text-white rounded p-2">Sign up</button>
      {msg && <p className="text-green-700 text-sm">{msg}</p>}
      {error && <p className="text-red-600 text-sm">{error}</p>}
    </form>
  )
}
