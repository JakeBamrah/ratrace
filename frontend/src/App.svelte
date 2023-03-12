<script lang="ts" context="module">
  export type SelectRow<T> = {
    id: T
    label: string
  }
</script>

<script lang="ts">
  import Index from 'flexsearch/src/index';
  import { Router, Route } from 'svelte-navigator'
  import { onMount } from 'svelte'

  import Home from './routes/Home.svelte'
  import Company from './routes/Company.svelte'
  import ApiService, { Industry } from './utils/apiService'
  import type { OrgQueryParamsType, AccountQueryParams } from './utils/apiService'
  import Login from './routes/Login.svelte'
  import CreateAccount from './routes/CreateAccount.svelte'
  import Account from './routes/Account.svelte'
  import Navbar from './routes/Navbar.svelte'
  import type { IndustryKey } from './utils/apiService'
  import { createFilter } from './utils/search'


  const api = new ApiService(import.meta.env.VITE_API_BASE_URL)
  let selected_org: SelectRow<number>
  let selected_industry: SelectRow<IndustryKey>
  let orgs = []
  let loading = false
  const industries = Object.keys(Industry).map(k => ({id : k as IndustryKey, label: Industry[k]}))

  const org_search_idx = new Index("performance")
  const onIndustrySelect = async () => {
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

      // NOTE: limit the number of orgs to render in the dropdown (see org_rows)
      // the search index will keep track of *all* available orgs for us
      orgs = resp

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

  const getOrgReviewsAndInterviews = async (params: OrgQueryParamsType) => {
    return await api.getOrgReviewsAndInterviews(params)
  }

  let account = null
  const onLogin = async (params: AccountQueryParams) => {
    const resp = await api.login(params)
    if (resp.authenticated) {
      account = resp.account
    }

    return resp.authenticated
  }

  const onLogout = async () => {
    api.logout().then(r => {
      if (!r.authenticated)
        account = null
    })
    return
  }

  const onSignUp = async (params: AccountQueryParams) => {
    const resp = await api.signup(params)
    if (!resp.error)
      account = resp.account

    return Boolean(resp.error)
  }

  onMount(async () => {
    const resp = await api.checkLogin()
    if (resp.authenticated) {
      account = resp.account
    }
  })
</script>

<main>
  <div class="pb-10 h-screen">
    <Router primary={false} url="/">
      <Navbar authenticated={Boolean(account)}/>
      <Route path="/login">
        <Login onLogin={onLogin} />
      </Route>
      <Route path="/signup">
        <CreateAccount onSignUp={onSignUp} />
      </Route>
      <Route path="/account">
        <Account onLogout={onLogout} />
      </Route>
      <Route path="org/*">
        <Route path=":id" let:params>
          <Company
            id={params.id}
            getOrg={getOrg}
            getReviewsAndInterviews={getOrgReviewsAndInterviews}
          />
        </Route>
      </Route>
      <Route>
        <Home
          bind:selected_industry={selected_industry}
          bind:selected_org={selected_org}
          industry_rows={industries}
          org_rows={orgs.length > 500 ? orgs.slice(0, 500) : orgs}
          loading_orgs={loading}
          filterOrgs={createFilter(org_search_idx, orgs)}
          onIndustrySelect={onIndustrySelect}
        />
      </Route>
    </Router>
  </div>
</main>
