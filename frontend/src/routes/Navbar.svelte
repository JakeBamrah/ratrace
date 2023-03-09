<script lang="ts">
  import PageContainer from '../lib/PageContainer.svelte'
  import { useNavigate } from 'svelte-navigator'

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
        <button on:click={() => navigate('/')}>
          About
        </button>
        <button on:click={() => navigate('/login')}>
          Login
        </button>
      </div>
    </div>
  </div>
</PageContainer>

