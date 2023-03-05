import type { CurrencyKey, RatingKey } from './apiService'

const SALARY_MAP = {
  'GBP': '£',
  'USD': '$',
  'EUR': '€',
  'JPY': 'JPY (¥)',
  'CNY': 'CNY (¥)'
}

const RATING_MAP = {
  'GOOD': 'Good',
  'AVERAGE': 'Meh',
  'BAD': 'Rat-race'
}

export const salaryMapper = (currency: CurrencyKey) =>  SALARY_MAP[currency]

export const ratingsMapper = (rating: RatingKey) => RATING_MAP[rating]
