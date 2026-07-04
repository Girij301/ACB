import { Button } from "@/components/ui";

interface HeroCTAProps {
  href?: string;
  children: React.ReactNode;
  primary?: boolean;
}

export function HeroCTA({
  children,
  primary = false,
}: HeroCTAProps) {
  return (
    <Button
      variant={primary ? "glass" : "ghost"}
      size="lg"
      className="
        group
        min-w-45
        transition-all
        duration-300
        hover:-translate-y-1
        hover:scale-[1.03]
      "
    >
      <span className="flex items-center gap-2">
        {children}

        <span
          className="
            transition-transform
            duration-300
            group-hover:translate-y-1
            hover:scale-[1.03]
          "
        >
          →
        </span>
      </span>
    </Button>
  );
}