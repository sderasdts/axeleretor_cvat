/** Горизонтальные столбцы; жёлтая заливка с чёрной обводкой читается на белом. */
export default function BarList({ items }) {
  return (
    <ul>
      {items.map(({ label, percent }) => (
        <li key={label} className="my-2 grid grid-cols-[90px_1fr_44px] items-center gap-2.5">
          <span>{label}</span>
          <div className="h-2.5 rounded-full bg-line" role="presentation">
            <div
              className="h-2.5 rounded-full border border-ink bg-brand"
              style={{ width: `${percent * 2}%` }}
            />
          </div>
          <b>{percent}%</b>
        </li>
      ))}
    </ul>
  )
}