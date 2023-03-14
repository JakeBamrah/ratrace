<script lang="ts">
  import { icons } from 'feather-icons'
  import Select from 'svelte-select'
  import { string, number } from 'yup';
  import { useNavigate } from 'svelte-navigator'

  import Input from '../lib/Input.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'
  import { account, Currency, Rating, PostEnum } from '../utils/apiService'
  import type { PostQueryParams, onPostType } from '../utils/apiService'
  import { validateYupValues, castYupValues } from '../utils/validators'
  import type { validationError } from '../utils/validators'


  export let onPost: onPostType
  export let positions: { id: number, label: string}[];

  let selected_position = positions.length > 0 ? positions[0] : null
  let creating_new_position = positions.length === 0

  const navigate = useNavigate()

  const posts = Object.keys(PostEnum).map(k => ({ id: k, label: PostEnum[k] }))
  let selected_post = posts[0]
  $: is_review = selected_post.id === PostEnum.REVIEW.toUpperCase()

  const currencies = Object.keys(Currency).map(k => ({ id: k, label: Currency[k] }))
  let selected_currency = currencies[0]

  // build tag objects but remove ALL selection as it is not a valid rating
  const tag_objs = Object.keys(Rating).map(k => ({ id: k, label: Rating[k] }))
  const tags = tag_objs.filter(t => t.id !== 'ALL')
  let selected_tag = tags[0]

  let tenure_stages = "1"
  let work_location = ""
  let compensation = "0"
  let post = ""
  let new_position = ""

  $: form_errors = {} as validationError

  const tenure_stages_schema = number()
    .positive("Tenure must be a positive number")
    .lessThan(50, "Compensation should be less than 50")
  const compensation_schema = number()
    .moreThan(-1, "Compensation must zero or more")
    .lessThan(10 * 1000000, "Compensation should be less than 8 digits")
  const position_schema = string()
    .required("Position is a required field")
    .min(2, "Position must be 2 characters")
    .max(32, "Position allows 32 characters max")
  const work_location_schema = string()
  const post_schema = string()
    .required("Post is required")
    .max(2000, "Post allows 2000 characters max")
  const validation_schema = {
    tenure_stages: tenure_stages_schema,
    compensation: compensation_schema,
    position: position_schema,
    location: work_location_schema,
    post: post_schema
  }

  let submit_disabled = false
  const onSubmit = async () => {
    if (!$account.id)
      return

    const values = {
      // pass existing position to validation if chosen (keeps everything happy)
      position: creating_new_position ? new_position : selected_position?.label,
      location: work_location,
      tenure_stages,
      compensation,
      post
    }
    const { has_errors, errors } = validateYupValues<any>(values, validation_schema)

    form_errors = errors
    if (has_errors) {
      return
    }

    let cast_values = castYupValues(values, validation_schema)
    const params = {
      ...cast_values,
      position_id: new_position ? null : selected_position?.id,
      tag: selected_tag.id,
      currency: selected_currency.id,
      post_type: selected_post.id
    }

    // prevent double spending, make sure button is disabled on submit
    submit_disabled = true
    await onPost(params as PostQueryParams).then(r => console.log(r))
    submit_disabled = false
    return
  }
</script>

<div>
  {#if $account?.id}
    <div class="flex w-full grid grid-cols-3 sm:grid-cols-6 gap-3 pt-4 pb-2">
      <div class="col-span-6 sm:col-span-3 ">
        <Select
          items={posts}
          bind:value={selected_post}
          clearable={false}
          searchable={false}
          itemId='id' />
      </div>
      <div class="col-span-6 sm:col-span-3 ">
        <Input
          id="location-input"
          bind:value={work_location}
          placeholder="location"
          type="text"
          error={Boolean(form_errors.work_location)}
        />
      </div>

      <div class="col-span-6 sm:col-span-3 ">
        <div class="flex items-center space-x-1">
          {#if creating_new_position}
            <Input
              id="new-position-input"
              bind:value={new_position}
              placeholder="new position name"
              type="text"
              error={Boolean(form_errors.position)}
            />
          {:else}
            <Select
              items={positions}
              bind:value={selected_position}
              clearable={false}
              itemId='id' />
            {/if}
            <button
              on:click={() => creating_new_position = !creating_new_position}
              class="
                rounded-lg p-1 hover:bg-grey-100 text-grey-500
                { creating_new_position ? 'bg-grey-100' : '' }
              ">
              {@html icons.plus.toSvg({ class: 'h-6 w-6'})}
            </button>
          </div>
      </div>
      <div class="col-span-6 sm:col-span-3">
        <Input
          id="tenure-stages-input"
          bind:value={tenure_stages}
          placeholder={ is_review ? "Tenure" : "Stages" }
          type="text"
          error={Boolean(form_errors.tenure_stages)}
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
        <div class="w-1/3">
          <Input
            id="compensation-input"
            bind:value={compensation}
            placeholder={ is_review ? "Salary" : "Offer" }
            type="text"
            error={Boolean(form_errors.compensation)}
          />
        </div>
        <div class="w-1/3">
          <Select
            items={tags}
            bind:value={selected_tag}
            clearable={false}
            itemId='id' />
        </div>
      </div>

      <div class="col-span-6">
        <Input
          id="post-input"
          bind:value={post}
          placeholder={ is_review ? "Review" : "Interview" }
          text_area={true}
          error={Boolean(form_errors.post)} />
      </div>
    </div>
    <div class="flex w-full justify-end">
      <button disabled={submit_disabled} on:click={onSubmit}>Submit</button>
    </div>
  {:else}
    <div class="flex items-center justify-center pt-4">
      <p>
        You must
        <button
          class="hover:underline text-grey-400"
          on:click={() => navigate('/login')}>
          login
        </button>
        to post
      </p>
    </div>
  {/if}
</div>
