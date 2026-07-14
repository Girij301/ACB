import { useExecution } from "@/hooks";


export function ExecutionPanel() {
  const {
    execution,
    loading,
    progress,
    completedSteps,
    totalSteps,
    successfulSteps,
    failedSteps,
  } = useExecution();


  return (
    <section
      className="
        glass
        flex
        h-full
        flex-col
        rounded-2xl
        p-5
      "
    >

      <div className="mb-5 flex items-center justify-between">

        <h2 className="text-lg font-semibold text-white">
          Execution Summary
        </h2>


        {loading && (
          <span
            className="
              text-xs
              text-cyan-300
            "
          >
            Running
          </span>
        )}

      </div>



      <div className="space-y-4">


        {/* Progress */}

        <div
          className="
            rounded-xl
            border
            border-white/10
            bg-white/5
            p-4
          "
        >

          <div
            className="
              mb-3
              flex
              justify-between
              text-sm
              text-white
            "
          >

            <span>
              Progress
            </span>


            <span className="text-white/60">
              {completedSteps}/{totalSteps}
            </span>

          </div>


          <div
            className="
              h-2
              overflow-hidden
              rounded-full
              bg-white/10
            "
          >

            <div
              className="
                h-full
                rounded-full
                bg-cyan-400
                transition-all
              "
              style={{
                width: `${progress}%`,
              }}
            />

          </div>


          <p
            className="
              mt-2
              text-xs
              text-white/50
            "
          >
            {progress}% complete
          </p>


        </div>




        {/* Statistics */}

        <div
          className="
            grid
            grid-cols-3
            gap-3
          "
        >

          <div
            className="
              rounded-xl
              border
              border-white/10
              bg-white/5
              p-3
            "
          >

            <p className="text-xs text-white/50">
              Total
            </p>

            <p className="mt-1 text-lg text-white">
              {totalSteps}
            </p>

          </div>



          <div
            className="
              rounded-xl
              border
              border-green-400/20
              bg-green-500/5
              p-3
            "
          >

            <p className="text-xs text-white/50">
              Success
            </p>

            <p className="mt-1 text-lg text-green-300">
              {successfulSteps}
            </p>

          </div>



          <div
            className="
              rounded-xl
              border
              border-red-400/20
              bg-red-500/5
              p-3
            "
          >

            <p className="text-xs text-white/50">
              Failed
            </p>

            <p className="mt-1 text-lg text-red-300">
              {failedSteps}
            </p>

          </div>


        </div>





        {/* Execution Info */}

        {execution && (

          <div
            className="
              rounded-xl
              border
              border-white/10
              bg-black/20
              p-4
            "
          >

            <p
              className="
                text-xs
                text-white/50
              "
            >
              Execution ID
            </p>


            <p
              className="
                mt-1
                text-sm
                text-white
              "
            >
              #{execution.execution_id}
            </p>


            <p
              className="
                mt-3
                text-xs
                text-white/50
              "
            >
              Workspace
            </p>


            <p
              className="
                mt-1
                truncate
                text-sm
                text-white/80
              "
            >
              {execution.workspace}
            </p>

          </div>

        )}



      </div>

    </section>
  );
}