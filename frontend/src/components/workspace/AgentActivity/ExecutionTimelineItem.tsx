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
}


function getEventIcon(type: string) {
  switch (type) {
    case "execution_started":
      return <Play className="h-4 w-4 text-cyan-400" />;


    case "step_started":
      return (
        <LoaderCircle
          className="h-4 w-4 animate-spin text-cyan-400"
        />
      );


    case "step_completed":
      return (
        <CheckCircle2
          className="h-4 w-4 text-green-400"
        />
      );


    case "retry_started":
      return (
        <RotateCcw
          className="h-4 w-4 text-yellow-400"
        />
      );


    case "retry_completed":
      return (
        <CheckCircle2
          className="h-4 w-4 text-green-400"
        />
      );


    case "debug_started":
      return (
        <Bug
          className="h-4 w-4 text-red-400"
        />
      );


    case "debug_completed":
      return (
        <CheckCircle2
          className="h-4 w-4 text-green-400"
        />
      );


    case "validation_started":
      return (
        <ShieldCheck
          className="h-4 w-4 text-indigo-400"
        />
      );


    case "validation_completed":
      return (
        <CheckCircle2
          className="h-4 w-4 text-green-400"
        />
      );


    case "execution_finished":
      return (
        <Flag
          className="h-4 w-4 text-emerald-400"
        />
      );


    default:
      return (
        <XCircle
          className="h-4 w-4 text-red-400"
        />
      );
  }
}



function getEventTitle(type: string) {
  switch (type) {

    case "execution_started":
      return "Execution Started";


    case "step_started":
      return "Step Started";


    case "step_completed":
      return "Step Completed";


    case "retry_started":
      return "Retry Started";


    case "retry_completed":
      return "Retry Completed";


    case "debug_started":
      return "Debug Started";


    case "debug_completed":
      return "Debug Completed";


    case "validation_started":
      return "Validation Started";


    case "validation_completed":
      return "Validation Completed";


    case "execution_finished":
      return "Execution Finished";


    default:
      return "Event";
  }
}



function getCardStyle(type: string) {

  switch(type) {

    case "step_started":
    case "retry_started":
    case "debug_started":
    case "validation_started":

      return `
        border-cyan-400/30
        bg-cyan-500/5
      `;


    case "execution_finished":

      return `
        border-emerald-400/30
        bg-emerald-500/5
      `;


    case "step_completed":
    case "retry_completed":
    case "debug_completed":
    case "validation_completed":

      return `
        border-green-400/20
        bg-green-500/5
      `;


    default:

      return `
        border-white/10
        bg-black/20
      `;
  }

}



export function ExecutionTimelineItem({
  event,
}: Props) {


  return (

    <div className="relative flex gap-4">


      {/* Timeline Node */}

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



      {/* Content */}

      <div className="flex-1">


        <div
          className={`
            rounded-xl
            border
            p-3
            transition-all
            duration-300
            ${getCardStyle(event.type)}
          `}
        >


          <div
            className="
              flex
              items-center
              justify-between
            "
          >

            <p className="text-sm font-medium text-white">
              {getEventTitle(event.type)}
            </p>



            {
              event.step_number !== null && (

                <span
                  className="
                    rounded-full
                    bg-cyan-500/20
                    px-2
                    py-0.5
                    text-xs
                    text-cyan-300
                  "
                >
                  Step {event.step_number}
                </span>

              )
            }


          </div>



          <p
            className="
              mt-2
              text-sm
              text-white/80
            "
          >
            {event.message}
          </p>



          <p
            className="
              mt-2
              text-xs
              text-white/40
            "
          >
            {
              new Date(
                event.timestamp
              ).toLocaleTimeString()
            }
          </p>


        </div>


      </div>


    </div>

  );
}