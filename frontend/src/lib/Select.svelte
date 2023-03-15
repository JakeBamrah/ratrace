<script lang="ts">
  import Select from 'svelte-select'
  import { default_filter } from '../utils/search'

  export let id: string = null
  export let itemId: string = null
  export let value: any = null
  export let placeholder: string = null
  export let clearable: boolean = false
  export let focused: boolean = false
  export let disabled: boolean = false
  export let searchable: boolean = true
  export let loading: boolean = false
  export let items: any[]
  export let filter: any = default_filter
  export let label: string = null

  // we define a separate select component so that styles can remain consistent
</script>

<div class="w-full">
  {#if label}
    <p class="text-xs font-extralight pb-1 text-grey-400">{label}</p>
  {/if}
  <Select
    id={id}
    itemId={itemId}
    bind:value={value}
    placeholder={placeholder}
    clearable={clearable}
    focused={focused}
    disabled={disabled}
    searchable={searchable}
    loading={loading}
    filter={filter}
    items={items}
    on:change
    class="
      !border-grey-100 !bg-grey-100 !rounded-lg !text-grey-700
      !placeholder:text-xs !font-light
    "
    --height="2.375rem"
    --font-size="0.875rem"
    --placeholder-color="#b0b0b0"
    --disabled-placeholder-color="#d1d5db"
  />
</div>
