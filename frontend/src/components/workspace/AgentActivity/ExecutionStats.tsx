import { Card, Grid } from "@/components/ui";
import { useExecution } from "@/hooks";

function formatDuration(durationMs: number | undefined) {
  if (!durationMs) {
    return "0s";
  }

  const seconds = Math.floor(durationMs / 1000);

  if (seconds < 60) {
    return `${seconds}s`;
  }

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  return `${minutes}m ${remainingSeconds}s`;
}

function StatCard({
  title,
  value,
  description,
}: {
  title: string;
  value: string | number;
  description?: string;
}) {
  return (
    <Card
      variant="default"
      className="
        rounded-2xl
        border
        border-white/10
        bg-gradient-to-b
        from-white/8
        to-white/5
        p-5
        transition-all
        duration-300
      "
    >
      <p className="text-xs uppercase tracking-wide text-white/45">
        {title}
      </p>

      <p className="mt-3 text-3xl font-semibold text-white">
        {value}
      </p>

      {description && (
        <p className="mt-2 text-xs leading-5 text-white/40">
          {description}
        </p>
      )}
    </Card>
  );
}

export function ExecutionStats() {
  const {
    successfulSteps,
    failedSteps,
    execution,
  } = useExecution();

  return (
    <section className="rounded-2xl border border-white/10 bg-white/5 p-5">
      <div className="mb-5">
        <h3 className="text-sm font-semibold text-white">
          Execution Statistics
        </h3>

        <p className="mt-1 text-xs text-white/45">
          Runtime metrics collected during execution
        </p>
      </div>

      <Grid
        cols={3}
        gap="md"
        className="grid-cols-1 md:grid-cols-2 xl:grid-cols-3"
      >
        <StatCard
          title="Completed Steps"
          value={successfulSteps}
          description="Successful execution steps"
        />

        <StatCard
          title="Failed Steps"
          value={failedSteps}
          description="Failed execution steps"
        />

        <StatCard
          title="Retries"
          value={execution?.retry_count ?? 0}
          description="Recovery attempts"
        />

        <StatCard
          title="Debug Runs"
          value={execution?.debug_count ?? 0}
          description="Debug executions"
        />

        <StatCard
          title="Validation Runs"
          value={execution?.validation_count ?? 0}
          description="Validation checks"
        />

        <StatCard
          title="Execution Time"
          value={formatDuration(
            execution?.duration_ms,
          )}
          description="Total runtime"
        />
      </Grid>
    </section>
  );
}