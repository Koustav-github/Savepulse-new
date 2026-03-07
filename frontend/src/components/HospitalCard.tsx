import StatusBadge from "./StatusBadge";
import type { AvailabilityStatus } from "@/data/hospitals";
import type { Hospital as MockHospital } from "@/lib/mockData";
import type { Hospital as DataHospital } from "@/data/hospitals";

type CombinedHospital = MockHospital | DataHospital;

interface HospitalCardProps {
  hospital?: CombinedHospital;
  name?: string;
  distance?: string;
  specializations?: string[];
  availability?: AvailabilityStatus | MockHospital["availability"];
  etaMinutes?: number;
  selected?: boolean;
  onSelect?: () => void;
  showDispatchButton?: boolean;
}

export default function HospitalCard({
  hospital,
  name,
  distance,
  specializations,
  availability,
  etaMinutes,
  selected,
  onSelect,
  showDispatchButton = true,
}: HospitalCardProps) {
  // Extract values with priority to the 'hospital' object
  const finalName = hospital?.name ?? name ?? "Unknown Hospital";
  const finalDistance = hospital?.distance ?? distance ?? "Unknown distance";
  
  // Logic to get specializations
  let finalSpecializations: string[] = specializations ?? [];
  if (hospital && "specializations" in hospital) {
    finalSpecializations = hospital.specializations;
  } else if (hospital && !("specializations" in hospital)) {
    // It's a MockHospital, derive from boolean flags
    if ((hospital as MockHospital).hasCardiacUnit) finalSpecializations.push("Cardiac Care");
    if ((hospital as MockHospital).hasTraumaUnit) finalSpecializations.push("Trauma Center");
    if ((hospital as MockHospital).hasRespUnit) finalSpecializations.push("Respiratory");
    if ((hospital as MockHospital).hasMaternalUnit) finalSpecializations.push("Maternity");
  }

  // Logic to get availability status for StatusBadge
  const rawAvailability = hospital?.availability ?? availability ?? "available";
  // Map 'limited' from mockData to 'busy' for StatusBadge consistency if needed
  const finalAvailability = rawAvailability === "limited" ? "busy" : (rawAvailability as any);

  // Logic to get ETA
  const finalEta = (hospital && "etaMinutes" in hospital) 
    ? hospital.etaMinutes 
    : (hospital && "erWaitMin" in hospital)
    ? (hospital as MockHospital).erWaitMin
    : etaMinutes ?? 0;

  return (
    <div 
      onClick={onSelect}
      className={`rounded-2xl border p-4 shadow-sm transition-all cursor-pointer ${
        selected 
          ? "border-emerald-500 bg-emerald-50/50 dark:border-emerald-500/50 dark:bg-emerald-950/20 ring-1 ring-emerald-500/20" 
          : "border-gray-200 bg-white dark:border-slate-700 dark:bg-slate-800 hover:border-gray-300 dark:hover:border-slate-600"
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-gray-900 dark:text-white truncate">
              {finalName}
            </h3>
            {selected && (
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-emerald-500 text-[10px] text-white">
                ✓
              </span>
            )}
          </div>
          <p className="mt-0.5 text-sm text-gray-500 dark:text-slate-400">
            📍 {finalDistance}
          </p>
        </div>
        <StatusBadge status={finalAvailability} />
      </div>

      <div className="mt-3 flex flex-wrap gap-1.5">
        {finalSpecializations.slice(0, 3).map((spec) => (
          <span
            key={spec}
            className="rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-900/40 dark:text-blue-300"
          >
            {spec}
          </span>
        ))}
      </div>

      <div className="mt-3 flex items-center justify-between">
        <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-slate-300">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span>~{finalEta} min arrival</span>
        </div>

        {showDispatchButton && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onSelect?.();
            }}
            disabled={finalAvailability === "full"}
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition-colors ${
              finalAvailability === "full"
                ? "cursor-not-allowed bg-gray-200 text-gray-400 dark:bg-slate-700 dark:text-slate-500"
                : "bg-red-600 text-white hover:bg-red-700 active:bg-red-800"
            }`}
          >
            {finalAvailability === "full" ? "Full" : "Select & Dispatch"}
          </button>
        )}
      </div>
    </div>
  );
}
