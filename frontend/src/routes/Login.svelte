<script lang="ts">
  import { useNavigate } from 'svelte-navigator'
  import { onMount } from 'svelte'
  import { string } from 'yup';

  import Input from '../lib/Input.svelte'
  import Button from '../lib/Button.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'
  import { authenticated } from '../utils/apiService'
  import type { Account, AccountQueryParams } from '../utils/apiService'
  import { validateYupValues } from '../utils/validators'
  import type { validationError } from '../utils/validators'


  export let onLogin: (params: AccountQueryParams) => Promise<{ account?: Account, error?: string, authenticated: boolean }>

  const navigate = useNavigate()

  let username = ""
  let password = ""
  $: form_errors = {} as validationError
  let login_input: HTMLInputElement

  onMount(() => {
    login_input.focus()

    if ($authenticated) {
      navigate('/')
    }
  })

  const username_schema = string()
    .required("Username is a required field")
    .min(3, "Username must be 3 characters")
    .max(20, "Username allows 20 characters max")
    .typeError("Must be a string")
  const password_schema = string()
    .required("Password is a required field")
    .min(8, "Password must be 8 characters")
    .max(64, "Password allows 64 characters max")
    .typeError("Must be a string")
  const validation_schema = { username: username_schema, password: password_schema }

  let error_message: string = null
  let submit_disabled = false
  const onSubmit = () => {
    const values = { username, password }
    const { has_errors, errors } = validateYupValues<AccountQueryParams>(values, validation_schema)

    form_errors = errors
    if (has_errors) {
      return
    }

    submit_disabled = true
    onLogin(values).then(resp => {
      if (!resp.authenticated) {
        error_message = resp.error
        return
      }

      navigate('/')
    })
    submit_disabled = false
    return
  }
</script>

<div
  class="
    flex flex-col items-center justify-center w-full
    p-0 px-2 h-4/5 relative
  ">
    <p class="text-2xl text-grey-700 pb-4 pl-1">Login</p>
    <div class="grid grid-cols-1 gap-6 w-80">
      <Input
        id="username-input"
        bind:value={username}
        placeholder="Username"
        label="Username"
        type="text"
        bind:ref={login_input}
        error={Boolean(form_errors.username)}
        errorMessage={form_errors.username}
      />

      <Input
        id="password-input"
        bind:value={password}
        placeholder="Password"
        label="Password"
        type="password"
        error={Boolean(form_errors.password)}
        errorMessage={form_errors.password}
      />
      <div class="flex justify-between items-center w-full border-t border-grey-300 py-5">
        <p class="text-red-400">{ error_message ? `(${error_message})` : ''}</p>
        <div class="flex space-x-4">
          <SecondaryButton on:click={() => navigate('/')}>Back</SecondaryButton>
          <Button on:click={onSubmit}>Login</Button>
        </div>
      </div>
    </div>
</div>
