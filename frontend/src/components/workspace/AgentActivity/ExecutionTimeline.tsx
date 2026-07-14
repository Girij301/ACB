import { useEffect, useRef } from "react";

import { useExecution } from "@/hooks";

import { ExecutionTimelineItem } from "./ExecutionTimelineItem";


export function ExecutionTimeline() {
  const { timeline } = useExecution();

  const bottomRef = useRef<HTMLDivElement | null>(null);


  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [timeline.length]);


  return (
    <section
      className="
        h-full
        flex
        min-h-0
        flex-1
        flex-col
        rounded-xl
        border
        border-white/10
        bg-white/5
        p-4
      "
    >
      <h3 className="mb-4 text-sm font-medium text-white">
        Execution Timeline
      </h3>


      <div className="flex-1 overflow-y-auto pr-2 min-h-0">

        {timeline.length === 0 ? (
          <p className="text-sm text-white/50">
            No execution events yet.
          </p>
        ) : (

          <div className="relative space-y-5">


            {/* Timeline Line */}
            <div
              className="
                absolute
                left-[7px]
                top-2
                bottom-2
                w-px
                bg-white/10
              "
            />


            {timeline.map((event) => (
              <ExecutionTimelineItem
                key={event.id}
                event={event}
              />
            ))}


            <div ref={bottomRef} />

          </div>

        )}

      </div>

    </section>
  );
}