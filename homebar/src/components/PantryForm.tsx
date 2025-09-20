// src/components/PantryForm.tsx
'use client'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabaseClient'


type PantryItem = { id: number; name: string; has: boolean }


export default function PantryForm() {
const [items, setItems] = useState<PantryItem[]>([])
const [loading, setLoading] = useState(true)


useEffect(() => {
(async () => {
// For demo: seed a few common items into ingredients table if empty (serverless would be better)
const { data: ing } = await supabase.from('ingredients').select('id,name').limit(200)
const list: PantryItem[] = (ing ?? []).map((x) => ({ id: x.id, name: x.name as string, has: false }))
setItems(list); setLoading(false)
})()
}, [])


async function toggle(id: number, name: string, has: boolean) {
const user = (await supabase.auth.getUser()).data.user
if (!user) return alert('Sign in first')
const payload = { user_id: user.id, ingredient_id: id, has: !has }
await supabase.from('user_pantry').upsert(payload, { onConflict: 'user_id,ingredient_id' })
setItems((prev) => prev.map((p) => (p.id === id ? { ...p, has: !has } : p)))
}


if (loading) return <p>Loading...</p>


return (
<div className="grid gap-2">
{items.map((it) => (
<label key={it.id} className="flex gap-2 items-center">
<input type="checkbox" checked={it.has} onChange={() => toggle(it.id, it.name, it.has)} />
<span>{it.name}</span>
</label>
))}
</div>
)
}