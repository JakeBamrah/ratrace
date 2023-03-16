<script lang="ts">
  import Select from '../lib/Select.svelte'
  import { useNavigate } from 'svelte-navigator'

  import type { SelectRow } from '../App.svelte'
  import type { IndustryKey } from '../utils/apiService'
  import Button from '../lib/Button.svelte'
  import Link from '../lib/Link.svelte'


  export let selected_industry: SelectRow<IndustryKey>
  export let selected_org: SelectRow<number>
  export let industry_rows: SelectRow<IndustryKey>[]
  export let org_rows: SelectRow<number>[]
  export let loading_orgs: boolean
  export let filterOrgs: any
  export let onIndustrySelect: any

  const navigate = useNavigate()
</script>

<div class="flex flex-col items-center justify-center p-0 px-2 h-4/5 relative">
  <div class="w-80 sm:w-4/5 md:max-w-xl lg:max-w-2xl space-y-6">
    <p class="text-3xl text-grey-700 pl-1">ratrace.run</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
      <Select
        id="industry-filter-input-el"
        itemId="id"
        bind:value={selected_industry}
        placeholder="Search industries"
        clearable={false}
        focused={true}
        items={industry_rows}
        on:change={onIndustrySelect}
      />

      <Select
        id="company-filter-input-el"
        itemId="id"
        bind:value={selected_org}
        placeholder="Search companies"
        clearable={false}
        items={org_rows}
        disabled={!Boolean(selected_industry)}
        loading={loading_orgs}
        filter={filterOrgs}
      />
    </div>

      <div class="flex w-full justify-between items-center space-x-4 border-t border-grey-300 py-5">
        <p class="pl-1">
          Can't find a company?
          <Link on:click={() => navigate('/create-company')}>Create one</Link>
        </p>
        <Button disabled={!selected_org} on:click={() => navigate(`/org/${selected_org?.id}`)}>
          Search
        </Button>
      </div>
  </div>
</div>

