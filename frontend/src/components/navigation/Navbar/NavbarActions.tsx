import { Link } from "react-router-dom";
import { UserButton, useAuth } from "@clerk/clerk-react";

import { Button } from "@/components/ui";
import { cn } from "@/lib";

interface NavbarActionsProps {
  className?: string;
}

export function NavbarActions({ className }: NavbarActionsProps) {
  const { isSignedIn } = useAuth();

  return (
    <div className={cn("flex items-center gap-3", className)}>
      {!isSignedIn ? (
        <>
          <Link to="/sign-in">
            <Button
              variant="ghost"
              size="sm"
              className="
                glass-hover
              hover:text-white
                "
            >
              Sign In
            </Button>
          </Link>

          <Link to="/sign-in">
            <Button variant="glass" size="sm">
              Get Started
            </Button>
          </Link>
        </>
      ) : (
        <>
          <Link to="/workspace">
            <Button variant="glass" size="sm">
              Workspace
            </Button>
          </Link>

          <UserButton
            appearance={{
              elements: {
                avatarBox:
                  "w-10 h-10 ring-1 ring-white/10 hover:ring-white/20 transition-all",
              },
            }}
          />
        </>
      )}
    </div>
  );
}
