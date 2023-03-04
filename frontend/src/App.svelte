<script lang="ts">
  import Index from 'flexsearch/src/index';
  import { Router, Route } from 'svelte-navigator'

  import Home from './routes/Home.svelte'
  import Company from './routes/Company.svelte'
  import ApiService, { Industry } from './lib/data/apiService'
  import type { IndustryKey } from './lib/data/apiService'
  import type { SelectRow } from './lib/Dropdown.svelte'
  import { createFilter } from './utils/search'


  const api = new ApiService(import.meta.env.VITE_API_BASE_URL)
  let selected_org: SelectRow<number>
  let selected_industry: SelectRow<IndustryKey>
  let orgs = []
  let loading = false
  const industries = Object.keys(Industry).map(k => ({id : k as IndustryKey, label: Industry[k]}))

  $: fetch = onIndustrySelect(selected_industry)

  const org_search_idx = new Index("performance")
  const onIndustrySelect = async (selected_industry: SelectRow<IndustryKey>) => {
    if (!selected_industry) {
      orgs = []
      return
    }

    selected_org = null
    loading = true
    const params = {
      industry: selected_industry?.id as IndustryKey,
      limit: 10000
    }
    api.getOrgNames(params).then(resp => {
      loading = false

      // limit the number of orgs to render in the dropdown
      // the search index will keep track of *all* available orgs for us
      orgs = resp.length > 500 ? resp.slice(0, 500) : resp

      // flex-search needs to use the same index id as our dropdown component
      // which relies on the array index rather than the item.id
      resp.forEach((o, idx) => org_search_idx.add(idx, o.label))
    })
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
          filterOrgs={createFilter(org_search_idx)}
        />
    </Route>
  </Router>
</main>
