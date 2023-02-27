<script lang="ts">
  import Dropdown from './Dropdown.svelte'
  import type { SelectRow } from './Dropdown.svelte'
  import type { IndustryKey } from './data/apiService'


  export let onIndustrySelect: (args: any) => any
  export let onCompanySelect: (args: any) => any
  export let industry_filter: string
  export let company_filter: string
  export let industry_rows: { id: IndustryKey, value: string }[]
  export let org_rows: SelectRow[]
  export let selected_industry: SelectRow
  export let selected_company: SelectRow
</script>

<div class="flex flex-col items-center justify-center p-0 sm:items-start sm:pl-24 h-screen">
  <div class="w-80 sm:w-4/5 md:max-w-xl lg:max-w-2xl">
    <p class="text-3xl pb-2 pl-1">ratrace.run</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-1">
      <Dropdown
        id="industry-filter-input-el"
        bind:value={industry_filter}
        bind:selected_value={selected_industry}
        placeholder="Select industry"
        use_window_shortcut={true}
        rows={industry_rows}
        onSelect={onIndustrySelect}
        focus_input_on_mount={true}
      />

      <Dropdown
        id="company-filter-input-el"
        bind:value={company_filter}
        bind:selected_value={selected_company}
        placeholder="Search companies"
        rows={org_rows}
        onSelect={onCompanySelect}
      />
    </div>
  </div>
</div>

