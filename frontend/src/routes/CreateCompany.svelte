<script lang="ts">
  import { useNavigate } from 'svelte-navigator'
  import { onMount } from 'svelte'
  import { string, number } from 'yup';

  import type { SelectRow } from '../App.svelte'
  import Input from '../lib/Input.svelte'
  import Select from '../lib/Select.svelte'
  import Button from '../lib/Button.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'
  import { authenticated } from '../utils/apiService'
  import type { IndustryKey, OrgQueryParamsType } from '../utils/apiService'
  import { validateYupValues, castYupValues } from '../utils/validators'
  import type { validationError } from '../utils/validators'


  export let onCompanyCreate: (params: OrgQueryParamsType) => Promise<{ error?: string }>
  export let industry_rows: SelectRow<IndustryKey>[]

  const navigate = useNavigate()

  let org_name = ""
  let size = ""
  let headquarters = ""
  let url = ""

  let selected_industry = industry_rows[0]

  $: form_errors = {} as validationError
  let name_input: HTMLInputElement

  const org_name_schema = string()
    .required("Company name is required")
    .min(3, "Must be 3 characters min")
    .max(30, "Must be 30 characters max")
    .typeError("Must be a string")
  const size_schema = number()
    .positive("Must be positive")
    .lessThan(100 * 1000, "Must be less than 6 digits")
    .typeError("Must be a number")
  const headquarters_schema = string()
    .required("HQ is required")
    .min(3, "Must be 3 characters min")
    .max(30, "Must be 30 characters max")
    .typeError("Must be a string")
  const url_schema = string()
    .typeError("Must be a string")
  const validation_schema = {
    org_name: org_name_schema,
    size: size_schema,
    headquarters: headquarters_schema,
    url: url_schema
  }

  let error_message: string = null
  let submit_disabled = false
  const onSubmit = () => {
    const values = {
      org_name,
      size,
      headquarters,
      url
    }

    let { has_errors, errors } = validateYupValues<OrgQueryParamsType>(values, validation_schema)
    form_errors = errors
    if (has_errors) {
      return
    }

    submit_disabled = true
    let cast_values = castYupValues(values, validation_schema)
    onCompanyCreate({...cast_values, industry: selected_industry.id} as any).then(resp => {
      // if name is already taken, assign error to username form-errors
      console.log(resp)
      const is_company_name_error = resp.error?.toLowerCase().includes('name')
      if (is_company_name_error) {
        form_errors.org_name = resp.error
        return
      }

      // otherwise just create an error message for underneath form
      if (resp.error) {
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
    <p class="text-2xl text-grey-700 pb-2 pl-1">Sign-up</p>
    <div class="grid grid-cols-1 space-y-6 w-80">
      <Input
        id="org-name-input"
        label="Company name*"
        bind:value={org_name}
        placeholder="Company name"
        type="text"
        bind:ref={name_input}
        error={Boolean(form_errors.org_name)}
        errorMessage={form_errors.org_name}
      />
      <Input
        id="size-input"
        label="Size*"
        bind:value={size}
        placeholder="Size"
        type="text"
        error={Boolean(form_errors.size)}
        errorMessage={form_errors.size}
      />
      <Input
        id="headquarters-input"
        label="Headquarters*"
        bind:value={headquarters}
        placeholder="Headquarters"
        type="text"
        error={Boolean(form_errors.headquarters)}
        errorMessage={form_errors.headquarters}
      />
      <Input
        id="url-input"
        label="Company url"
        bind:value={url}
        placeholder="Url"
        type="text"
        error={Boolean(form_errors.url)}
        errorMessage={form_errors.url}
      />
      <Select
        id="industry-filter-input-el"
        itemId="id"
        bind:value={selected_industry}
        label="Industry*"
        placeholder="Search industries"
        clearable={false}
        items={industry_rows}
      />
      <div
        class="
          flex justify-between items-center w-full
          border-t border-grey-300 py-5
        ">
        <p class="text-red-400">{ error_message ? `(${error_message})` : ''}</p>
        <div class="flex space-x-4">
          <SecondaryButton on:click={() => navigate('/')}>Back</SecondaryButton>
          <Button
            disabled={submit_disabled}
            on:click={onSubmit}>
            Submit company
          </Button>
        </div>
      </div>
    </div>
</div>
