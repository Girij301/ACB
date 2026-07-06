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
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">
          Chat
        </h2>

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
            <div className="text-center">
              <h3 className="text-2xl font-semibold text-white">
                Welcome to ACB AI
              </h3>

              <p className="mt-4 max-w-md text-sm leading-7 text-white/50">
                Start a conversation to plan,
                build, debug and deploy your
                project with your autonomous AI
                engineer.
              </p>
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

      <ChatInput
        loading={loading}
        onSend={onSend}
      />
    </section>
  );
}