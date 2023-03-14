<script lang="ts">
  import Select from 'svelte-select'
  import { useNavigate } from 'svelte-navigator'
  import { icons } from 'feather-icons'

  import type { SelectRow } from '../App.svelte'
  import type { IndustryKey } from '../utils/apiService'
  import Button from '../lib/Button.svelte'


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
  <div class="w-80 sm:w-4/5 md:max-w-xl lg:max-w-2xl">
    <p class="text-3xl pb-2 pl-1">ratrace.run</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-1">
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

    <div class="DESKTOP_BUTTON flex justify-end w-full pt-3">
      <Button on:click={() => navigate(`/org/${selected_org?.id}`)}>
        Search
      </Button>
    </div>

  </div>
</div>

