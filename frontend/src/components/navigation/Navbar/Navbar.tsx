import { cn } from "@/lib";

import { navbarVariants } from "./navbarVariants";
import { NavbarActions } from "./NavbarActions";
import { NavbarBrand } from "./NavbarBrand";
import { NavbarLinks } from "./NavbarLinks";

interface NavbarProps {
  className?: string;
}

export function Navbar({
  className,
}: NavbarProps) {
  return (
    <header className={cn(navbarVariants(), className)}>
      <NavbarBrand />

      <NavbarLinks />

      <NavbarActions />
    </header>
  );
}