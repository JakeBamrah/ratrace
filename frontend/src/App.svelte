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
  import ApiService, { Industry, authenticated } from './utils/apiService'
  import type { OrgQueryParamsType } from './utils/apiService'
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
  let loading_orgs = false
  const industries = Object.keys(Industry).map(k => ({id : k as IndustryKey, label: Industry[k]}))

  const org_search_idx = new Index("performance")
  const onIndustrySelect = async () => {
    if (!selected_industry) {
      orgs = []
      return
    }

    selected_org = null
    loading_orgs = true
    const params = {
      industry: selected_industry?.id as IndustryKey,
      limit: 10000
    }
    api.getOrgNames(params).then(resp => {
      loading_orgs = false

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

  let loading_app = true
  onMount(async () => {
    // authenticate each page load
    await api.authenticate()
    loading_app = false
  })
</script>

<main>
  <div class="pb-10 h-screen">
    {#if loading_app}
      <div class="EMPTY_PLACEHOLDER_TO_STOP_FLICKERING"></div>
    {:else}
      <Router primary={false} url="/">
        <Navbar authenticated={$authenticated}/>
        <Route path="/login">
          <Login onLogin={api.login} />
        </Route>
        <Route path="/signup">
          <CreateAccount onSignUp={api.signup} />
        </Route>
        <Route path="/account">
          <Account
            onAccountUpdate={api.accountUpdate}
            onLogout={api.logout} />
        </Route>
        <Route path="org/*">
          <Route path=":id" let:params>
            <Company
              id={params.id}
              onGetOrg={getOrg}
              onGetOrgPosts={api.getOrgPosts}
              onVote={api.vote}
              onPost={api.post}
              onDeletePost={api.deletePost}
            />
          </Route>
        </Route>
        <Route>
          <Home
            bind:selected_industry={selected_industry}
            bind:selected_org={selected_org}
            industry_rows={industries}
            org_rows={orgs.length > 500 ? orgs.slice(0, 500) : orgs}
            loading_orgs={loading_orgs}
            filterOrgs={createFilter(org_search_idx, orgs)}
            onIndustrySelect={onIndustrySelect}
          />
        </Route>
      </Router>
    {/if}
  </div>
</main>
