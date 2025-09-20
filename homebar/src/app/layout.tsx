import './globals.css'
import Navbar from '@/components/NavBar'
import { ReactNode } from 'react'


export const metadata = { title: 'HomeBar', description: 'Cocktails from your pantry' }


export default function RootLayout({ children }: { children: ReactNode }) {
return (
<html lang="en">
<body className="min-h-screen bg-neutral-50 text-neutral-900">
<Navbar />
<main className="max-w-5xl mx-auto p-4">{children}</main>
</body>
</html>
)
}