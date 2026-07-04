import { cva } from "class-variance-authority";

export const capabilitiesVariants = cva(
  [
    "relative",
    "mx-auto",
    "flex",
    "w-full",
    "max-w-7xl",
    "flex-col",
    "items-center",
    "gap-16",
    "px-6",
    "py-36",
    "lg:px-8",
  ].join(" ")
);

export const capabilityGridVariants = cva(
  [
    "grid",
    "w-full",
    "grid-cols-1",
    "gap-8",
    "md:grid-cols-2",
    "xl:grid-cols-4",
  ].join(" ")
);