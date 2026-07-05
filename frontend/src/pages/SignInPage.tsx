import { SignIn } from "@clerk/clerk-react";

export function SignInPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-black">
      <SignIn />
    </main>
  );
}