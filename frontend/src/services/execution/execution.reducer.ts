import type {
  ExecutionEvent,
  ExecutionSummary,
  StepResult,
} from "./types";


export type ExecutionPhase =
  | "idle"
  | "thinking"
  | "planning"
  | "running"
  | "retrying"
  | "debugging"
  | "validating"
  | "completed"
  | "failed";


export interface TimelineEntry {
  id: string;
  type: ExecutionEvent["type"];
  timestamp: string;
  message: string;
  step_number: number | null;
  payload: Record<string, unknown> | null;
}


export interface EventGroup {
  type: string;
  count: number;
  last_timestamp: string;
}


export interface ExecutionState {
  loading: boolean;
  connected: boolean;
  error: string | null;

  execution: ExecutionSummary | null;

  steps: StepResult[];

  events: ExecutionEvent[];

  timeline: TimelineEntry[];

  eventGroups: EventGroup[];

  executionPhase: ExecutionPhase;

  currentPhase: string;

  currentAction: string;

  hasFailed: boolean;

  activeStep: number | null;

  retryingStep: number | null;

  debuggingStep: number | null;

  validating: boolean;

  totalSteps: number;

  completedSteps: number;

  successfulSteps: number;

  failedSteps: number;

  progress: number;
}


export const initialExecutionState: ExecutionState = {

  loading:false,

  connected:false,

  error:null,

  execution:null,

  steps:[],

  events:[],

  timeline:[],

  eventGroups:[],

  executionPhase:"idle",

  currentPhase:"Idle",

  currentAction:"",

  hasFailed:false,

  activeStep:null,

  retryingStep:null,

  debuggingStep:null,

  validating:false,

  totalSteps:0,

  completedSteps:0,

  successfulSteps:0,

  failedSteps:0,

  progress:0,
};



function calculateProgress(
  completed:number,
  total:number,
){
  if(total===0) return 0;

  return Math.round(
    (completed / total) * 100
  );
}



function createTimelineEntry(
  event:ExecutionEvent,
):TimelineEntry{

  return {

    id:
      `${event.type}-${event.timestamp}-${event.step_number ?? "execution"}`,

    type:event.type,

    timestamp:event.timestamp,

    message:event.message,

    step_number:event.step_number,

    payload:event.payload,
  };
}



function updateEventGroups(
  groups:EventGroup[],
  event:ExecutionEvent,
){

  const existing =
    groups.find(
      g=>g.type===event.type
    );


  if(existing){

    return groups.map(g=>

      g.type===event.type
      ?
      {
        ...g,
        count:g.count+1,
        last_timestamp:event.timestamp,
      }
      :
      g
    );

  }


  return [
    ...groups,
    {
      type:event.type,
      count:1,
      last_timestamp:event.timestamp,
    }
  ];

}



export function executionReducer(
  state:ExecutionState,
  event:ExecutionEvent,
):ExecutionState{


  const entry =
    createTimelineEntry(event);



  const duplicate =
    state.timeline.some(
      item=>item.id===entry.id
    );


  if(duplicate){
    return state;
  }



  const nextState:ExecutionState={

    ...state,

    events:[
      ...state.events,
      event
    ],

    timeline:[
      ...state.timeline,
      entry
    ],

    eventGroups:
      updateEventGroups(
        state.eventGroups,
        event
      )
  };



  switch(event.type){


    case "execution_started":


      return {

        ...nextState,


        execution:{

          execution_id:
            event.execution_id ?? 0,

          session_id:
            event.session_id ?? "",


          plan_id:
            Number(event.payload?.plan_id) || 0,


          status:"RUNNING",


          workspace:
            String(
              event.payload?.workspace ?? ""
            ),


          total_steps:
            Number(
              event.payload?.total_steps
            ) || 0,


          successful_steps:0,

          failed_steps:0,

          retry_count:0,

          debug_count:0,

          validation_count:0,

          duration_ms:0,


          started_at:
            event.timestamp,


          completed_at:null,
        },


        loading:true,


        executionPhase:"running",

        currentPhase:"Executing",

        currentAction:event.message,


        totalSteps:
          Number(event.payload?.total_steps) || 0,


        progress:0,

        completedSteps:0,

        successfulSteps:0,

        failedSteps:0,


        hasFailed:false,

      };

    case "step_started":
      return {
        ...nextState,
        activeStep: event.step_number,
        currentAction: event.message,
        currentPhase: "Executing",

      };

    case "step_completed":{
      const success =
        event.payload?.status==="success";
      const completed =
        state.completedSteps + 1;
      const successful =
        success
        ?
        state.successfulSteps+1
        :
        state.successfulSteps;
      const failed =
        success
        ?
        state.failedSteps
        :
        state.failedSteps+1;
      return {
        ...nextState,
        completedSteps:completed,
        successfulSteps:successful,
        failedSteps:failed,
        progress:
          calculateProgress(
            completed,
            state.totalSteps
          ),
        currentPhase:
          success
          ?
          "Executing"
          :
          "Failed",
        currentAction:
          event.message,
        hasFailed:
          !success || state.hasFailed,
        execution:
          state.execution
          ?
          {
            ...state.execution,
            successful_steps:
              successful,
            failed_steps:
              failed,
          }
          :
          null,
          activeStep: null,
      };
    }

    case "execution_finished": {
      const success = event.payload?.success === true;

      return {
        ...nextState,
        loading: false,
        executionPhase: success ? "completed" : "failed",
        currentPhase: success ? "Completed" : "Failed",
        currentAction: event.message,
        progress: 100,
        execution:
          event.payload?.execution
            ? (event.payload.execution as ExecutionSummary)
            : state.execution,
      };
    }

    case "retry_started":
      return {
        ...nextState,
        retryingStep:
          event.step_number,
        executionPhase:"retrying",
        currentPhase:"Retrying",
        currentAction:event.message,
      };

    case "retry_completed":
      return {
        ...nextState,
        retryingStep:null,
        executionPhase:"running",
        currentPhase:"Executing",
        currentAction:event.message,
      };

    case "debug_started":
      return {
        ...nextState,
        debuggingStep:
          event.step_number,
        executionPhase:"debugging",
        currentPhase:"Debugging",
        currentAction:event.message,
      };

    case "debug_completed":
      return {
        ...nextState,
        debuggingStep:null,
        executionPhase:"running",
        currentPhase:"Executing",
        currentAction:event.message,
      };

    case "validation_started":
      return {
        ...nextState,
        validating:true,
        executionPhase:"validating",
        currentPhase:"Validation",
        currentAction:event.message,
      };

    case "validation_completed":
      return {
        ...nextState,
        validating:false,
        executionPhase:"running",
        currentPhase:"Executing",
        currentAction:event.message,
      };

    default:
      return nextState;
  }
}