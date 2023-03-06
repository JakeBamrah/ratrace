import axios from 'axios'
import type { AxiosInstance } from 'axios'


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
}

type OrgQueryParamsType = {
  org_name?: string
  org_id?: number
  industry?: IndustryKey
  limit?: number
  review_limit?: number
  interview_limit?: number
  position?: string
  offset?: number
}

type AccountID = number
export type Account = {
  id: AccountID
  username: string
}

export type Position = {
  id: number
  name: string
  org_id: number
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
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      baseURL: base_url
    }

    this.api = axios.create(config)
  }

  getOrg = async ({ org_id, review_limit, interview_limit, position }: OrgQueryParamsType): Promise<Organisation> => {
    const params = { review_limit, interview_limit, position }
    const resp = await this.api.get(`/orgs/${org_id}`, { params })
    return resp.data.org
  }

  getOrgNames = async ({ industry, offset, limit }: Omit<OrgQueryParamsType, 'org_name'>): Promise<{ id: string, label: string }[]> => {
    const params = { industry, limit, offset }
    const resp = await this.api.get('/orgs/get_names', { params })
    return resp.data.org_names
  }

  searchOrgs = async ({ org_name, industry, limit, offset }: OrgQueryParamsType): Promise<Organisation[]> => {
    const params = { org_name, industry, limit, offset }
    const resp = await this.api.get('/orgs/search', { params })
    return resp.data.orgs
  }
}
