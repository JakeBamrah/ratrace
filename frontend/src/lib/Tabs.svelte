<script lang="ts">
  type Tab = { id: any, value: string }
  export let onTabSelect: (tab: Tab) => void
  export let selected_tab: Tab
  export let left_tabs: Tab[] = []
</script>

<div class="flex justify-between w-full">
  <div class="flex space-x-2">
    {#each left_tabs as tab}
      <button
        class="
          hover:bg-grey-100 px-3 py-2 rounded-full
          {selected_tab.id === tab.id ? 'bg-grey-100' : 'bg-transparent'}
        "
        on:click={() => onTabSelect(tab)}>
        {tab.value}
      </button>
    {/each}
  </div>

  <div class="flex space-x-2">
    <slot name="symbols">
    </slot>
  </div>
</div>
