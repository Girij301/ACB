export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat().format(value);
}