export const formatTimestamp = (date: Date | number) => {
  let time_ago = 0
  const today = new Date()
  if (date instanceof Date) {
    time_ago = (today.getTime() - date.getTime()) / 1000
  }

  if (typeof date === 'number') {
    time_ago = (today.getTime() / 1000) - date
  }

  if (time_ago > TIME_REFS.year) {
      // if it's over year return date of post YYYY-MM-DD
      const fmt_date = new Date(time_ago * 1000)
      return `${fmt_date.toISOString().slice(0, 10).replace(/-/g, '-')}`
  }
  if (time_ago > TIME_REFS.month) {
      const months = Math.round(time_ago / TIME_REFS.month)
      return `${months} ${months > 1 ? 'months' : 'month'} ago`
  }
  if (time_ago > TIME_REFS.week) {
      const weeks = Math.round(time_ago / TIME_REFS.week)
      return `${weeks} ${weeks > 1 ? 'weeks' : 'week'} ago`
  }
  if (time_ago > TIME_REFS.day) {
      const days = Math.round(time_ago / TIME_REFS.day)
      return `${days} ${days > 1 ? 'days' : 'day'} ago`
  }
  if (time_ago > TIME_REFS.hour) {
      const hours = Math.round(time_ago / TIME_REFS.hour)
      return `${hours} ${hours > 1 ? 'hours' : 'hour'} ago`
  }
  if (time_ago > TIME_REFS.minute) {
      const minutes = Math.round(time_ago / TIME_REFS.minute)
      return `${minutes > 1 ? minutes : 'A' } ${minutes > 1 ? 'minutes' : 'minute'} ago`
  }
  return "Just now"
}

const TIME_REFS = {
  minute: 60,
  hour:   3600,
  day:    86400,
  week:   604800,
  month:  2678400,
  year:   31536000
}
