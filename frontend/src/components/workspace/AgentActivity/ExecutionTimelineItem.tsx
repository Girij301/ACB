import {
  CheckCircle2,
  RotateCcw,
  Bug,
  ShieldCheck,
  Play,
  Flag,
  XCircle,
  LoaderCircle,
} from "lucide-react";

import type { TimelineEntry } from "@/services/execution";

interface Props {
  event: TimelineEntry;
  repeatCount?: number;
}

function formatTimestamp(timestamp: string) {
  const date = new Date(timestamp);

  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function getEventIcon(type: string) {
  switch (type) {
    case "execution_started":
      return <Play className="h-4 w-4 text-cyan-400" />;

    case "step_started":
      return (
        <LoaderCircle className="h-4 w-4 animate-spin text-cyan-400" />
      );

    case "step_completed":
      return (
        <CheckCircle2 className="h-4 w-4 text-green-400" />
      );

    case "retry_started":
    case "retry_completed":
      return (
        <RotateCcw className="h-4 w-4 text-yellow-400" />
      );

    case "debug_started":
      return (
        <Bug className="h-4 w-4 text-red-400" />
      );

    case "debug_completed":
      return (
        <CheckCircle2 className="h-4 w-4 text-green-400" />
      );

    case "validation_started":
    case "validation_completed":
      return (
        <ShieldCheck className="h-4 w-4 text-indigo-400" />
      );

    case "execution_finished":
      return (
        <Flag className="h-4 w-4 text-emerald-400" />
      );

    default:
      return (
        <XCircle className="h-4 w-4 text-red-400" />
      );
  }
}

function getEventTitle(type: string) {
  switch (type) {
    case "retry_started":
      return "Retry Attempt Started";

    case "retry_completed":
      return "Retry Recovery Completed";

    case "validation_started":
      return "Validation Running";

    case "validation_completed":
      return "Validation Passed";

    case "execution_started":
      return "Execution Started";

    case "step_started":
      return "Step Started";

    case "step_completed":
      return "Step Completed";

    case "debug_started":
      return "Debugging Started";

    case "debug_completed":
      return "Debug Completed";

    case "execution_finished":
      return "Execution Finished";

    default:
      return "Event";
  }
}

function getStatusBadge(type: string) {
  switch (type) {
    case "retry_started":
      return "RECOVERY";

    case "retry_completed":
      return "RECOVERED";

    case "validation_started":
      return "CHECKING";

    case "validation_completed":
      return "PASSED";

    case "debug_started":
      return "FIXING";

    case "debug_completed":
      return "FIXED";

    default:
      return null;
  }
}

function getCardStyle(type: string) {
  switch (type) {
    case "retry_started":
    case "retry_completed":
      return "border-yellow-400/30 bg-yellow-500/5";

    case "validation_started":
    case "validation_completed":
      return "border-indigo-400/30 bg-indigo-500/5";

    case "debug_started":
      return "border-red-400/30 bg-red-500/5";

    case "step_started":
      return "border-cyan-400/30 bg-cyan-500/5";

    case "step_completed":
    case "debug_completed":
      return "border-green-400/20 bg-green-500/5";

    case "execution_finished":
      return "border-emerald-400/30 bg-emerald-500/5";

    default:
      return "border-white/10 bg-black/20";
  }
}

export function ExecutionTimelineItem({
  event,
  repeatCount = 1,
}: Props) {
  const badge =
    getStatusBadge(event.type);

  return (
    <div className="relative flex gap-4">
      <div
        className="
          relative
          z-10
          flex
          h-4
          w-4
          items-center
          justify-center
          rounded-full
          bg-black
        "
      >
        {getEventIcon(event.type)}
      </div>

      <div className="flex-1">
        <div
          className={`
            rounded-2xl
            border
            p-4
            transition-all
            duration-300
            ${getCardStyle(event.type)}
          `}
        >
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h4 className="text-sm font-semibold text-white">
                {getEventTitle(event.type)}
              </h4>

              <p className="mt-2 text-sm leading-6 text-white/75">
                {event.message}
              </p>
            </div>

            <div className="flex flex-wrap justify-end gap-2">
              {badge && (
                <span className="rounded-full bg-white/10 px-2.5 py-1 text-[11px] font-medium text-white/70">
                  {badge}
                </span>
              )}

              {event.step_number !== null && (
                <span className="rounded-full bg-cyan-500/20 px-2.5 py-1 text-[11px] font-medium text-cyan-300">
                  Step {event.step_number}
                </span>
              )}

              {repeatCount > 1 && (
                <span className="rounded-full bg-white/10 px-2.5 py-1 text-[11px] font-medium text-white/60">
                  ×{repeatCount}
                </span>
              )}
            </div>
          </div>

          <div className="mt-4 border-t border-white/5 pt-3">
            <p className="text-xs tracking-wide text-white/40">
              {formatTimestamp(event.timestamp)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}