import type { PropsWithChildren } from "react";
import { ClerkProvider } from "@clerk/clerk-react";

import { ApiProvider } from "@/services/api";

const publishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!publishableKey) {
  throw new Error(
    "Missing VITE_CLERK_PUBLISHABLE_KEY. Please check your frontend .env file."
  );
}

export function AppProviders({ children }: PropsWithChildren) {
  return (
    <ClerkProvider publishableKey={publishableKey}>
      <ApiProvider>
        {children}
      </ApiProvider>
    </ClerkProvider>
  );
}