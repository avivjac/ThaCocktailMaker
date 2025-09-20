// src/app/api/match/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { filterByIngredient, searchByName } from '@/lib/cocktailDB'


export async function GET(req: NextRequest) {
const { searchParams } = new URL(req.url)
const q = (searchParams.get('q') ?? '').trim()
if (!q) return NextResponse.json({ drinks: [] })


// Heuristic: if single word & likely ingredient → use filter; else search by name
const isIngredient = q.split(/\s+/).length === 1
const drinks = isIngredient ? await filterByIngredient(q) : await searchByName(q)
return NextResponse.json({ drinks })
}