<script lang="ts">
  import { useNavigate } from 'svelte-navigator'
  import { onMount } from 'svelte'
  import { string } from 'yup';

  import Input from '../lib/Input.svelte'
  import Button from '../lib/Button.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'
  import type { AccountQueryParams } from '../utils/apiService'
  import { validateYupValues } from '../utils/validators'
  import type { validationError } from '../utils/validators'


  export let onSignUp: (params: AccountQueryParams) => Promise<Boolean>

  const navigate = useNavigate()

  let username = ""
  let password = ""
  let reenter_password = ""
  $: form_errors = {} as validationError
  let username_input: HTMLInputElement

  onMount(() => {
    username_input.focus()
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

  let submit_disabled = false
  const onSubmit = () => {
    const values = { username, password }
    let { has_errors, errors } = validateYupValues<AccountQueryParams>(values, validation_schema)

    form_errors = errors
    if (password != reenter_password) {
      form_errors['reenter_password'] = "Passwords do not match"
      has_errors = true
    }

    if (has_errors) {
      return
    }

    submit_disabled = true
    onSignUp(values).then(err => {
      if (!err)
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
    <p class="text-2xl text-grey-700 pb-2 pl-1">Sign-up</p>
    <div class="grid grid-cols-1 space-y-6 w-80">
      <Input
        id="username-input"
        label="Username*"
        bind:value={username}
        placeholder="Username"
        type="text"
        bind:ref={username_input}
        error={Boolean(form_errors.username)}
        errorMessage={form_errors.username}
      />
      <Input
        id="password-input"
        label="Password*"
        bind:value={password}
        placeholder="Password"
        type="password"
        error={Boolean(form_errors.password)}
        errorMessage={form_errors.password}
      />
      <Input
        id="reenter-password-input"
        label="Re-enter password*"
        bind:value={reenter_password}
        placeholder="Re-enter password"
        type="password"
        error={Boolean(form_errors.reenter_password)}
        errorMessage={form_errors.reenter_password}
      />
      <div class="flex w-full justify-end space-x-4 border-t border-grey-300 py-5">
        <SecondaryButton on:click={() => navigate('/')}>Back</SecondaryButton>
        <Button
          disabled={submit_disabled}
          on:click={onSubmit}>
          Create account
        </Button>
      </div>
    </div>
</div>
