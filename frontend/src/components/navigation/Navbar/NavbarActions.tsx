import { Button } from "@/components/ui";
import { cn } from "@/lib";

interface NavbarActionsProps {
  className?: string;
}

export function NavbarActions({
  className,
}: NavbarActionsProps) {
  return (
    <div
      className={cn(
        "flex items-center gap-3",
        className
      )}
    >
      <Button variant="ghost" size="sm">
        Sign In
      </Button>

      <Button variant="glass" size="sm">
        Get Started
      </Button>
    </div>
  );
}