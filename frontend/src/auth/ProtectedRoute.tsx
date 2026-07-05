import type { PropsWithChildren } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@clerk/clerk-react";

export function ProtectedRoute({
  children,
}: PropsWithChildren) {
  const { isLoaded, isSignedIn } = useAuth();
  const location = useLocation();

  // Wait until Clerk finishes loading
  if (!isLoaded) {
    return null;
  }

  // Redirect unauthenticated users
  if (!isSignedIn) {
    return (
      <Navigate
        to="/sign-in"
        replace
        state={{ from: location }}
      />
    );
  }

  return <>{children}</>;
}