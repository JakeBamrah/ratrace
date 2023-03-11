import type { CurrencyKey, RatingKey } from './apiService'
import { Rating } from './apiService'

const SALARY_MAP = {
  'GBP': '£',
  'USD': '$',
  'EUR': '€',
  'JPY': 'JPY (¥)',
  'CNY': 'CNY (¥)'
}

export const salaryMapper   = (currency: CurrencyKey) =>  SALARY_MAP[currency]

export const ratingsMapper  = (rating: RatingKey) => Rating[rating]

export const addCommasRegex = (num: string) => {
     // don't ask... copied from stack in a rush:
     // https://stackoverflow.com/questions/2901102/how-to-format-a-number-with-commas-as-thousands-separators
     // adds commas to a string number (can handle decimals but removes zeroes)
     // e.g. 10000.50 -> 10,000.5
    return num.toString().replace(/\B(?!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

export const numCommaFormatter   = (num: number, decimals = 2) => {
  if (isNaN(num))
    return "0"

  let num_str = (num).toFixed(decimals)
  if (decimals > 0) {
    const nums = num_str.split('.')
    let [fmt_num, dec] = nums
    return addCommasRegex(fmt_num) + '.' + dec
  }

  return addCommasRegex(num_str)
}

export const getCompanySizeBracket = (size: number) => {
  if (size > 5000)
      return "5000-1000"
  if (size > 1000)
      return "1000-5000"
  if (size > 500)
      return "500-1000"
  if (size > 200)
      return "200-500"
  if (size > 100)
      return "100-200"
  if (size > 50)
      return "50-100"
  if (size > 10)
      return "10-50"

  return "1-10"
}

export const alphabeticalSort = (a: string, b: string) => {
  if (a < b)
    return -1
  if (a > b)
    return 1

  return 0
}
