// src/components/Navbar.tsx
'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { supabase } from '@/lib/supabaseClient'
import { useEffect, useState } from 'react'


export default function Navbar() {
const pathname = usePathname()
const [email, setEmail] = useState<string | null>(null)


useEffect(() => {
supabase.auth.getUser().then(({ data }) => setEmail(data.user?.email ?? null))
}, [pathname])


return (
<nav className="w-full border-b bg-white">
<div className="max-w-5xl mx-auto p-3 flex items-center gap-4">
<Link href="/" className="font-semibold">HomeBar</Link>
<Link href="/discover" className="ml-auto">Discover</Link>
<Link href="/pantry">Pantry</Link>
{email ? (
<button
className="px-3 py-1 rounded-lg border"
onClick={async () => { await supabase.auth.signOut(); location.href = '/' }}
>Sign out</button>
) : (
<Link className="px-3 py-1 rounded-lg border" href="/signin">Sign in</Link>
)}
</div>
</nav>
)
}