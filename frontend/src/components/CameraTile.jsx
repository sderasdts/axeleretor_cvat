import RiskChip from './RiskChip'

/**
 * Плитка камеры с рамками людей. Координаты рамок — в процентах от кадра.
 * Вместо placeholder-фона подставьте <video> / <img> с потоком.
 */
export default function CameraTile({ id, zone, risk, status, people = [], onSelect }) {
  return (
    <article className="overflow-hidden rounded-xl border border-line bg-white">
      <div className="relative h-44 bg-ink-800">
        {people.map((p) => (
          <div key={p.label} className="absolute border-2"
               style={{ left: `${p.x}%`, top: `${p.y}%`, width: `${p.w}%`, height: `${p.h}%`,
                        borderColor: p.ok ? '#1E8E5A' : '#D92D20' }}>
            <span className="absolute -top-5 -left-0.5 whitespace-nowrap px-1.5 text-[11px] text-white"
                  style={{ background: p.ok ? '#17663F' : '#B42318' }}>
              {p.label}
            </span>
          </div>
        ))}
        <span className="absolute top-2.5 left-2.5"><RiskChip risk={risk}>{status}</RiskChip></span>
      </div>
      <button type="button" onClick={() => onSelect?.(id)}
              className="block min-h-11 w-full px-3.5 py-2.5 text-left focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-ink">
        <b>Камера {id}</b>
        <span className="block text-[13px] text-muted">{zone}</span>
      </button>
    </article>
  )
}