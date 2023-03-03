<script lang="ts">
  import { Router, Route } from 'svelte-navigator'
  import Home from './lib/Home.svelte'
  import Company from './routes/Company.svelte'
  import ApiService, { Industry } from './lib/data/apiService'
  import type { IndustryKey } from './lib/data/apiService'
  import type { SelectRow } from './lib/Dropdown.svelte'


  const api = new ApiService(import.meta.env.VITE_API_BASE_URL)
  let selected_org: SelectRow
  let selected_industry: SelectRow
  let orgs = []
  let loading = false
  const industries = Object.keys(Industry).map(k => ({value : k as IndustryKey, label: Industry[k]}))

  $: fetch = onIndustrySelect(selected_industry)

  const onIndustrySelect = async (selected_industry: SelectRow) => {
    if (!selected_industry) {
      orgs = []
      return
    }

    const params = { industry: selected_industry?.value as IndustryKey, limit: 10000 }
    selected_org = null
    loading = true
    api.getOrgNames(params).then(resp => {orgs = resp; loading = false})
    return
  }

  const getOrg = async (org_id: number) => {
    const params = { org_id }
    return await api.getOrg(params)
  }

</script>

<main>
  <Router primary={false} url="/">
    <Route path="org/*">
      <Route path=":id" let:params let:navigate>
        <Company id={params.id} navigate={navigate} getOrg={getOrg} />
      </Route>
    </Route>
    <Route let:navigate>
        <Home
          bind:selected_industry={selected_industry}
          bind:selected_org={selected_org}
          industry_rows={industries}
          org_rows={orgs}
          loading_orgs={loading}
          navigate={navigate}
        />
    </Route>
  </Router>
</main>
