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
        "flex w-full",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[75%] rounded-2xl px-4 py-3",
          "border border-white/10",
          "text-sm leading-7",
          "shadow-lg",
          isUser
            ? "bg-blue-500/15 text-white"
            : "glass text-white/90"
        )}
      >
        {content}
      </div>
    </div>
  );
}