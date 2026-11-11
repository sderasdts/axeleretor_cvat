import Button from './Button'

export default function PageHeader({ title, filters = [], actionLabel, onAction }) {
  return (
    <header className="flex flex-wrap items-center justify-between gap-3">
      <h1 className="text-2xl font-semibold">{title}</h1>
      <div className="flex flex-wrap gap-2">
        {filters.map((f) => (
          <button key={f} type="button"
                  className="inline-flex min-h-11 items-center rounded-lg border border-line bg-white px-3.5 hover:bg-surface focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink">
            {f}
          </button>
        ))}
        {actionLabel && <Button onClick={onAction}>{actionLabel}</Button>}
      </div>
    </header>
  )
}