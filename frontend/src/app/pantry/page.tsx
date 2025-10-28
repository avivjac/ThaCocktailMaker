// src/app/pantry/page.tsx
import PantryForm from '@/components/PantryForm'
import { getServerSupabase } from '@/lib/serverSupabase'


export default async function PantryPage() {
const supabase = getServerSupabase()
const { data: { user } } = await supabase.auth.getUser()


return (
<div className="grid gap-4">
<h1 className="text-2xl font-bold">מה יש לי בבית</h1>
{!user && <p className="text-sm">כדי לשמור פאנטרי אישי, היכנס לחשבון.</p>}
<PantryForm />
</div>
)
}