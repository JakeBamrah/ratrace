import axios from 'axios'
import type { AxiosInstance } from 'axios'

type OrgType = {
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

export enum Industry {
    ALL = 'All',
    TRANSPORT_AND_LOGISTICS = 'Transport and Logistics',
    EDUCATION = 'Education',
    SALES = 'Sales',
    SCIENCE_AND_PHARMACEUTICALS = 'Science and Pharmaceuticals',
    SOCIAL_CARE = 'Social care',
    RETAIL = 'Retail',
    RECRUITMENT_AND_HR = 'Recruitment and HR',
    PUBLIC_SERVICES = 'Public services',
    PROPERTY_AND_CONSTRUCTION = 'Property and Construction',
    MEDIA_AND_INTERNET = 'Media and Internet',
    MARKETING_ADVERTISING_AND_PR = 'Marketing, Advertising and PR',
    LEISURE_SPORTS_AND_TOURISM = 'Leisure, Sports and Tourism',
    LAW_ENFORCEMENT_AND_SECURITY = 'Law Enforcement and Security',
    LAW = 'Law',
    INFORMATION_TECHONOLOGY = 'I.T',
    HOSPITALITY = 'Hospitality',
    ENGINEERING_AND_MANUFACTURING = 'Engineering and Manufacturing',
    ENERGY_AND_UTILITIES = 'Energy and Utilities',
    CREATIVE_ARTS_AND_DESIGN = 'Creative Arts and Design',
    CHARITY_AND_VOLUNTARY_WORK = 'Charity and Voluntary Work',
    BUSINSS_CONSULTING_MANAGEMENT = 'Business, Consulting and Management',
    ACCOUNTANCY_BANKING_FINANCE = 'Accountancy, Banking and Finance'
}

export type IndustryKey = keyof typeof Industry

type OrgQueryParamsType = {
  org_name: string
  industry: IndustryKey
  limit?: number
  offset?: number
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

  getOrg = async (id: number, review_limit?: number, interview_limit?: number, position?: string): Promise<OrgType> => {
    const params = { review_limit, interview_limit, position }
    const resp = await this.api.get(`/orgs/${id}`, { params })
    return resp.data.org
  }

  getOrgNames = async ({ industry, offset, limit }: Omit<OrgQueryParamsType, 'org_name'>): Promise<Pick<OrgType, 'name'| 'id'>[]> => {
    const params = { industry, limit, offset }
    const resp = await this.api.get('/orgs/get_names', { params })
    return resp.data.org_names
  }

  searchOrgs = async ({ org_name, industry, limit, offset }: OrgQueryParamsType): Promise<OrgType[]> => {
    const params = { org_name, industry, limit, offset }
    const resp = await this.api.get('/orgs/search', { params })
    return resp.data.orgs
  }
}
