// src/components/AuthProvider.tsx
'use client'

import { supabase } from '@/lib/supabaseClient'
import { createContext, useContext, useEffect, useState, ReactNode } from 'react'

type AuthCtx = {
  user: any | null
  loading: boolean
  signOut: () => Promise<void>
}

const Ctx = createContext<AuthCtx>({
  user: null,
  loading: true,
  signOut: async () => {}
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    supabase.auth.getUser().then(({ data }) => {
      if (!mounted) return
      setUser(data.user ?? null)
      setLoading(false)
    })
    const { data: sub } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })
    return () => { mounted = false; sub.subscription.unsubscribe() }
  }, [])

  async function signOut() {
    await supabase.auth.signOut()
  }

  return (
    <Ctx.Provider value={{ user, loading, signOut }}>
      {children}
    </Ctx.Provider>
  )
}

export const useAuth = () => useContext(Ctx)