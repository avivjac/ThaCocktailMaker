'use client'

import { useAuth } from '@/components/AuthProvider'
import { apiGet, apiPut } from '@/lib/api'
import { useEffect, useState } from 'react'

type PantryRow = {
  id: number
  ingredient_id: number | null
  custom_name: string | null
  has: boolean
  amount_ml: number | null
}

export default function PantryPage() {
  const { user, loading } = useAuth()
  const [pantry, setPantry] = useState<PantryRow[]>([])
  const [customName, setCustomName] = useState('')
  const [ingredientId, setIngredientId] = useState<string>('') // אופציונלי
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!loading && user) fetchPantry()
  }, [loading, user])

  async function fetchPantry() {
    try {
      const data = await apiGet<{ pantry: PantryRow[] }>('/pantry')
      setPantry(data.pantry || [])
    } catch (e: any) {
      setError(e.message || 'Load failed')
    }
  }

  async function addOrUpdate() {
    setBusy(true); setError(null)
    try {
      const payload = [
        ingredientId
          ? { ingredient_id: Number(ingredientId), has: true }
          : { custom_name: customName, has: true }
      ]
      await apiPut('/pantry', payload)
      setCustomName(''); setIngredientId('')
      await fetchPantry()
    } catch (e: any) {
      setError(e.message || 'Save failed')
    } finally {
      setBusy(false)
    }
  }

  if (loading) return <p>Loading...</p>
  if (!user) return <p>אנא התחבר/י כדי לגשת ל־Pantry.</p>

  return (
    <div className="grid gap-4">
      <h1 className="text-2xl font-bold">My Pantry</h1>

      <div className="grid md:grid-cols-2 gap-3 items-end">
        <div className="grid gap-1">
          <label className="text-sm">Custom name</label>
          <input
            className="border p-2 rounded"
            placeholder="Monin Passionfruit"
            value={customName}
            onChange={(e) => setCustomName(e.target.value)}
          />
        </div>
        <div className="grid gap-1">
          <label className="text-sm">Ingredient ID (optional)</label>
          <input
            className="border p-2 rounded"
            placeholder="e.g. 1"
            value={ingredientId}
            onChange={(e) => setIngredientId(e.target.value)}
          />
        </div>
        <button
          onClick={addOrUpdate}
          disabled={busy}
          className="bg-black text-white rounded p-2"
        >
          {busy ? 'Saving…' : 'Add / Upsert'}
        </button>
      </div>

      {error && <p className="text-red-600 text-sm">{error}</p>}

      <div className="grid gap-2">
        {pantry.length === 0 && <p className="opacity-70">אין פריטים עדיין.</p>}
        {pantry.map((row) => (
          <div key={row.id} className="border rounded p-2 bg-white">
            <div className="font-medium">
              {row.custom_name || `Ingredient #${row.ingredient_id}`}
            </div>
            <div className="text-xs opacity-70">
              has: {String(row.has)}{row.amount_ml ? ` • ${row.amount_ml} ml` : ''}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
