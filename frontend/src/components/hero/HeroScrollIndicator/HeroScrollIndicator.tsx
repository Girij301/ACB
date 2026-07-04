import { useEffect, useState } from "react";
import { ChevronDown } from "lucide-react";

import { cn } from "@/lib";

import { heroScrollIndicatorVariants } from "./heroScrollIndicatorVariants";

interface HeroScrollIndicatorProps {
  className?: string;
}

export function HeroScrollIndicator({
  className,
}: HeroScrollIndicatorProps) {
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    function handleScroll() {
      setHidden(window.scrollY > 40);
    }

    window.addEventListener("scroll", handleScroll);

    return () =>
      window.removeEventListener("scroll", handleScroll);
  }, []);

  function handleClick() {
    document
      .getElementById("capabilities")
      ?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className={cn(
        heroScrollIndicatorVariants(),
        "transition-all duration-500",
        hidden
          ? "translate-y-4 opacity-0 pointer-events-none"
          : "translate-y-0 opacity-100",
        className
      )}
    >
      <span className="text-xs uppercase tracking-[0.35em] text-white/40">
        Scroll
      </span>

      <ChevronDown
        size={18}
        className="animate-bounce text-cyan-400"
      />
    </button>
  );
}