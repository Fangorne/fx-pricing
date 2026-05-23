import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import { ConventionsPage } from '@/features/conventions/ConventionsPage'
import { CalendarPage } from '@/features/calendars/CalendarPage'
import { SpotCalculatorPage } from '@/features/dates/SpotCalculatorPage'

function Home() {
  return (
    <div className="p-6">
      <div className="rounded-lg bg-blue-500 p-4 text-white">
        <p>FX Pricing Platform — ready</p>
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-950 text-gray-100">
        <header className="border-b border-gray-800 px-6 py-4">
          <div className="flex items-center gap-6">
            <Link to="/" className="text-xl font-semibold text-blue-400 hover:text-blue-300">
              FX Pricing
            </Link>
            <nav className="flex gap-4 text-sm">
              <Link
                to="/conventions"
                className="text-gray-400 hover:text-gray-100 transition-colors"
              >
                Conventions
              </Link>
              <Link to="/calendars" className="text-gray-400 hover:text-gray-100 transition-colors">
                Calendriers
              </Link>
              <Link to="/dates" className="text-gray-400 hover:text-gray-100 transition-colors">
                Calculateur
              </Link>
            </nav>
          </div>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/conventions" element={<ConventionsPage />} />
            <Route path="/conventions/:pair" element={<ConventionsPage />} />
            <Route path="/calendars" element={<CalendarPage />} />
            <Route path="/dates" element={<SpotCalculatorPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
