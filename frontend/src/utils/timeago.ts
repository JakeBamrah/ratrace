export const formatTimestamp = (date: Date) => {
    const today = new Date()
    const time_ago = (today.getTime() - date.getTime()) / 1000

    if (time_ago > TIME_REFS.year) {
        const years = Math.round(time_ago / TIME_REFS.year)
        return `${years} ${years > 1 ? 'years' : 'year'} ago`
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
