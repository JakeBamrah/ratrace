<script lang="ts">
  import { Router, Route } from 'svelte-navigator'
  import Home from './lib/Home.svelte'
  import Company from './routes/Company.svelte'
  import ApiService, { Industry } from './lib/data/apiService'
  import type { IndustryKey } from './lib/data/apiService'
  import type { SelectRow } from './lib/Dropdown.svelte'


  const api = new ApiService(import.meta.env.VITE_API_BASE_URL)

  let industry_filter = ""
  let company_filter = ""
  let selected_industry: SelectRow = null
  let selected_company: SelectRow = null

  let orgs = []
  const industries = Object.keys(Industry).map(k => ({id : k as IndustryKey, value: Industry[k]}))
  const onIndustrySelect = async (row: SelectRow) => {
    industry_filter = row.value
    selected_industry = row
    orgs = await api.getOrgNames({ industry: row.id as IndustryKey, limit: 10000 })
    return
  }

  const onCompanySelect = async (row: any) => {
    company_filter = row.value
    return
  }
</script>

<main>
  <Router primary={false} url="/">
    <Route path="org/*">
      <Route path=":id" let:params let:navigate>
        <Company id={params.id} navigate={navigate} />
      </Route>
    </Route>
    <Route>
        <Home
          bind:industry_filter={industry_filter}
          bind:company_filter={company_filter}
          onIndustrySelect={onIndustrySelect}
          onCompanySelect={onCompanySelect}
          industry_rows={industries}
          org_rows={orgs}
          selected_industry={selected_industry}
          selected_company={selected_company}
        />
    </Route>
  </Router>
</main>
