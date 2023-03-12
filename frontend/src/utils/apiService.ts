import axios from 'axios'
import type { AxiosInstance } from 'axios'

import { alphabeticalSort } from './mappers'


export enum Currency {
    GBP = 'gbp',
    USD = 'usd',
    EUR = 'eur',
    JPY = 'jpy',
    CNY = 'cny'
}
export type CurrencyKey = keyof typeof Currency

export enum Rating {
    ALL = 'All',
    GOOD = 'Good',
    AVERAGE = 'Meh',
    BAD = 'Rat-race'
}
export type RatingKey = keyof typeof Rating

export enum ReviewSort {
  DATE_CREATED = 'Date created',
  COMPENSATION = 'Compensation',
  TENURE = 'Tenure',
  DOWNVOTES = 'Downvotes',
  UPVOTES = 'Upvotes'
}
export type ReviewSortKey = keyof typeof ReviewSort

export enum Vote {
    UPVOTE = 'upvote',
    DOWNVOTE = 'downvote'
}

export enum Industry {
    ALL = 'All',
    ACCOUNTANCY_BANKING_FINANCE = 'Accountancy, Banking and Finance',
    BUSINESS_CONSULTING_MANAGEMENT = 'Business, Consulting and Management',
    CHARITY_AND_VOLUNTARY_WORK = 'Charity and Voluntary Work',
    CREATIVE_ARTS_AND_DESIGN = 'Creative Arts and Design',
    EDUCATION = 'Education',
    ENERGY_AND_UTILITIES = 'Energy and Utilities',
    ENGINEERING_AND_MANUFACTURING = 'Engineering and Manufacturing',
    HOSPITALITY = 'Hospitality',
    INFORMATION_TECHONOLOGY = 'I.T',
    LAW = 'Law',
    LAW_ENFORCEMENT_AND_SECURITY = 'Law Enforcement and Security',
    LEISURE_SPORTS_AND_TOURISM = 'Leisure, Sports and Tourism',
    MARKETING_ADVERTISING_AND_PR = 'Marketing, Advertising and PR',
    MEDIA_AND_INTERNET = 'Media and Internet',
    PROPERTY_AND_CONSTRUCTION = 'Property and Construction',
    PUBLIC_SERVICES = 'Public services',
    RECRUITMENT_AND_HR = 'Recruitment and HR',
    RETAIL = 'Retail',
    SALES = 'Sales',
    SCIENCE_AND_PHARMACEUTICALS = 'Science and Pharmaceuticals',
    SOCIAL_CARE = 'Social care',
    TRANSPORT_AND_LOGISTICS = 'Transport and Logistics',
}
export type IndustryKey = keyof typeof Industry

export type Organisation = {
  name: string
  id: number
  created_at: number
  headquarters: string
  industry: Industry
  size: number
  url?: string
  reviews: any[]
  interviews: any[]
  total_reviews: number
  total_interviews: number
}

export type OrgQueryParamsType = {
  org_name?: string
  org_id?: number
  industry?: IndustryKey
  tag?: RatingKey
  sort_order?: ReviewSortKey
  position_id?: number
  limit?: number
  offset?: number
}

type AccountID = number
export type Account = {
  id: AccountID
  username: string
  dark_mode: boolean
  anonymous: boolean
  reviews?: Review[]
  interviews?: Interview[]
}

export type AccountQueryParams = {
  username: string
  account_id?: number
  password?: string
  dark_mode?: Boolean
  anonymous?: string
}

export type Position = {
  id: number
  name: string
  org_id: number
  total_reviews: number
  total_interviews: number
}

export type Review = {
  account: Account
  position: Position
  created_at: number
  location: string
  org_id: number
  tag: RatingKey
  upvotes: AccountID[]
  downvotes: AccountID[]
  duration_years: number
  review: string
  currency: CurrencyKey
  salary: number
}

export type Interview = {
  account: Account
  position: Position
  created_at: number
  location: string
  org_id: number
  tag: RatingKey
  upvotes: AccountID[]
  downvotes: AccountID[]
  interview: string
  currency: CurrencyKey
  offer: number
}


export default class ApiService {
  base_url: string
  api: AxiosInstance

  constructor(base_url: string) {
    let config = {
      headers: {
        'Content-Type': ['application/json', 'gzip'],
        'Access-Control-Allow-Origin': '*'
      },
      baseURL: base_url,
      // allow cookies to be set from a http request from a different domain
      withCredentials: true
    }

    this.api = axios.create(config)
  }

  getOrg = async ({ org_id, limit = 50}: OrgQueryParamsType): Promise<Organisation> => {
    const params = { org_id, limit }
    const resp = await this.api.get(`/orgs/${org_id}`, { params })

    // sort positions for selected org
    const org = resp.data.org.org
    org.positions.sort((a, b) => alphabeticalSort(a.name, b.name))

    return resp.data.org
  }

  getOrgNames = async ({ industry, offset, limit }: Omit<OrgQueryParamsType, 'org_name'>): Promise<{ id: string, label: string }[]> => {
    const params = {
      industry: industry && industry !== 'ALL' ? industry : null,
      limit,
      offset
    }
    const resp = await this.api.get('/orgs/get_names', { params })
    return resp.data
  }

  searchOrgs = async ({ org_name, industry, limit, offset }: OrgQueryParamsType): Promise<Organisation[]> => {
    const params = { org_name, industry, limit, offset }
    const resp = await this.api.get('/orgs/search', { params })
    return resp.data.orgs
  }

  getOrgReviewsAndInterviews = async(args: OrgQueryParamsType) => {
    const {
      org_id,
      position_id,
      tag,
      sort_order,
      limit,
      offset
    } = args

    const params = {
      position_id: position_id === -1 ? null : position_id,
      tag: tag === Rating.ALL.toUpperCase() ? null : tag,
      sort_order,
      limit,
      offset
    }
    const resp = await this.api.get(`/orgs/${org_id}/reviews_and_interviews`, { params })
    return resp.data.reviews_and_interviews
  }

  login = async(args: AccountQueryParams): Promise<any> => {
    const resp = await this.api.post('/auth/login', args)
    return resp.data
  }

  checkLogin = async(): Promise<any> => {
    const resp = await this.api.get('/auth/check_session')
    return resp.data
  }

  logout = async () => {
    const resp = await this.api.get('/auth/logout')
    return resp.data
  }

  signup = async (args: AccountQueryParams): Promise<any> => {
    const resp = await this.api.post('/auth/signup', args)
    return resp.data
  }
}
