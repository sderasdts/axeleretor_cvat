import PageHeader from '../components/PageHeader'
import KpiCard from '../components/KpiCard'
import Card from '../components/Card'
import TrendChart from '../components/TrendChart'
import BarList from '../components/BarList'
import AlertList from '../components/AlertList'
import { kpis, trend, topViolations, alerts, recommendations } from '../data/mock'

export default function Dashboard() {
  return (
    <>
      <PageHeader title="Сводка" filters={['Сегодня · смена 1', 'Все зоны', 'Все камеры']} actionLabel="Экспорт" />
      <div className="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4">
        {kpis.map((k) => <KpiCard key={k.label} {...k} />)}
      </div>
      <div className="grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] gap-4">
        <Card title="Compliance по часам" className="md:col-span-2">
          <TrendChart data={trend} />
          <p className="text-[13px] text-muted">Провал в 12:00 — зона «Склад Б», смена 1</p>
        </Card>
        <Card title="Топ нарушений по типу СИЗ"><BarList items={topViolations} /></Card>
      </div>
      <div className="grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] gap-4">
        <Card title="Последние алерты"><AlertList items={alerts} /></Card>
        <Card title="Рекомендации" accent><AlertList items={recommendations} /></Card>
      </div>
    </>
  )
}