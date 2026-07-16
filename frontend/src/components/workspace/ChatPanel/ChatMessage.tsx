import {
  Bot,
  User,
} from "lucide-react";

import { cn } from "@/lib";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export function ChatMessage({
  role,
  content,
}: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        "flex gap-3",
        isUser
          ? "justify-end"
          : "justify-start",
      )}
    >
      {!isUser && (
        <div
          className="
            flex
            h-10
            w-10
            shrink-0
            items-center
            justify-center
            rounded-xl
            bg-cyan-500/10
            text-cyan-300
          "
        >
          <Bot className="h-5 w-5" />
        </div>
      )}

      <div
        className={cn(
          "max-w-[75%]",
          "rounded-2xl",
          "border",
          "px-5",
          "py-4",
          "text-sm",
          "leading-7",
          "shadow-lg",
          isUser
            ? "border-blue-500/20 bg-blue-500/15 text-white"
            : "border-white/10 bg-white/5 text-white/90",
        )}
      >
        {content}
      </div>

      {isUser && (
        <div
          className="
            flex
            h-10
            w-10
            shrink-0
            items-center
            justify-center
            rounded-xl
            bg-blue-500/10
            text-blue-300
          "
        >
          <User className="h-5 w-5" />
        </div>
      )}
    </div>
  );
}