import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import RootLayout from "./components/layout/RootLayout.tsx";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/Home/index.tsx";
import ApplicationsPage from "./pages/Applications/index.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<RootLayout />}>
          <Route index element={<HomePage />} />
          <Route path="apps" element={<ApplicationsPage />} />
        </Route>
      </Routes>
    </Router>
  </StrictMode>
);
