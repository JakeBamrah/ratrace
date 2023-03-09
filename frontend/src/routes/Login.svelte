<script lang="ts">
  import { useNavigate } from 'svelte-navigator'

  import PageContainer from '../lib/PageContainer.svelte'
  import Input from '../lib/Input.svelte'

  const navigate = useNavigate()
  let login = ""
  let password = ""
</script>

<div class="flex flex-col items-center justify-center p-0 px-2 h-4/5 relative">
  <PageContainer>
    <p class="text-3xl pb-2 pl-1">Login</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-1">
      <Input
        value={login}
        placeholder="username" />
      <Input
        value={password}
        placeholder="password" />
    </div>
  </PageContainer>
</div>


