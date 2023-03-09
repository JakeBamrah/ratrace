<script lang="ts">
  import { useNavigate } from 'svelte-navigator'

  import PageContainer from '../lib/PageContainer.svelte'
  import Input from '../lib/Input.svelte'

  const navigate = useNavigate()
  let login = ""
  let password = ""
  let verify_password = ""
</script>

<div class="flex flex-col items-center justify-center p-0 px-2 h-4/5 relative">
  <PageContainer>
    <p class="text-3xl pb-2 pl-1">Create account</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-1">
      <Input
        value={login}
        placeholder="username" />
      <Input
        value={password}
        placeholder="password" />
      <Input
        value={verify_password}
        placeholder="verify password" />
    </div>
  </PageContainer>
</div>


