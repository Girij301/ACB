import { Sparkles } from "lucide-react";

import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./ChatMessage";

import type { ChatMessage as Message } from "@/services/chat";

interface ChatPanelProps {
  messages: Message[];
  loading: boolean;
  onSend: (message: string) => Promise<void> | void;
}

export function ChatPanel({
  messages,
  loading,
  onSend,
}: ChatPanelProps) {
  return (
    <section className="glass flex h-full flex-col rounded-2xl p-5">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-white">
            Chat
          </h2>

          <p className="mt-1 text-sm text-white/50">
            Communicate with your autonomous AI engineer
          </p>
        </div>

        <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-300">
          Online
        </span>
      </div>

      <div
        className="
          flex-1
          overflow-y-auto
          rounded-2xl
          border
          border-white/5
          bg-black/20
          p-5
        "
      >
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div
              className="
                max-w-md
                rounded-2xl
                border
                border-white/10
                bg-white/5
                p-8
                text-center
                shadow-xl
              "
            >
              <div
                className="
                  mx-auto
                  flex
                  h-12
                  w-12
                  items-center
                  justify-center
                  rounded-xl
                  bg-cyan-500/10
                  text-cyan-300
                "
              >
                <Sparkles className="h-6 w-6" />
              </div>

              <h3 className="mt-5 text-xl font-semibold text-white">
                Welcome to ACB AI
              </h3>

              <p className="mt-3 text-sm leading-7 text-white/50">
                Start a conversation to plan, build,
                debug and deploy your project with
                your autonomous AI engineer.
              </p>

              <div
                className="
                  mt-5
                  rounded-xl
                  border
                  border-white/10
                  bg-black/20
                  px-4
                  py-3
                  text-xs
                  text-white/40
                "
              >
                Describe what you want to build...
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
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

      <div className="mt-5">
        <ChatInput
          loading={loading}
          onSend={onSend}
        />
      </div>
    </section>
  );
}