import RiskChip from './RiskChip'

export default function AlertList({ items }) {
  return (
    <ul>
      {items.map(({ risk, title, meta }) => (
        <li key={title} className="flex items-center gap-3 border-t border-line py-2.5 first:border-t-0">
          <RiskChip risk={risk} />
          <div className="flex-1">
            <p className="font-semibold">{title}</p>
            <p className="text-[13px] text-muted">{meta}</p>
          </div>
        </li>
      ))}
    </ul>
  )
}