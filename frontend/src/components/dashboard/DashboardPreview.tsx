import { FadeUp } from "@/components/animations";
import { Heading } from "@/components/ui";

import { dashboardPreviewVariants } from "./dashboardPreviewVariants";
import { DashboardWindow } from "./DashboardWindow";

export function DashboardPreview() {
  return (
    <section className={dashboardPreviewVariants()}>
      <div className="max-w-3xl text-center">
        <Heading level="h2">
          Built for Autonomous Development
        </Heading>

        <p className="mt-6 text-lg text-white/70">
          Watch your AI engineer plan, execute, debug and deliver
          software through a beautiful development workspace.
        </p>
      </div>

      <FadeUp delay={150}>
        <DashboardWindow />
      </FadeUp>
    </section>
  );
}