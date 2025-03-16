import './App.css'
import ApplicationsPage from './pages/Applications'
import HomePage from './pages/Home'

import {BrowserRouter as Router, Routes, Route} from "react-router-dom"

function App() {

  return ( 
      <Router>
        <Routes>
          <Route index element={<HomePage />} />
          <Route path='apps'  element={<ApplicationsPage />} />
        </Routes>
      </Router>  
  )
}

export default App
