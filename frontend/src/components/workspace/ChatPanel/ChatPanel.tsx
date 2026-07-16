import {
  Bot,
  Sparkles,
  Zap,
  Code2,
} from "lucide-react";

import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./ChatMessage";

import type { ChatMessage as Message } from "@/services/chat";

interface ChatPanelProps {
  messages: Message[];
  loading: boolean;
  onSend: (
    message: string,
  ) => Promise<void> | void;
}

function SuggestionCard({
  icon,
  text,
}: {
  icon: React.ReactNode;
  text: string;
}) {
  return (
    <div
      className="
        flex
        items-center
        gap-3
        rounded-xl
        border
        border-white/10
        bg-white/5
        p-3
      "
    >
      <div
        className="
          flex
          h-9
          w-9
          items-center
          justify-center
          rounded-lg
          bg-cyan-500/10
          text-cyan-300
        "
      >
        {icon}
      </div>

      <span className="text-sm text-white/70">
        {text}
      </span>
    </div>
  );
}

export function ChatPanel({
  messages,
  loading,
  onSend,
}: ChatPanelProps) {
  return (
    <section className="glass flex h-full min-h-0 flex-col rounded-2xl p-5">
      {/* Header */}

      <div className="mb-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div
            className="
              flex
              h-11
              w-11
              items-center
              justify-center
              rounded-xl
              bg-cyan-500/10
              text-cyan-300
            "
          >
            <Bot className="h-5 w-5" />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white">
              AI Engineer
            </h2>

            <p className="text-sm text-white/45">
              Plan, build, debug and execute projects
            </p>
          </div>
        </div>

        <div
          className="
            rounded-full
            border
            border-emerald-500/20
            bg-emerald-500/10
            px-3
            py-1
            text-xs
            text-emerald-300
          "
        >
          Online
        </div>
      </div>

      {/* Messages */}

      <div
        className="
          min-h-0
          flex-1
          overflow-y-auto
          rounded-2xl
          border
          border-white/10
          bg-black/20
          p-5
        "
      >
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div className="max-w-lg text-center">
              <div
                className="
                  mx-auto
                  flex
                  h-16
                  w-16
                  items-center
                  justify-center
                  rounded-2xl
                  bg-cyan-500/10
                  text-cyan-300
                "
              >
                <Sparkles className="h-8 w-8" />
              </div>

              <h3 className="mt-6 text-2xl font-semibold text-white">
                Welcome to ACB AI
              </h3>

              <p className="mt-3 text-sm leading-7 text-white/50">
                Describe what you want to build and your
                autonomous AI engineer will generate a
                plan, execute it, debug failures and
                continuously monitor the execution.
              </p>

              <div className="mt-8 space-y-3">
                <SuggestionCard
                  icon={<Code2 className="h-4 w-4" />}
                  text="Build a full-stack Todo application"
                />

                <SuggestionCard
                  icon={<Zap className="h-4 w-4" />}
                  text="Debug my FastAPI project"
                />

                <SuggestionCard
                  icon={<Bot className="h-4 w-4" />}
                  text="Explain and improve my codebase"
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-5">
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                role={message.role}
                content={message.content}
              />
            ))}
          </div>
        )}
      </div>

      {/* Input */}

      <div className="mt-5">
        <ChatInput
          loading={loading}
          onSend={onSend}
        />
      </div>
    </section>
  );
}