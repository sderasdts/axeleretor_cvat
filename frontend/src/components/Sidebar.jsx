export const NAV = [
  { key: 'dashboard', label: 'Дашборд' },
  { key: 'cameras', label: 'Камеры' },
  { key: 'journal', label: 'Журнал событий' },
  { key: 'employees', label: 'Сотрудники' },
  { key: 'alerts', label: 'Оповещения' },
  { key: 'reports', label: 'Отчёты' },
  { key: 'settings', label: 'Настройки' },
]

export default function Sidebar({ active, onNavigate, items = NAV }) {
  return (
    <nav aria-label="Основная навигация" className="flex w-54 flex-none flex-col gap-1 bg-ink px-3 py-5 text-[#D6D6D6]">
      <div className="flex items-center gap-2.5 px-2 pb-5 text-base font-bold text-white">
        <span className="size-7 rounded-[7px] bg-brand" aria-hidden="true" />
        СИЗ·Контроль
      </div>
      {items.map(({ key, label }) => {
        const on = key === active
        return (
          <button key={key} type="button" onClick={() => onNavigate?.(key)}
                  aria-current={on ? 'page' : undefined}
                  className={`flex min-h-11 items-center gap-2.5 rounded-lg px-2.5 text-left
                    focus-visible:outline-2 focus-visible:outline-brand
                    ${on ? 'bg-ink-700 font-semibold text-white' : 'hover:bg-ink-800'}`}>
            <span className={`size-2 rounded-xs ${on ? 'bg-brand' : 'bg-[#8A8A8A]'}`} aria-hidden="true" />
            {label}
          </button>
        )
      })}
    </nav>
  )
}