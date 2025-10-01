// src/app/discover/page.tsx
'use client'
import { useState } from 'react'


export default function Discover() {
const [q, setQ] = useState('margarita')
const [results, setResults] = useState<any[]>([])
const [loading, setLoading] = useState(false)
const [note, setNote] = useState<string | null>(null)

// search the specific cocktail through the API
async function search() {
  setLoading(true)
  setNote(null)
  try {
    const res = await fetch(`/api/match?q=${encodeURIComponent(q)}`, { cache: 'no-store' })
    const json = await res.json()
    console.log('API response', json)
    if (json.error) setNote('אירעה שגיאה בשרת')
    if (json.note) setNote(json.note)
    setResults(Array.isArray(json.drinks) ? json.drinks : [])
  } catch (e) {
    console.error(e)
    setNote('לא ניתן לשלוף נתונים מה־API')
    setResults([])
  } finally {
    setLoading(false)
  }
}



return (
<div className="grid gap-4">
    <h1 className="text-2xl font-bold">מצא קוקטייל</h1>
    <div className="flex gap-2">
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search by name or ingredient"
            className="border rounded p-2 flex-1" />
        <button onClick={search} className="px-4 py-2 rounded bg-black text-white">Search</button>
    </div>
{loading && <p>Loading...</p>}

{!loading && results.length === 0 && ( 
  <p className="opacity-70">
    לא נמצאו תוצאות. נסה שם באנגלית (למשל: <code>margarita</code>) או בסיס כמו <code>gin</code>/<code>whisky</code>.
  </p>
)}

<div className="grid md:grid-cols-3 gap-4">
    {results.map((d) => (
    <div key={d.idDrink} className="rounded-xl border bg-white overflow-hidden">
    <img src={d.strDrinkThumb} alt={d.strDrink} className="w-full aspect-video object-cover" />
    <div className="p-3">
        <div className="font-semibold">{d.strDrink}</div>
            <div className="text-sm opacity-70">#{d.idDrink}</div>
        </div>
    </div>
    ))}
</div>
</div>
)
}