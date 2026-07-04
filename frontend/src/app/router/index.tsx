import { BrowserRouter, Routes, Route } from "react-router-dom";

function Landing() {
  return <h1 className="text-white text-4xl">Landing Page</h1>;
}

function Workspace() {
  return <h1 className="text-white text-4xl">Workspace</h1>;
}

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/workspace" element={<Workspace />} />
      </Routes>
    </BrowserRouter>
  );
}