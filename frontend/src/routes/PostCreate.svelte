<script lang="ts">
  import { icons } from 'feather-icons'
  import Select from 'svelte-select'
  import { string } from 'yup';
  import { useNavigate } from 'svelte-navigator'

  import Input from '../lib/Input.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'
  import { account, Currency } from '../utils/apiService'
  import type { AccountQueryParams } from '../utils/apiService'
  import { validateYupValues } from '../utils/validators'
  import type { validationError } from '../utils/validators'


  export let positions: { id: number, label: string}[];
  let selected_position = null

  const navigate = useNavigate()

  const post_types = ["Review", "Interview"]
  const select_post_items = post_types.map(p => ({ id: p, label: p}))
  let selected_post = select_post_items[0]
  $: is_review = selected_post.id === 'Review'

  const currencies = Object.keys(Currency).map(k => ({ id: k, label: Currency[k] }))
  let selected_currency = currencies[0]

  let post = ""

  let username = ""
  let password = ""
  $: form_errors = {} as validationError
  let login_input: HTMLInputElement

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

    return
  }
</script>

<div class="flex w-full grid grid-cols-3 sm:grid-cols-6 gap-3 pt-4 pb-2">
  <div class="col-span-6 sm:col-span-3 ">
    <Select
      items={select_post_items}
      bind:value={selected_post}
      clearable={false}
      searchable={false}
      itemId='id' />
  </div>
  <div class="col-span-6 sm:col-span-3 ">
    <Input
      id="username-input"
      bind:value={username}
      placeholder="location"
      type="text"
      bind:ref={login_input}
      error={Boolean(form_errors.username)}
    />
  </div>

  <div class="col-span-6 sm:col-span-3 ">
    <div class="flex items-center space-x-1">
      <Select
        items={positions}
        bind:value={selected_position}
        placeholder="position"
        clearable={false}
        itemId='id' />
        <button 
          on:click={() => "disable select and replace with text input"}
          class="rounded-lg p-1 hover:bg-grey-100 text-grey-400">
          {@html icons.plus.toSvg({ class: 'h-6 w-6'})}
        </button>
      </div>
  </div>
  <div class="col-span-6 sm:col-span-3">
    <Input
      id="username-input"
      bind:value={username}
      placeholder={ is_review ? "Tenure" : "Stages" }
      type="text"
      bind:ref={login_input}
      error={Boolean(form_errors.username)}
    />
  </div>

  <div class="col-span-6 flex space-x-3">
    <div class="w-1/3 sm:w-1/2">
      <Select
        items={currencies}
        bind:value={selected_currency}
        clearable={false}
        itemId='id' />
    </div>
    <div class="w-2/3 sm:w-1/2">
      <Input
        id="username-input"
        bind:value={username}
        placeholder={ is_review ? "Salary" : "Offer" }
        type="text"
        bind:ref={login_input}
        error={Boolean(form_errors.username)}
      />
    </div>
  </div>

  <div class="col-span-6">
    <textarea
      name="textarea"
      bind:value={post}
      placeholder={ is_review ? "Review" : "Interview" }
      class="border p-3 rounded-xl w-full h-24 resize-none"></textarea>
  </div>
</div>
