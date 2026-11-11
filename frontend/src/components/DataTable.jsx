/**
 * columns: [{ key, header, render?(row) }]
 * Широкая таблица прокручивается внутри карточки, а не ломает страницу.
 */
export default function DataTable({ columns, rows, rowKey = 'id', minWidth = 720 }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-line bg-white">
      <table className="w-full border-collapse text-left" style={{ minWidth }}>
        <thead>
          <tr className="text-[13px] text-muted">
            {columns.map((c) => (
              <th key={c.key} scope="col" className="p-3 font-normal">{c.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row[rowKey]} className="border-t border-line">
              {columns.map((c) => (
                <td key={c.key} className="p-3">{c.render ? c.render(row) : row[c.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}