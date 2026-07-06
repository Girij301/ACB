import { cn } from "@/lib";

interface NavbarLinksProps {
  className?: string;
}

const links = [
  {
    label: "Capabilities",
    href: "#capabilities",
  },
  {
    label: "How It Works",
    href: "#documentation",
  },
  {
    label: "Get Started",
    href: "#cta",
  },
];

export function NavbarLinks({ className }: NavbarLinksProps) {
  return (
    <nav className={cn("hidden items-center gap-8 lg:flex", className)}>
      {links.map((link) => (
        <a
          key={link.label}
          href={link.href}
          className="
    group
    relative
    text-sm
    font-medium
    text-white/70
    transition-all
    duration-300
    hover:-translate-y-0.5
    hover:text-white
  "
        >
          {link.label}

          <span
            className="
      absolute
      -bottom-1
      left-0
      h-px
      w-0
      bg-cyan-400
      transition-all
      duration-300
      group-hover:w-full
    "
          />
        </a>
      ))}
    </nav>
  );
}
