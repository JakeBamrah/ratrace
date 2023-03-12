<script lang="ts">
  import PageContainer from '../lib/PageContainer.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'
  import { useNavigate } from 'svelte-navigator'


  export let authenticated: Boolean = false

  const navigate = useNavigate()
</script>

<PageContainer>
  <div class="w-full py-10 sm:py-8 px-2 relative">
    <div class="flex justify-between items-center">
      <div>
          <button
            class="rounded-full bg-grey-200 h-12 w-12"
            on:click={() => navigate('/')} />
      </div>
      <div class="space-x-4 sm:space-x-2 z-1">
        <SecondaryButton on:click={() => navigate('/')}>
          About
        </SecondaryButton>
        {#if authenticated}
          <button class="hover:underline" on:click={() => navigate('/account')}>
            Account
          </button>
        {:else}
          <button on:click={() => navigate('/login')}>
            Login
          </button>
        {/if}
      </div>
    </div>
  </div>
</PageContainer>

