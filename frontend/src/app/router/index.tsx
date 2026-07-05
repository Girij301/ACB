import { BrowserRouter, Route, Routes } from "react-router-dom";

import { ProtectedRoute } from "@/auth";

import {
  LandingPage,
  SignInPage,
  SignUpPage,
  WorkspacePage,
} from "@/pages";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route path="/sign-in/*" element={<SignInPage />} />

        <Route path="/sign-up/*" element={<SignUpPage />} />

        <Route
          path="/workspace"
          element={
            <ProtectedRoute>
              <WorkspacePage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}