import axios from 'redaxios';
import { writable, derived } from 'svelte/store';
import type { Writable, Readable } from 'svelte/store'

import { alphabeticalSort } from './mappers'


export enum Currency {
    GBP = 'GBP',
    USD = 'USD',
    EUR = 'EUR',
    JPY = 'JPY',
    CNY = 'CNY'
}
export type CurrencyKey = keyof typeof Currency

export enum Rating {
    ALL = 'All',
    GOOD = 'Good',
    AVERAGE = 'Meh',
    BAD = 'Rat-race'
}
export type RatingKey = keyof typeof Rating

export enum PostSort {
  DATE_CREATED = 'Date created',
  COMPENSATION = 'Compensation',
  TENURE = 'Tenure',
  STAGES = 'Stages',
  DOWNVOTES = 'Downvotes',
  UPVOTES = 'Upvotes'
}
export type PostSortKey = keyof typeof PostSort

export enum Vote {
    UPVOTE = 1,
    DOWNVOTE = -1
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
  verified: boolean
}

export type OrgQueryParamsType = {
  org_name?: string
  org_id?: number
  industry?: IndustryKey
  tag?: RatingKey
  sort_order?: PostSortKey
  position_id?: number
  limit?: number
  offset?: number
  post_type?: PostEnum
  headquarters?: string
  size?: number
  url?: string
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
  username?: string
  account_id?: number
  password?: string
  dark_mode?: boolean
  anonymous?: boolean
}

export type Position = {
  id: number
  name: string
  org_id: number
  total_reviews: number
  total_interviews: number
}

export type Review = {
  id: number
  account: Account
  position: Position
  created_at: number
  location: string
  org_id: number
  tag: RatingKey
  upvotes: AccountID[]
  downvotes: AccountID[]
  duration_years: number
  post: string
  currency: CurrencyKey
  compensation: number
  reported: boolean
}

export type Interview = {
  id: number
  account: Account
  position: Position
  created_at: number
  location: string
  org_id: number
  stages: number
  tag: RatingKey
  upvotes: AccountID[]
  downvotes: AccountID[]
  post: string
  currency: CurrencyKey
  compensation: number
  reported: boolean
}

export type PostQueryParams = {
    tag: RatingKey
    post: string
    location: string
    position?: string
    position_id?: number
    compensation: number
    tenure_stages?: number
    currency: CurrencyKey
    org_id?: number
    post_type: PostEnum
}
export type onPostType = (args: PostQueryParams) => Promise<any>

export enum PostEnum {
  REVIEW = 'Review',
  INTERVIEW = 'Interview'
}

// HACK: Extend types hack to silence errors
export type Post = (Review | Interview) & { stages?: number, duration_years?: number }

export type VoteParams = {
  post_id: number
  vote: Vote
  already_upvoted?: boolean
  already_downvoted?: boolean
  vote_model_type?: PostEnum
}
export type onVote = (args: VoteParams) => Promise<any>

// store for top level account subscription
export const account: Writable<Account> = writable(null)
export const authenticated: Readable<Boolean> = derived(account, $account => Boolean($account))

export default class ApiService {
  base_url: string
  api: any

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

  sanitizeParams = (args: { [key: string]: any }) => {
    /*
     * Remove undefined or null args from request params. Redaxios doesn't
     * remove null or undefined arguments from request params.
     */
    let sanitized_params = {}
    Object.keys(args).forEach(k => {
      if (args[k] === null || typeof args[k] === 'undefined') {
        console.log(k, args[k])
        return
      }
      sanitized_params[k] = args[k]
    })

    return sanitized_params
  }

  getOrg = async ({ org_id, limit = 50}: OrgQueryParamsType): Promise<{ org: Organisation, reviews: Review[], interviews: Interview[] }> => {
    const params = { org_id, limit }
    const resp = await this.api.get(`/orgs/${org_id}`, { params })

    // sort positions for selected org
    const org = resp.data.org
    org?.positions.sort((a: Organisation, b: Organisation) => alphabeticalSort(a.name, b.name))

    return resp.data
  }

  getOrgNames = async ({ industry, offset, limit }: Omit<OrgQueryParamsType, 'org_name'>): Promise<{ id: string, label: string }[]> => {
    const params = this.sanitizeParams({
      industry: industry && industry !== 'ALL' ? industry : null,
      limit,
      offset
    })

    const resp = await this.api.get('/orgs/get-names', { params })
    return resp.data
  }

  searchOrgs = async ({ org_name, industry, limit, offset }: OrgQueryParamsType): Promise<Organisation[]> => {
    const params = this.sanitizeParams({ org_name, industry, limit, offset })
    const resp = await this.api.get('/orgs/search', { params })
    return resp.data
  }

  getOrgPosts = async(args: OrgQueryParamsType): Promise<{ posts: Post[], max_reached: boolean }> => {
    const {
      org_id,
      position_id,
      tag,
      sort_order,
      limit,
      offset,
      post_type
    } = args

    const params = this.sanitizeParams({
      position_id: position_id === -1 ? null : position_id,
      tag: tag === Rating.ALL.toUpperCase() ? null : tag,
      sort_order,
      limit,
      offset
    })

    let url = `/orgs/${org_id}/reviews`
    if (post_type === PostEnum.INTERVIEW) {
        url = `/orgs/${org_id}/interviews`
    }

    const resp = await this.api.get(url, { params })
    return resp.data
  }

  login = async(args: AccountQueryParams): Promise<{ account?: Account, authenticated: boolean, error?: string }> => {
    const params = this.sanitizeParams(args)
    const resp = await this.api.post('/auth/login', params)
    if (resp.data && resp.data.authenticated) {
      account.set(resp.data.account)
    }

    return resp.data
  }

  authenticate = async(): Promise<{ account?: Account, authenticated: boolean }> => {
    const resp = await this.api.get('/auth/check-session')
    if (resp.data && resp.data.authenticated) {
      account.set(resp.data.account)
    }

    return resp.data.authenticated
  }

  logout = async () => {
    const resp = await this.api.get('/auth/logout')
    if (resp.data && !resp.data.authenticated) {
      account.set(null)
    }
    return resp.data.authenticated
  }

  signup = async (args: AccountQueryParams): Promise<{ account?: Account, error?: string }> => {
    const params = this.sanitizeParams(args)
    const resp = await this.api.post('/auth/signup', params)
    if (resp.data && !resp.data.error) {
      account.set(resp.data.account)
    }

    return resp.data
  }

  accountUpdate = async (args: AccountQueryParams): Promise<any> => {
    const params = this.sanitizeParams(args)
    const resp = await this.api.post('/account/update', params)
    return Boolean(resp.data.error)
  }

  vote = async (args: VoteParams): Promise<any> => {
    const params = this.sanitizeParams(args)
    const resp = await this.api.put('/account/vote', params)
    return resp
  }

  post = async (args: PostQueryParams): Promise<{ post_created: boolean, error?: string}> => {
    const params = this.sanitizeParams({
      tag: args.tag,
      post: args.post,
      location: args.location,
      position: args.position,
      position_id: args.position_id,
      compensation: args.compensation,
      currency: args.currency,
      org_id: args.org_id,
    })

    let url = '/account/post-review'
    if (args.post_type === PostEnum.REVIEW.toUpperCase()) {
      params['duration_years'] = args.tenure_stages
    }

    if (args.post_type === PostEnum.INTERVIEW.toUpperCase()) {
      url = '/account/post-interview'
      // interview stages should always be a whole number
      params['stages'] = Math.round(args.tenure_stages)
    }

    const resp = await this.api.post(url, params)
    return resp.data
  }

  deletePost = async (post_id: number, post_type: PostEnum): Promise<{ post_deleted: boolean, error: string }> => {
    const url = '/account/delete-post'
    const params = this.sanitizeParams({ post_id, post_type })
    const resp = await this.api.post(url, params)
    return resp.data
  }

  createCompany = async (args: OrgQueryParamsType): Promise<{ org_created?: boolean, error?: string }> => {
    const params = this.sanitizeParams({
      name: args.org_name,
      size: args.size,
      headquarters: args.headquarters,
      url: args.url,
      industry: args.industry
    })

    const url = '/orgs/create-company'
    const resp = await this.api.post(url, params)
    return resp.data
  }
}
