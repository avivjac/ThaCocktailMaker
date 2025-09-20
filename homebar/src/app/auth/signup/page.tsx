// src/app/(auth)/signup/page.tsx
'use client'
import { z } from 'zod'
import { useState } from 'react'
import { supabase } from '@/lib/supabaseClient'


const schema = z.object({ email: z.string().email(), password: z.string().min(6) })


export default function SignUp() {
const [error, setError] = useState<string | null>(null)
const [msg, setMsg] = useState<string | null>(null)
async function onSubmit(formData: FormData) {
setError(null); setMsg(null)
const obj = { email: String(formData.get('email')), password: String(formData.get('password')) }
const parsed = schema.safeParse(obj)
if (!parsed.success) return setError('Invalid input')
const { error } = await supabase.auth.signUp(parsed.data)
if (error) return setError(error.message)
setMsg('Check your email to confirm. Once verified, sign in!')
}
return (
<form action={onSubmit} className="grid gap-3 max-w-sm">
<h1 className="text-2xl font-bold">Create account</h1>
<input name="email" placeholder="Email" className="border p-2 rounded" />
<input name="password" type="password" placeholder="Password" className="border p-2 rounded" />
<button className="bg-black text-white rounded p-2">Sign up</button>
{msg && <p className="text-green-700">{msg}</p>}
{error && <p className="text-red-600">{error}</p>}
</form>
)
}