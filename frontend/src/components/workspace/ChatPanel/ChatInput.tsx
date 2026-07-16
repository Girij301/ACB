import { useRef, useState } from "react";
import {
  SendHorizontal,
  Sparkles,
} from "lucide-react";

import { Button } from "@/components/ui";

interface ChatInputProps {
  loading: boolean;
  onSend: (
    message: string,
  ) => Promise<void> | void;
}

export function ChatInput({
  loading,
  onSend,
}: ChatInputProps) {
  const [message, setMessage] =
    useState("");

  const textareaRef =
    useRef<HTMLTextAreaElement>(null);

  function resize() {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "0px";

    textarea.style.height = `${Math.min(
      textarea.scrollHeight,
      180,
    )}px`;
  }

  async function submit() {
    const value = message.trim();

    if (!value || loading) return;

    await onSend(value);

    setMessage("");

    if (textareaRef.current) {
      textareaRef.current.style.height =
        "52px";
    }
  }

  async function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>,
  ) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      await submit();
    }
  }

  return (
    <div
      className="
        rounded-2xl
        border
        border-white/10
        bg-white/5
        p-3
        backdrop-blur-xl
      "
    >
      <div className="mb-3 flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-cyan-400" />

        <p className="text-xs text-white/50">
          Press Enter to send • Shift + Enter for
          a new line
        </p>
      </div>

      <div className="flex items-end gap-3">
        <textarea
          ref={textareaRef}
          rows={1}
          value={message}
          disabled={loading}
          placeholder="Describe what you want ACB AI to build..."
          onChange={(e) =>
            setMessage(e.target.value)
          }
          onInput={resize}
          onKeyDown={handleKeyDown}
          className="
            min-h-[52px]
            max-h-44
            flex-1
            resize-none
            overflow-y-auto
            rounded-xl
            border
            border-white/10
            bg-black/20
            px-4
            py-3
            text-sm
            leading-6
            text-white
            outline-none
            transition-all
            duration-200
            placeholder:text-white/35
            focus:border-cyan-500/40
            focus:bg-black/30
            disabled:opacity-60
          "
        />

        <Button
          variant="glass"
          size="md"
          loading={loading}
          onClick={submit}
          className="
            h-[52px]
            rounded-xl
            px-5
          "
        >
          {!loading && (
            <>
              <SendHorizontal className="h-4 w-4" />

              <span className="ml-2">
                Send
              </span>
            </>
          )}
        </Button>
      </div>
    </div>
  );
}