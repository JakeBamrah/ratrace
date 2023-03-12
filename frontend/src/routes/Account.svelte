<script lang="ts">
  import { useNavigate } from 'svelte-navigator'
  import { onMount } from 'svelte'

  import PageContainer from '../lib/PageContainer.svelte'
  import type { AccountQueryParams } from '../utils/apiService'


  export let onLogout: () => void

  const navigate = useNavigate()

  const handleLogout = () => {
    onLogout()
    navigate('/')
  }

  // check if account has access and pull in account data on mount
  //onMount(() => login_input.focus())
</script>

<div class="flex flex-col items-center justify-center p-0 px-2 h-4/5 relative">
  <PageContainer>
    <button on:click={handleLogout}>Logout</button>
  </PageContainer>
</div>
