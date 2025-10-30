import { supabase } from '@/lib/supabaseClient'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

async function getAccessToken() {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token || null
}

export async function apiGet<T = any>(path: string): Promise<T> {
  const token = await getAccessToken()
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: token ? `Bearer ${token}` : '' },
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<T>
}

export async function apiPut<T = any>(path: string, body: unknown): Promise<T> {
  const token = await getAccessToken()
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'PUT',
    headers: {
      Authorization: token ? `Bearer ${token}` : '',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<T>
}
