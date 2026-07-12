import { footerVariants } from "./footerVariants";

export function Footer() {
  return (
    <footer className={footerVariants()}>
      <div
        className="
          mx-auto
          flex
          max-w-7xl
          flex-col
          items-center
          justify-between
          gap-6
          text-center
          text-sm
          text-white/50
          md:flex-row
        "
      >
        <p>
          © 2026 Coding Agent. All rights reserved. Girij
        </p>

        <div className="flex items-center gap-6">
          <a
            href="#"
            className="transition-colors hover:text-white"
          >
            Documentation
          </a>

          <a
            href="#"
            className="transition-colors hover:text-white"
          >
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}