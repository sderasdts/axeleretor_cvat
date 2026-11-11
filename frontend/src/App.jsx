import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Cameras from './pages/Cameras'
import Journal from './pages/Journal'

const PAGES = { dashboard: Dashboard, cameras: Cameras, journal: Journal }

export default function App() {
  const [page, setPage] = useState('dashboard')
  const Page = PAGES[page] ?? Dashboard // остальные разделы пока ведут на дашборд

  return (
    <div className="flex min-h-screen">
      <Sidebar active={page} onNavigate={setPage} />
      <main className="flex min-w-0 flex-1 flex-col gap-5 px-7 py-6">
        <Page />
      </main>
    </div>
  )
}

