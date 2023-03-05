<script lang="ts">
  import PageContainer from '../lib/PageContainer.svelte'

  export let navigate: any
</script>

<PageContainer>
  <div class="w-full py-10 sm:py-8">
    <div class="flex justify-between">
      <button on:click={() => navigate('/')}>
        ratrace
      </button>
      <div class="space-x-4 sm:space-x-2">
      <button on:click={() => navigate('/')}>
        About
      </button>
      <button on:click={() => navigate('/')}>
        Login
      </button>
      </div>
    </div>
  </div>
</PageContainer>

