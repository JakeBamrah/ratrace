<script lang="ts">
  type Tab = { id: any, value: string }
  export let onTabSelect: (tab: Tab) => void
  export let selected_tab: Tab
  export let left_tabs: Tab[] = []
  export let symbols: Tab[] = []
</script>

<div class="flex justify-between w-full">
  <div class="flex space-x-2">
    {#each left_tabs as tab}
      <button
        class="
          px-3 py-1 rounded-full
          {selected_tab.id === tab.id ? 'bg-grey-300 text-white' : 'bg-transparent'}
        "
        on:click={() => onTabSelect(tab)}>
        {tab.value}
      </button>
    {/each}
  </div>

  <div class="flex space-x-2">
    {#each symbols as tab}
      <button
        class="
          p-1.5 rounded-full
          {selected_tab.id === tab.id ? 'bg-grey-300 text-white' : 'bg-transparent'}
        "
        on:click={() => onTabSelect(tab)}>
        {@html tab.value}
      </button>
    {/each}
  </div>
</div>
