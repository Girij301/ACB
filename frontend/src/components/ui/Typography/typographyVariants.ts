import { cva } from "class-variance-authority";

export const headingVariants = cva(
  [
    "font-heading",
    "italic",
    "tracking-tight",
    "text-white",
  ],
  {
    variants: {
      level: {
        h1: "text-6xl md:text-7xl lg:text-8xl leading-none",
        h2: "text-5xl md:text-6xl leading-tight",
        h3: "text-4xl md:text-5xl",
        h4: "text-3xl",
        h5: "text-2xl",
        h6: "text-xl",
      },
    },

    defaultVariants: {
      level: "h2",
    },
  }
);

export const textVariants = cva(
  [
    "font-body",
    "text-white",
  ],
  {
    variants: {
      variant: {
        body: "text-base leading-relaxed",
        muted: "text-white/70",
        small: "text-sm",
        caption: "text-xs text-white/60",
      },
    },

    defaultVariants: {
      variant: "body",
    },
  }
);