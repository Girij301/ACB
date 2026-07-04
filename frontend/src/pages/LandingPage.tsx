import { Hero } from "@/components/hero";
import { Capabilities } from "@/components/capabilities";
import { HowItWorks } from "@/components/how-it-works";
import { Navbar } from "@/components/navigation";
import { MainLayout } from "@/layouts/MainLayout";
import { DashboardPreview } from "@/components/dashboard";
import { CallToAction } from "@/components/call-to-action";
import { Footer } from "@/components/footer";
import { GlobalBackground } from "@/components/background";

export function LandingPage() {
  return (
    <MainLayout>
      <GlobalBackground />
      <Navbar />

      <Hero />

      <Capabilities />

      <HowItWorks />
      <DashboardPreview />
      <CallToAction />
      <Footer />
    </MainLayout>
  );
}