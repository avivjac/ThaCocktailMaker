// src/app/api/pantry/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSupabase } from '@/lib/serverSupabase'


export async function GET() {
const supabase = getServerSupabase()
const { data: { user } } = await supabase.auth.getUser()
if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
const { data, error } = await supabase.from('user_pantry').select('ingredient_id, has')
if (error) return NextResponse.json({ error: error.message }, { status: 500 })
return NextResponse.json({ pantry: data })
}


export async function PUT(req: NextRequest) {
const supabase = getServerSupabase()
const { data: { user } } = await supabase.auth.getUser()
if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
const body = await req.json()
// body = [{ ingredient_id, has }]
const rows = (body ?? []).map((r: any) => ({ ...r, user_id: user.id }))
const { error } = await supabase.from('user_pantry').upsert(rows, { onConflict: 'user_id,ingredient_id' })
if (error) return NextResponse.json({ error: error.message }, { status: 500 })
return NextResponse.json({ ok: true })
}