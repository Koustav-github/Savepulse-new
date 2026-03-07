import type { AvailabilityStatus } from "@/data/hospitals";

interface StatusBadgeProps {
  status: AvailabilityStatus;
  size?: "sm" | "md" | "lg";
}

const sizeClasses: Record<string, string> = {
  sm: "px-2 py-0.5 text-[10px]",
  md: "px-2.5 py-1 text-xs",
  lg: "px-3 py-1.5 text-sm",
};

const config: Record<
  AvailabilityStatus,
  { label: string; dot: string; bg: string; text: string }
> = {
  available: {
    label: "Available",
    dot: "bg-green-500",
    bg: "bg-green-100 dark:bg-green-900/40",
    text: "text-green-700 dark:text-green-300",
  },
  busy: {
    label: "Busy",
    dot: "bg-yellow-500",
    bg: "bg-yellow-100 dark:bg-yellow-900/40",
    text: "text-yellow-700 dark:text-yellow-300",
  },
  full: {
    label: "Full",
    dot: "bg-red-500",
    bg: "bg-red-100 dark:bg-red-900/40",
    text: "text-red-700 dark:text-red-300",
  },
  dispatching: {
    label: "Dispatching",
    dot: "bg-orange-500",
    bg: "bg-orange-100 dark:bg-orange-900/40",
    text: "text-orange-700 dark:text-orange-300",
  },
  idle: {
    label: "Idle",
    dot: "bg-gray-400",
    bg: "bg-gray-100 dark:bg-gray-800/40",
    text: "text-gray-600 dark:text-gray-400",
  },
  arriving: {
    label: "Arriving",
    dot: "bg-blue-500",
    bg: "bg-blue-100 dark:bg-blue-900/40",
    text: "text-blue-700 dark:text-blue-300",
  },
  active: {
    label: "Active",
    dot: "bg-emerald-500",
    bg: "bg-emerald-100 dark:bg-emerald-900/40",
    text: "text-emerald-700 dark:text-emerald-300",
  },
  pending: {
    label: "Pending",
    dot: "bg-amber-500",
    bg: "bg-amber-100 dark:bg-amber-900/40",
    text: "text-amber-700 dark:text-amber-300",
  },
  confirmed: {
    label: "Confirmed",
    dot: "bg-blue-600",
    bg: "bg-blue-100 dark:bg-blue-900/40",
    text: "text-blue-700 dark:text-blue-300",
  },
  completed: {
    label: "Completed",
    dot: "bg-gray-500",
    bg: "bg-gray-200 dark:bg-gray-700/40",
    text: "text-gray-700 dark:text-gray-300",
  },
};

export default function StatusBadge({ status, size = "md" }: StatusBadgeProps) {
  const { label, dot, bg, text } = config[status];
  const sz = sizeClasses[size];
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-semibold ${sz} ${bg} ${text}`}
    >
      <span className={`h-2 w-2 rounded-full ${dot}`} />
      {label}
    </span>
  );
}