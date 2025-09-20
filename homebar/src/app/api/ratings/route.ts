// src/app/api/ratings/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSupabase } from '@/lib/serverSupabase'


export async function POST(req: NextRequest) {
const supabase = getServerSupabase()
const { data: { user } } = await supabase.auth.getUser()
if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
const { cocktail_id, stars, liked, notes } = await req.json()
const { error } = await supabase.from('ratings').upsert({ user_id: user.id, cocktail_id, stars, liked, notes })
if (error) return NextResponse.json({ error: error.message }, { status: 500 })
return NextResponse.json({ ok: true })
}