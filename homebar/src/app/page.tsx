// src/app/page.tsx
import Link from 'next/link'


export default function Page() {
return (
<div className="grid gap-6">
<h1 className="text-3xl font-bold">HomeBar</h1>
<p>בחר מה יש לך בבית וקבל קוקטיילים מותאמים אליך.</p>
<div className="flex gap-3">
<Link className="px-4 py-2 rounded-xl bg-black text-white" href="/discover">למציאת קוקטייל</Link>
<Link className="px-4 py-2 rounded-xl bg-white border" href="/pantry">לעדכון הפאנטרי</Link>
</div>
</div>
)
}