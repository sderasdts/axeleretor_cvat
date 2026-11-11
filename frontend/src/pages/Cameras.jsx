import PageHeader from '../components/PageHeader'
import CameraTile from '../components/CameraTile'
import { cameras } from '../data/mock'

export default function Cameras() {
  return (
    <>
      <PageHeader title="Камеры в реальном времени" filters={['Сетка 2×2', 'Все зоны']} actionLabel="Добавить камеру" />
      <div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-4">
        {cameras.map((c) => <CameraTile key={c.id} {...c} />)}
      </div>
    </>
  )
}