export default function Card({ title, accent = false, className = '', children }) {
  return (
    <section
      className={`min-w-0 rounded-xl border bg-white p-4.5 ${
        accent ? 'border-2 border-brand' : 'border-line'
      } ${className}`}
    >
      {title && <h2 className="mb-3 text-[15px] font-semibold">{title}</h2>}
      {children}
    </section>
  )
}