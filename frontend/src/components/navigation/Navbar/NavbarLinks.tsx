import { cn } from "@/lib";

interface NavbarLinksProps {
  className?: string;
}

const links = [
  {
    label: "Features",
    href: "#features",
  },
  {
    label: "Capabilities",
    href: "#capabilities",
  },
  {
    label: "Documentation",
    href: "#documentation",
  },
];

export function NavbarLinks({
  className,
}: NavbarLinksProps) {
  return (
    <nav
      className={cn(
        "hidden items-center gap-8 lg:flex",
        className
      )}
    >
      {links.map((link) => (
        <a
          key={link.label}
          href={link.href}
          className={cn(
            "text-sm",
            "font-medium",
            "text-white/70",
            "transition-colors",
            "duration-200",
            "hover:text-white"
          )}
        >
          {link.label}
        </a>
      ))}
    </nav>
  );
}