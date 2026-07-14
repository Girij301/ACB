import { Card } from "@/components/ui";
import { Grid } from "@/components/ui";
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
      className="border-white/10 bg-white/5 p-4"
    >
      <p className="text-xs text-white/50">
        {title}
      </p>

      <p className="mt-2 text-2xl font-semibold text-white">
        {value}
      </p>

      {description && (
        <p className="mt-1 text-xs text-white/40">
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
    <section className="rounded-xl border border-white/10 bg-white/5 p-4">
      <h3 className="mb-4 text-sm font-medium text-white">
        Execution Statistics
      </h3>


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
          value={formatDuration(execution?.duration_ms)}
          description="Total runtime"
        />
      </Grid>
    </section>
  );
}