import * as React from "react";
import { type VariantProps } from "class-variance-authority";

import { avatarVariants } from "./avatarVariants";
import { cn } from "../../../lib";

export interface AvatarProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof avatarVariants> {
  src?: string;
  alt?: string;
  initials?: string;
}

export function Avatar({
  className,
  size,
  variant,
  src,
  alt,
  initials,
  ...props
}: AvatarProps) {
  return (
    <div
      className={cn(
        avatarVariants({
          size,
          variant,
        }),
        className
      )}
      {...props}
    >
      {src ? (
        <img
          src={src}
          alt={alt}
          className="h-full w-full object-cover"
        />
      ) : (
        <span className="font-medium text-white">
          {initials ?? "AI"}
        </span>
      )}
    </div>
  );
}