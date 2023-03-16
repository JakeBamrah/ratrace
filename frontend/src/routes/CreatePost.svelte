<script lang="ts">
  import DOMPurify from 'dompurify'
  import { Plus } from 'lucide-svelte';
  import { marked } from 'marked'
  import Select from '../lib/Select.svelte'
  import { string, number } from 'yup';
  import { useNavigate } from 'svelte-navigator'

  import Input from '../lib/Input.svelte'
  import Link from '../lib/Link.svelte'
  import Button from '../lib/Button.svelte'
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

  // preview post as markdown config
  let preview_post = false
  const sanitize_config = { USE_PROFILES: { html: true } }

  // form validation and parsing
  let tenure_stages = "1"
  let work_location = ""
  let compensation = "0"
  let post = ""
  let new_position = ""

  $: form_errors = {} as validationError

  const tenure_stages_schema = number()
    .positive("Must be a positive number")
    .lessThan(50, "Must be less than 50")
    .typeError("Must be a number")
  const compensation_schema = number()
    .moreThan(-1, "Must be > 0")
    .lessThan(10 * 1000000, "Must be less than 8 digits")
    .typeError("Must be a number")
  const position_schema = string()
    .required("Position is a required")
    .min(2, "Must be 2 characters or greater")
    .max(32, "Must be 32 characters or less")
    .typeError("Must be a string")
  const work_location_schema = string()
  const post_schema = string()
    .required("Post is required")
    .max(2000, "Post allows 2000 characters max")
    .typeError("Must be a string")
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
    await onPost(params as PostQueryParams)
    submit_disabled = false
    return
  }
</script>

<div class="space-y-2">
  {#if $account?.id}
    <div class="flex w-full grid grid-cols-3 sm:grid-cols-6 gap-6 pt-4 pb-4">
      <div class="col-span-6 sm:col-span-3 ">
        <Select
          items={posts}
          bind:value={selected_post}
          clearable={false}
          searchable={false}
          itemId='id'
          label="Post type*"/>
      </div>
      <div class="col-span-6 sm:col-span-3 ">
        <Input
          id="location-input"
          bind:value={work_location}
          placeholder="Location"
          label="Location"
          type="text"
          error={Boolean(form_errors.work_location)}
          errorMessage={form_errors.work_location} />
      </div>

      <div class="col-span-6 sm:col-span-3 ">
        <div class="flex items-end space-x-1">
          {#if creating_new_position}
            <Input
              id="new-position-input"
              bind:value={new_position}
              placeholder="new position name"
              label="New position*"
              type="text"
              error={Boolean(form_errors.position)}
              errorMessage={form_errors.position} />
          {:else}
            <Select
              items={positions}
              bind:value={selected_position}
              clearable={false}
              itemId='id'
              label="Position*" />
            {/if}
            <button
              on:click={() => creating_new_position = !creating_new_position}
              class="
                rounded-lg p-1 hover:bg-grey-100 text-grey-500
                { creating_new_position ? 'bg-grey-100' : '' }
              ">
              <Plus class="h-6 w-6" style="margin:3px;" />
            </button>
          </div>
      </div>
      <div class="col-span-6 sm:col-span-3">
        <Input
          id="tenure-stages-input"
          bind:value={tenure_stages}
          placeholder={ is_review ? "Tenure" : "Stages" }
          label={ is_review ? "Tenure" : "Stages" }
          type="text"
          error={Boolean(form_errors.tenure_stages)}
          errorMessage={form_errors.tenure_stages} />
      </div>

      <div class="col-span-6 flex space-x-3">
        <div class="w-1/3">
          <Select
            items={currencies}
            bind:value={selected_currency}
            clearable={false}
            searchable={false}
            itemId='id'
            label="Currency*"/>
        </div>
        <div class="w-1/3">
          <Input
            id="compensation-input"
            label={ is_review ? "Salary" : "Offer" }
            bind:value={compensation}
            placeholder={ is_review ? "Salary" : "Offer" }
            type="text"
            error={Boolean(form_errors.compensation)}
            errorMessage={form_errors.compensation} />
        </div>
        <div class="w-1/3">
          <Select
            items={tags}
            bind:value={selected_tag}
            clearable={false}
            searchable={false}
            itemId='id'
            label="Review tag*" />
        </div>
      </div>

      <div class="col-span-6 relative">
        {#if preview_post}
          <div class="POST_PREVIEW">
            <p class="text-xs font-extralight pb-1 text-grey-400">Preview</p>
            <div
              class="
                w-full px-4 py-2 relative flex items-center text-black
                bg-transparent dark:bg-dark-400 rounded-lg border border-grey-100
              ">
              <div
                class="
                  w-full bg-transparent h-24 resize-none pt-1
                  border-none focus:outline-none ring-0
                  space-y-4 overflow-hidden overflow-y-scroll
                ">
                {@html DOMPurify.sanitize(marked.parse(post ?? ''), sanitize_config)}
              </div>
            </div>
          </div>
        {:else}
          <p
            class="
              absolute w-full text-right text-xs font-extralight text-grey-400
            ">
            [supports <Link on:click={() => navigate('/about#markdown')}>markdown</Link>]
          </p>
          <Input
            id="post-input"
            bind:value={post}
            placeholder={ is_review ? "Review" : "Interview" }
            label={ is_review ? "Review*" : "Interview*" }
            text_area={true}
            error={Boolean(form_errors.post)}
            errorMessage={form_errors.post} />
        {/if}
      </div>
    </div>
    <div class="flex justify-end space-x-4 border-t pt-5">
      <SecondaryButton
        on:click={() => preview_post = !preview_post }>
          {preview_post ? 'Write' : 'Preview'}
      </SecondaryButton>
      <Button disabled={submit_disabled} on:click={onSubmit}>Submit</Button>
    </div>
  {:else}
    <div class="flex items-center justify-center pt-5">
      <p>
        You must
        <Link on:click={() => navigate('/login')}> log in </Link>
        to post
      </p>
    </div>
  {/if}
</div>
