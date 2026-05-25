import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AppShell } from '@/components/layout'
import { ConventionsPage } from '@/features/conventions/ConventionsPage'
import { CalendarPage } from '@/features/calendars/CalendarPage'
import { SpotCalculatorPage } from '@/features/dates/SpotCalculatorPage'
import { HomePage } from '@/features/home/HomePage'
import { DesignSystemPage } from '@/pages/DesignSystemPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/conventions" element={<ConventionsPage />} />
          <Route path="/calendars" element={<CalendarPage />} />
          <Route path="/dates" element={<SpotCalculatorPage />} />
          <Route path="/design-system" element={<DesignSystemPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
