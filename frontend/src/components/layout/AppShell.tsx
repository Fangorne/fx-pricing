import { Outlet, useLocation } from 'react-router-dom'
import { Sidebar } from './Sidebar'

export function AppShell() {
  const { pathname } = useLocation()
  return (
    <div className="flex h-screen overflow-hidden bg-bg-base">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <div key={pathname} className="animate-[fadeIn_150ms_ease-out]">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
