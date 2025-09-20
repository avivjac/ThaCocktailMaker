// src/app/(auth)/signin/page.tsx
'use client'
import { z } from 'zod'
import { useState } from 'react'
import { supabase } from '@/lib/supabaseClient'


const schema = z.object({ email: z.string().email(), password: z.string().min(6) })


export default function SignIn() {
const [error, setError] = useState<string | null>(null)
async function onSubmit(formData: FormData) {
setError(null)
const obj = { email: String(formData.get('email')), password: String(formData.get('password')) }
const parsed = schema.safeParse(obj)
if (!parsed.success) return setError('Invalid credentials')
const { data, error } = await supabase.auth.signInWithPassword(parsed.data)
if (error) return setError(error.message)
location.href = '/discover'
}
return (
<form action={onSubmit} className="grid gap-3 max-w-sm">
<h1 className="text-2xl font-bold">Sign in</h1>
<input name="email" placeholder="Email" className="border p-2 rounded" />
<input name="password" type="password" placeholder="Password" className="border p-2 rounded" />
<button className="bg-black text-white rounded p-2">Sign in</button>
{error && <p className="text-red-600">{error}</p>}
</form>
)
}