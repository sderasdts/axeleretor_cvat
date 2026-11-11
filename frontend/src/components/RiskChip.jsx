const STYLES = {
  high: 'bg-risk-high-bg text-risk-high-fg',
  mid: 'bg-risk-mid-bg text-risk-mid-fg',
  low: 'bg-risk-ok-bg text-risk-ok-fg',
}
export const RISK_LABEL = { high: 'Высокий', mid: 'Средний', low: 'Низкий' }

/** Статус всегда подписан текстом, цвет — только усиление. */
export default function RiskChip({ risk = 'low', children }) {
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-semibold ${STYLES[risk]}`}>
      {children ?? RISK_LABEL[risk]}
    </span>
  )
}