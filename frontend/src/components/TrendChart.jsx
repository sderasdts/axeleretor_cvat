/** Лёгкий SVG-график без зависимостей. data: [{ t, v }], v — проценты 85–100. */
export default function TrendChart({ data, min = 85, max = 100, width = 640, height = 200 }) {
  const pad = { l: 34, r: 12, t: 16, b: 28 }
  const x = (i) => pad.l + (i * (width - pad.l - pad.r)) / (data.length - 1)
  const y = (v) => pad.t + ((max - v) * (height - pad.t - pad.b)) / (max - min)
  const points = data.map((d, i) => `${x(i)},${y(d.v)}`).join(' ')
  const low = data.reduce((a, b) => (b.v < a.v ? b : a))
  const ticks = [100, 95, 90, 85]

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="w-full" role="img"
         aria-label={`Compliance по часам, минимум ${low.v}% в ${low.t}`}>
      {ticks.map((t) => (
        <g key={t}>
          <line x1={pad.l} x2={width - pad.r} y1={y(t)} y2={y(t)} className="stroke-line" />
          <text x={0} y={y(t) + 4} className="fill-muted text-[11px]">{t}</text>
        </g>
      ))}
      <polyline points={points} fill="none" className="stroke-ink" strokeWidth="3" />
      {data.map((d, i) => (
        <text key={d.t} x={x(i)} y={height - 6} textAnchor="middle" className="fill-muted text-[11px]">{d.t}</text>
      ))}
      <circle cx={x(data.indexOf(low))} cy={y(low.v)} r="6" className="fill-risk-high-fg" />
    </svg>
  )
}