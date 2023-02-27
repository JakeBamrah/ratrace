<script lang="ts">
  import { onMount } from 'svelte'

  import Input from './Input.svelte'


  export let getOrgs: () => any

  let company_filter = ""
  let position_filter = ""
  let company_input_el: HTMLInputElement

  onMount(async () => {
    company_input_el.focus()
    console.log(getOrgs())
  })
</script>

<div class="flex flex-col items-center justify-center p-0 sm:items-start sm:pl-24 h-screen">
  <div class="w-80 sm:w-4/5 md:max-w-xl lg:max-w-2xl">
    <p class="text-3xl pb-2 pl-1">ratrace.run</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-1">
      <Input
        id="company-filter-input-el"
        bind:value={company_filter}
        placeholder="Search companies"
        use_window_shortcut={true}
        bind:ref={company_input_el}
      />

      <Input
        id="position-filter-input-el"
        bind:value={position_filter}
        placeholder="Search positions"
      />
    </div>
  </div>
</div>

