import { LoaderCircle } from "lucide-react";

import { useExecution } from "@/hooks";


function StatBox({
  title,
  value,
  variant = "default",
}: {
  title: string;
  value: number;
  variant?: "default" | "success" | "failed";
}) {

  const styles = {
    default:
      "border-white/10 bg-white/5 text-white",
    success:
      "border-green-400/20 bg-green-500/5 text-green-300",
    failed:
      "border-red-400/20 bg-red-500/5 text-red-300",
  };


  return (
    <div
      className={`
        rounded-xl
        border
        p-3
        transition-all
        duration-300
        hover:bg-white/10
        ${styles[variant]}
      `}
    >
      <p className="text-xs text-white/50">
        {title}
      </p>

      <p className="mt-1 text-lg font-semibold">
        {value}
      </p>
    </div>
  );
}



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


      <div
        className="
          mb-5
          flex
          items-center
          justify-between
        "
      >

        <h2
          className="
            text-lg
            font-semibold
            text-white
          "
        >
          Execution Summary
        </h2>



        {
          loading && (

            <div
              className="
                flex
                items-center
                gap-2
                rounded-full
                border
                border-cyan-400/20
                bg-cyan-500/10
                px-3
                py-1
                text-xs
                text-cyan-300
              "
            >

              <LoaderCircle
                className="
                  h-3
                  w-3
                  animate-spin
                "
              />

              Running

            </div>

          )
        }

      </div>




      {
        !execution && !loading && (

          <div
            className="
              flex
              flex-1
              items-center
              justify-center
              rounded-xl
              border
              border-white/10
              bg-black/20
            "
          >

            <div
              className="
                text-center
              "
            >

              <p
                className="
                  text-sm
                  text-white/70
                "
              >
                No execution started
              </p>


              <p
                className="
                  mt-2
                  text-xs
                  text-white/40
                "
              >
                Start an execution to see live progress.
              </p>

            </div>

          </div>

        )

      }




      {
        (execution || loading) && (

          <div
            className="
              space-y-4
            "
          >



            {/* Progress */}

            <div
              className="
                rounded-xl
                border
                border-white/10
                bg-white/5
                p-4
                transition-all
                duration-300
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


                <span
                  className="
                    text-white/60
                  "
                >
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
                    duration-500
                  "
                  style={{
                    width:`${progress}%`,
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





            {/* Stats */}

            <div
              className="
                grid
                grid-cols-3
                gap-3
              "
            >

              <StatBox
                title="Total"
                value={totalSteps}
              />


              <StatBox
                title="Success"
                value={successfulSteps}
                variant="success"
              />


              <StatBox
                title="Failed"
                value={failedSteps}
                variant="failed"
              />


            </div>





            {
              execution && (

                <div
                  className="
                    rounded-xl
                    border
                    border-white/10
                    bg-black/20
                    p-4
                    transition-all
                    duration-300
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

              )
            }


          </div>

        )
      }


    </section>

  );
}