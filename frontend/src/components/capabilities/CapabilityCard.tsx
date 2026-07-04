import type { LucideIcon } from "lucide-react";

import { Card } from "@/components/ui";

interface CapabilityCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function CapabilityCard({
  icon: Icon,
  title,
  description,
}: CapabilityCardProps) {
  return (
    <Card
      variant="interactive"
      className="
        group
        relative
        overflow-hidden
        rounded-3xl
        p-8
        transition-all
        h-full min-h-80 flex flex-col
        duration-300
        hover:-translate-y-1
        hover:scale-[1.02]
      "
    >
      {/* Animated Border */}

      <div
        className="
          absolute
          inset-0
          rounded-3xl
          bg-linear-to-br
          from-cyan-500/20
          via-transparent
          to-violet-500/20
          opacity-0
          transition-opacity
          duration-500
          group-hover:opacity-100
        "
      />

      <div
        className="
          absolute
          inset-px
          rounded-3xl
          bg-neutral-950
        "
      />

      {/* Spotlight */}

      <div
        className="
          absolute
          -top-20
          left-1/2
          h-40
          w-40
          -translate-x-1/2
          rounded-full
          bg-cyan-400/10
          blur-3xl
          opacity-0
          transition-opacity
          duration-500
          group-hover:opacity-100
        "
      />

      <div className="relative z-10">
        {/* Icon */}

        <div
          className="
            mb-8
            flex
            h-16
            w-16
            items-center
            justify-center
            rounded-2xl
            bg-white/5
            ring-1
            ring-white/10
            transition-all
            duration-500
            group-hover:scale-110
            group-hover:rotate-3
            group-hover:bg-cyan-500/10
          "
        >
          <Icon
            className="
              h-8
              w-8
              text-cyan-300
              transition-transform
              duration-500
              group-hover:scale-110
            "
          />
        </div>

        {/* Title */}

        <h3
          className="
            text-2xl
            font-semibold
            text-white
          "
        >
          {title}
        </h3>

        {/* Description */}

        <p
          className="
            mt-4
            leading-7
            text-white/70
          "
        >
          {description}
        </p>
      </div>
    </Card>
  );
}