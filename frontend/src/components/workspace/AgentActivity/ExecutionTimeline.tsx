import { useEffect, useMemo, useRef } from "react";
import { History } from "lucide-react";

import { useExecution } from "@/hooks";

import { ExecutionTimelineItem } from "./ExecutionTimelineItem";

import type { TimelineEntry } from "@/services/execution";

interface GroupedTimelineEntry extends TimelineEntry {
  repeatCount: number;
}

function collapseTimeline(
  timeline: TimelineEntry[],
): GroupedTimelineEntry[] {
  const result: GroupedTimelineEntry[] = [];

  for (const event of timeline) {
    const previous =
      result[result.length - 1];

    if (
      previous &&
      previous.type === event.type &&
      previous.step_number === event.step_number &&
      previous.message === event.message
    ) {
      previous.repeatCount += 1;
      continue;
    }

    result.push({
      ...event,
      repeatCount: 1,
    });
  }

  return result;
}

export function ExecutionTimeline() {
  const { timeline } = useExecution();

  const bottomRef =
    useRef<HTMLDivElement | null>(null);

  const groupedTimeline =
    useMemo(
      () => collapseTimeline(timeline),
      [timeline],
    );

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [groupedTimeline.length]);

  return (
    <section
      className="
      flex
      h-full
      min-h-0
      flex-col
      rounded-2xl
      border
      border-white/10
      bg-white/5
      p-5
    "
    >
      <div className="mb-5 flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2">
            <History className="h-4 w-4 text-cyan-400" />

            <h3 className="text-sm font-semibold text-white">
              Execution Timeline
            </h3>
          </div>

          <p className="mt-1 text-xs text-white/45">
            Live execution events in chronological order
          </p>
        </div>

        <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-white/60">
          {groupedTimeline.length} Events
        </span>
      </div>

      <div
        className="
        min-h-0
        flex-1
        overflow-y-auto
        pr-2
      "
      >
        {groupedTimeline.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div className="max-w-xs text-center">
              <History className="mx-auto h-10 w-10 text-white/20" />

              <p className="mt-4 text-sm font-medium text-white/70">
                No execution activity
              </p>

              <p className="mt-2 text-xs leading-6 text-white/40">
                Timeline events will appear here once the
                agent begins executing your plan.
              </p>
            </div>
          </div>
        ) : (
          <div className="relative space-y-5">
            <div
              className="
                absolute
                bottom-2
                left-[7px]
                top-2
                w-px
                bg-white/10
              "
            />

            {groupedTimeline.map((event) => (
              <ExecutionTimelineItem
                key={event.id}
                event={event}
                repeatCount={event.repeatCount}
              />
            ))}

            <div ref={bottomRef} />
          </div>
        )}
      </div>
    </section>
  );
}