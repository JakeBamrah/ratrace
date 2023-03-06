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
    return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
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
