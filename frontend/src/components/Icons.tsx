import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

const base = {
  width: 22,
  height: 22,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
};

export function AskIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M21 11.4a7.8 7.8 0 0 1-8 7.6 9.2 9.2 0 0 1-3.3-.6L5 21l1.2-4.1A7.2 7.2 0 0 1 4 11.6 7.8 7.8 0 0 1 12 4a7.8 7.8 0 0 1 9 7.4Z" />
      <path d="M8.3 11.8h.1M12 11.8h.1M15.7 11.8h.1" />
    </svg>
  );
}

export function BookIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M3.5 5.5A3.5 3.5 0 0 1 7 4h4v16H7a3.5 3.5 0 0 0-3.5 1V5.5Z" />
      <path d="M20.5 5.5A3.5 3.5 0 0 0 17 4h-4v16h4a3.5 3.5 0 0 1 3.5 1V5.5Z" />
    </svg>
  );
}

export function EvalIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="5" y="3" width="14" height="18" rx="1.5" />
      <path d="M9 3.5V2h6v1.5M8.5 9.5l1.4 1.4 2.4-2.7M8.5 15l1.4 1.4 2.4-2.7M14.5 10h2M14.5 15.5h2" />
    </svg>
  );
}

export function SearchIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="m15.5 15.5 5 5" />
    </svg>
  );
}

export function CheckIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="12" cy="12" r="9" fill="currentColor" stroke="none" />
      <path d="m8 12 2.5 2.5L16.5 9" stroke="white" strokeWidth="2" />
    </svg>
  );
}

export function CopyIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="8" y="8" width="11" height="11" rx="1.5" />
      <path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-10A1.5 1.5 0 0 0 3 5.5v10A1.5 1.5 0 0 0 4.5 17H8" />
    </svg>
  );
}
