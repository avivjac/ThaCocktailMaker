// src/app/api/match/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { filterByIngredient, searchByName } from '@/lib/cocktaildb'

export const dynamic = 'force-dynamic' // למנוע קאשינג של Next ב־dev

// מיפוי מילים נפוצות בעברית לבסיסים באנגלית
const he2en: Record<string, string> = {
  'וודקה': 'vodka',
  'ג׳ין': 'gin',
  'גין': 'gin',
  'רום': 'rum',
  'טקילה': 'tequila',
  'וויסקי': 'whisky',
  'ויסקי': 'whisky',
  'ליים': 'lime',
  'לימון': 'lemon',
  'פסיפלורה': 'passionfruit',
}

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url)
    let q = (searchParams.get('q') ?? '').trim()
    if (!q) return NextResponse.json({ drinks: [], note: 'empty query' })

    // נרמל מילים בעברית
    if (he2en[q]) q = he2en[q]

    // 1) חיפוש לפי שם
    let drinks = await searchByName(q)

    // 2) אם אין תוצאות ולמילה אחת – נסה לפי מרכיב
    if ((!drinks || drinks.length === 0) && q.split(/\s+/).length === 1) {
      drinks = await filterByIngredient(q)
    }

    return NextResponse.json({ drinks: Array.isArray(drinks) ? drinks : [], q })
  } catch (err: any) {
    console.error('MATCH API ERROR:', err?.message || err)
    return NextResponse.json({ drinks: [], error: 'server_error' }, { status: 500 })
  }
}
