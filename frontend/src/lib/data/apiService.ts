import axios from 'axios'
import type { AxiosInstance } from 'axios'

type OrgType = {
  name: string
  id: number
  created_at: number
  headquarters: string
  industry: string
  size: number
  url?: string
  reviews: any[]
  interviews: any[]
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

  getOrgs = async (): Promise<Pick<OrgType, 'name'| 'id'>[]> => {
    const resp = await this.api.get('/orgs/get_names')
    return resp.data.org_names
  }

  searchOrgs = async (org_name: string, limit?: number, offset?: number): Promise<OrgType[]> => {
    const params = { org_name }
    const resp = await this.api.get('/orgs/search', { params })
    return resp.data.orgs
  }
}
