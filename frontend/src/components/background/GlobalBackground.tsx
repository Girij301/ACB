export function GlobalBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-50 overflow-hidden">
      {/* Center Glow */}

      <div
        className="
          absolute
          left-1/2
          top-0
          h-[60rem]
          w-[60rem]
          -translate-x-1/2
          rounded-full
          bg-cyan-500/[0.05]
          blur-[180px]
        "
      />

      {/* Left Glow */}

      <div
        className="
          absolute
          -left-40
          top-1/3
          h-[40rem]
          w-[40rem]
          rounded-full
          bg-violet-500/[0.04]
          blur-[170px]
        "
      />

      {/* Right Glow */}

      <div
        className="
          absolute
          -right-40
          top-1/4
          h-[42rem]
          w-[42rem]
          rounded-full
          bg-sky-500/[0.04]
          blur-[170px]
        "
      />
    </div>
  );
}