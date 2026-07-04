import type { PropsWithChildren } from "react";

import { cn } from "../../lib";
import { mainLayoutVariants } from "./mainLayoutVariants";
import { MainLayoutBackground } from "./MainLayoutBackground";

export function MainLayout({
  children,
}: PropsWithChildren) {
  return (
    <div className={cn(mainLayoutVariants())}>
      <MainLayoutBackground />

      {children}
    </div>
  );
}