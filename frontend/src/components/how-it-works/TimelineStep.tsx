import type { LucideIcon } from "lucide-react";

import { Card } from "@/components/ui";

interface TimelineStepProps {
  number: string;
  icon: LucideIcon;
  title: string;
  description: string;
}

export function TimelineStep({
  number,
  icon: Icon,
  title,
  description,
}: TimelineStepProps) {
  return (
    <div className="relative flex items-start gap-8">
      {/* Timeline Line */}

      <div
        className="
          absolute
          left-8
          top-16
          bottom-0
          w-px
          bg-linear-to-b
          from-cyan-500/40
          to-transparent
          last:hidden
        "
      />

      {/* Number */}

      <div
        className="
          relative
          z-10
          flex
          h-16
          w-16
          shrink-0
          items-center
          justify-center
          rounded-full
          border
          border-cyan-500/20
          bg-neutral-950
          text-sm
          font-semibold
          text-cyan-300
          shadow-lg
          shadow-cyan-500/10
        "
      >
        {number}
      </div>

      {/* Card */}

      <Card
        variant="interactive"
        className="
          group
          flex-1
          rounded-3xl
          p-8
          transition-all
          duration-500
          hover:-translate-y-1
        "
      >
        <div className="flex items-start gap-5">
          <div
            className="
              flex
              h-14
              w-14
              items-center
              justify-center
              rounded-2xl
              bg-cyan-500/10
              text-cyan-300
              transition-all
              duration-500
              group-hover:scale-110
              group-hover:bg-cyan-500/20
            "
          >
            <Icon className="h-7 w-7" />
          </div>

          <div>
            <h3 className="text-2xl font-semibold text-white">
              {title}
            </h3>

            <p className="mt-4 leading-7 text-white/70">
              {description}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}