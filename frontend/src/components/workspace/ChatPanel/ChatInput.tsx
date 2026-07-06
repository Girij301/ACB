import { useRef, useState } from "react";
import { SendHorizontal } from "lucide-react";

import { Button } from "@/components/ui";

interface ChatInputProps {
  loading: boolean;
  onSend: (message: string) => Promise<void> | void;
}

export function ChatInput({
  loading,
  onSend,
}: ChatInputProps) {
  const [message, setMessage] = useState("");

  const textareaRef =
    useRef<HTMLTextAreaElement>(null);

  function resize() {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "0px";
    textarea.style.height = `${Math.min(
      textarea.scrollHeight,
      180
    )}px`;
  }

  async function submit() {
    const value = message.trim();

    if (!value || loading) return;

    await onSend(value);

    setMessage("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "48px";
    }
  }

  async function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
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
    <div className="mt-5 flex items-end gap-3">
      <textarea
        ref={textareaRef}
        rows={1}
        value={message}
        disabled={loading}
        placeholder="Ask ACB AI anything..."
        onChange={(e) =>
          setMessage(e.target.value)
        }
        onInput={resize}
        onKeyDown={handleKeyDown}
        className="
          glass
          max-h-44
          min-h-12
          flex-1
          resize-none
          overflow-y-auto
          rounded-2xl
          px-4
          py-3
          text-sm
          leading-6
          text-white
          outline-none
          placeholder:text-white/40
          disabled:opacity-60
        "
      />

      <Button
        variant="glass"
        size="md"
        loading={loading}
        onClick={submit}
      >
        {!loading && (
          <SendHorizontal className="h-5 w-5" />
        )}
      </Button>
    </div>
  );
}