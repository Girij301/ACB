import { SignUp } from "@clerk/clerk-react";

export function SignUpPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-black">
      <SignUp />
    </main>
  );
}