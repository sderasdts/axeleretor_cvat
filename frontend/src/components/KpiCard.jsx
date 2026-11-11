import Card from './Card'

const TONE = { ok: 'text-risk-ok-fg', high: 'text-risk-high-fg', neutral: 'text-muted' }

export default function KpiCard({ label, value, delta, tone = 'neutral' }) {
  return (
    <Card>
      <p className="text-[13px] text-muted">{label}</p>
      <p className="my-1 text-3xl font-bold">{value}</p>
      <p className={`text-[13px] font-semibold ${TONE[tone]}`}>{delta}</p>
    </Card>
  )
}