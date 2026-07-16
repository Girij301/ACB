import { useCallback, useRef } from "react";

interface UseResizableOptions {
  value: number;
  min: number;
  max: number;
  onChange: (value: number) => void;
}

export function useResizable({
  value,
  min,
  max,
  onChange,
}: UseResizableOptions) {
  const startX = useRef(0);
  const startValue = useRef(value);

  const onMouseDown = useCallback(
    (event: React.MouseEvent) => {
      event.preventDefault();

      startX.current = event.clientX;
      startValue.current = value;

      function handleMove(e: MouseEvent) {
        const delta =
          e.clientX - startX.current;

        const next = Math.min(
          max,
          Math.max(
            min,
            startValue.current + delta,
          ),
        );

        onChange(next);
      }

      function handleUp() {
        window.removeEventListener(
          "mousemove",
          handleMove,
        );

        window.removeEventListener(
          "mouseup",
          handleUp,
        );
      }

      window.addEventListener(
        "mousemove",
        handleMove,
      );

      window.addEventListener(
        "mouseup",
        handleUp,
      );
    },
    [value, min, max, onChange],
  );

  return {
    onMouseDown,
  };
}