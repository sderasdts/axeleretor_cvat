import PageHeader from '../components/PageHeader'
import DataTable from '../components/DataTable'
import RiskChip from '../components/RiskChip'
import { events } from '../data/mock'

const columns = [
  { key: 'frame', header: 'Кадр', render: () => <div className="h-10 w-16 rounded-md bg-ink-800" aria-hidden="true" /> },
  { key: 'time', header: 'Время' },
  { key: 'id', header: 'ID', render: (r) => `#${r.id}` },
  { key: 'employee', header: 'Сотрудник' },
  { key: 'place', header: 'Зона · камера' },
  { key: 'ppe', header: 'СИЗ' },
  { key: 'risk', header: 'Риск', render: (r) => <RiskChip risk={r.risk} /> },
]

export default function Journal() {
  return (
    <>
      <PageHeader title="Журнал событий" filters={['Период: 7 дней', 'Тип СИЗ: все', 'Сотрудник: все']} actionLabel="Экспорт" />
      <DataTable columns={columns} rows={events} />
    </>
  )
}