const VARIANTS = {
  primary: 'bg-brand border-brand text-ink font-semibold hover:brightness-95',
  secondary: 'bg-white border-line text-ink hover:bg-surface',
}
export default function Button({ variant = 'primary', className = '', ...props }) {
  return (
    <button
      className={`inline-flex min-h-11 items-center justify-center rounded-lg border px-3.5
        focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink
        ${VARIANTS[variant]} ${className}`}
      {...props}
    />
  )
}