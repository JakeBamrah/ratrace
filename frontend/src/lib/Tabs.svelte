<script lang="ts">
  export let onTabSelect: (tab: any) => void
  export let selected_tab: string
  export let tabs: string[]
</script>

<div class="flex space-x-2">
  {#each tabs as tab}
    <button
      class="
        px-3 py-1 rounded-full
        {selected_tab === tab ? 'bg-grey-300 text-white' : 'bg-transparent'}
      "
      on:click={() => onTabSelect(tab)}>
      {tab}
    </button>
  {/each}
</div>
