// Демо-данные. Замените запросами к вашему API.
export const kpis = [
  { label: 'Compliance rate', value: '94,2%', delta: '▲ 1,8 п.п. к вчера', tone: 'ok' },
  { label: 'Нарушений за смену', value: '37', delta: '▼ 6 к вчера', tone: 'ok' },
  { label: 'Людей в кадре сейчас', value: '128', delta: '12 камер онлайн', tone: 'neutral' },
  { label: 'Активные алерты', value: '5', delta: '2 высокого риска', tone: 'high' },
]

export const topViolations = [
  { label: 'Каска', percent: 41 },
  { label: 'Жилет', percent: 27 },
  { label: 'Очки', percent: 15 },
  { label: 'Перчатки', percent: 11 },
  { label: 'Спецобувь', percent: 6 },
]

// compliance по часам, %
export const trend = [
  { t: '08:00', v: 97 }, { t: '09:00', v: 98 }, { t: '10:00', v: 94 },
  { t: '11:00', v: 99 }, { t: '12:00', v: 90 }, { t: '13:00', v: 96 }, { t: '14:00', v: 98 },
]

export const alerts = [
  { risk: 'high', title: 'Нет каски · Склад Б', meta: 'Камера 07 · 12:04 · ID 4821' },
  { risk: 'mid', title: 'Нет жилета · Погрузка', meta: 'Камера 03 · 11:52 · ID 4790' },
  { risk: 'low', title: 'Нет перчаток · Цех 2', meta: 'Камера 11 · 11:40 · ID 4755' },
]

export const recommendations = [
  { risk: 'mid', title: 'Склад Б: 60% нарушений — каска', meta: 'Концентрация в 12:00–13:00. Проверить выдачу СИЗ на смене 1.' },
  { risk: 'mid', title: 'Сотрудники с 3+ повторами за неделю: 4', meta: 'Назначить внеплановый инструктаж.' },
]

export const cameras = [
  { id: '07', zone: 'Склад Б', risk: 'high', status: 'Нарушение', people: [
    { x: 20, y: 30, w: 18, h: 60, label: 'ID 4821 · нет каски', ok: false },
    { x: 58, y: 25, w: 16, h: 65, label: 'ID 4822 · ОК', ok: true } ] },
  { id: '03', zone: 'Погрузка', risk: 'mid', status: 'Предупреждение', people: [
    { x: 35, y: 28, w: 20, h: 62, label: 'ID 4790 · нет жилета', ok: false } ] },
  { id: '11', zone: 'Цех 2', risk: 'low', status: 'Норма', people: [
    { x: 30, y: 26, w: 18, h: 64, label: 'ID 4755 · ОК', ok: true } ] },
  { id: '01', zone: 'Вход', risk: 'low', status: 'Норма', people: [
    { x: 42, y: 25, w: 18, h: 66, label: 'ID 4801 · ОК', ok: true } ] },
]

export const events = [
  { time: '12:04', id: 4821, employee: 'Иванов А. (по лицу)', place: 'Склад Б · К07', ppe: 'Каска', risk: 'high' },
  { time: '11:52', id: 4790, employee: 'Не опознан', place: 'Погрузка · К03', ppe: 'Жилет', risk: 'mid' },
  { time: '11:40', id: 4755, employee: 'Петров С.', place: 'Цех 2 · К11', ppe: 'Перчатки', risk: 'low' },
  { time: '11:21', id: 4702, employee: 'Сидоров Д.', place: 'Склад Б · К07', ppe: 'Каска', risk: 'high' },
]