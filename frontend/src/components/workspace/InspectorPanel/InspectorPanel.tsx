export function InspectorPanel() {
  return (
    <section
      className="
        glass
        flex
        h-full
        flex-col
        rounded-2xl
        p-5
      "
    >
      <h2 className="text-lg font-semibold text-white">
        Inspector
      </h2>

      <div className="mt-4 flex-1 rounded-xl border border-white/5 bg-black/20" />
    </section>
  );
}