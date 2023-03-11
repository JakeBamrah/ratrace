<script lang="ts">
  import { useNavigate } from 'svelte-navigator'
  import { onMount } from 'svelte'
  import { string } from 'yup';

  import Input from '../lib/Input.svelte'
  import PageContainer from '../lib/PageContainer.svelte'
  import type { AccountQueryParams } from '../utils/apiService'
  import { validateYupValues } from '../utils/validators'
  import type { validationError } from '../utils/validators'


  export let onLogin: (params: AccountQueryParams) => Promise<boolean>

  const navigate = useNavigate()

  let username = ""
  let password = ""
  $: form_errors = {} as validationError
  let login_input: HTMLInputElement

  onMount(() => login_input.focus())

  const username_schema = string()
    .required("Username is a required field")
    .min(3, "Username must be 3 characters")
    .max(20, "Username allows 20 characters max")
  const password_schema = string()
    .required("Password is a required field")
    .min(8, "Password must be 8 characters")
    .max(64, "Password allows 64 characters max")
  const validation_schema = { username: username_schema, password: password_schema }

  const onSubmit = () => {
    const values = { username, password }
    const { has_errors, errors } = validateYupValues<AccountQueryParams>(values, validation_schema)

    form_errors = errors
    if (has_errors) {
      return
    }

    onLogin(values).then(authenticated => {
      if (authenticated)
        navigate('/')
    })
    return
  }
</script>

<div class="flex flex-col items-center justify-center p-0 px-2 h-4/5 relative">
  <PageContainer>
    <p class="text-3xl pb-2 pl-1">Login</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-1">
      <Input
        id="username-input"
        bind:value={username}
        placeholder="username"
        type="text"
        bind:ref={login_input}
        error={form_errors.username}
        />

      <Input
        id="password-input"
        bind:value={password}
        placeholder="password"
        type="password"
        error={form_errors.password}
        />
        <button on:click={onSubmit}>Login</button>
    </div>
  </PageContainer>
</div>

