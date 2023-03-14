<script lang="ts">
  import { icons } from 'feather-icons'
  import { onMount } from 'svelte'
  import Select from 'svelte-select'
  import { useNavigate } from 'svelte-navigator'

  import { Industry, Rating, PostSort, PostEnum } from '../utils/apiService'
  import type {
    Review, Interview, PostSortKey, onVote, onPostType,
    RatingKey, Position, OrgQueryParamsType, Post, PostQueryParams
  } from '../utils/apiService'
  import Posts from './Posts.svelte'
  import Button from '../lib/Button.svelte'
  import PageContainer from '../lib/PageContainer.svelte'
  import Tabs from '../lib/Tabs.svelte'
  import CreatePost from './CreatePost.svelte'
  import { getCompanySizeBracket } from '../utils/mappers'


  const LIMIT = 50
  const ALL_POSITIONS = { id: -1, label: 'All'}
  const DEFAULT_SORT = { id: PostSort.DATE_CREATED.toUpperCase() as PostSortKey, label: PostSort.DATE_CREATED }
  const DEFAULT_SELECTED_TAG: { id: RatingKey, label: Rating } = {
      id: Rating.ALL.toUpperCase() as RatingKey,
      label: Rating.ALL
    }


  enum SelectedPanelKey {
    REVIEWS = 'Reviews',
    INTERVIEWS = 'Interviews',
    CREATE = 'Create',
  }
  type SelectedPanel = { id: SelectedPanelKey, value: string }
  type SelectSort = { id: PostSortKey, label: PostSort }

  export let id: string
  export let getOrg: (org_id: number) => Promise<any>
  export let onGetOrgPosts: (org_id: OrgQueryParamsType) => Promise<any>
  export let onVote: onVote
  export let onPost: onPostType

  const navigate = useNavigate()

  // ------ REVIEW \ INTERVIW FILTER OPTIONS ------
  let selected_panel: SelectedPanel = { id: SelectedPanelKey.REVIEWS, value: 'Reviews' }
  const left_panels: SelectedPanel[] = [
    { id: SelectedPanelKey.REVIEWS, value: 'Reviews' },
    { id: SelectedPanelKey.INTERVIEWS, value: 'Interviews' }
  ]
  const right_panels: SelectedPanel[] = [
    { id: SelectedPanelKey.CREATE, value: icons["edit-3"].toSvg({ class: 'h-4 w-4'}) }
  ]

  const tags = Object.keys(Rating).map(k => ({ id: k, label: Rating[k]}))
  let review_selected_tag = DEFAULT_SELECTED_TAG
  let interview_selected_tag = DEFAULT_SELECTED_TAG

  $: sorts = Object.keys(PostSort).map(k => {
    // tenure is only available as a choice for the reviews panel
    const is_tenure = PostSort[k] === PostSort.TENURE
    const is_stages = PostSort[k] === PostSort.STAGES
    return {
      id: k,
      label: PostSort[k],
      selectable: !(is_tenure && is_interview) && !(is_stages && is_review)
    }}) as SelectSort[]
  let review_selected_sort: SelectSort = DEFAULT_SORT
  let interview_selected_sort: SelectSort = DEFAULT_SORT

  let positions = []
  let review_selected_position: { id: number, label: string } = ALL_POSITIONS
  let interview_selected_position: { id: number, label: string } = ALL_POSITIONS

  let org = null
  let reviews: Review[] = []
  let interviews: Interview[] = []

  // offset used for loading more rows (pagination)
  let review_offset: number = 0
  let interview_offset: number = 0

  // included in the api to determine if we've maxed out the rows for the filter
  let filter_review_max_reached = false
  let filter_interview_max_reached = false

  // check if we've pulled all reviews for the org
  $: maxed_out_reviews = reviews.length === org?.total_reviews
  $: maxed_out_interviews = interviews.length === org?.total_interviews

  $: is_review = selected_panel?.id === SelectedPanelKey.REVIEWS
  $: is_interview = selected_panel?.id === SelectedPanelKey.INTERVIEWS

  const sortItems = (args : {
    items: (Review | Interview)[]
    tag: RatingKey
    sort: PostSortKey
    position_id: number
  }) => {
    /*
     * Items are pulled in from api (getOrg or handleGetOrgPosts). If
     * data has come directly from the api it has already been sorted. If all
     * data has been loaded we sort in-app.
     */
    const {
      items,
      tag,
      sort,
      position_id,
    } = args

    // if max not reached, we've had to pull in data (pre-sorted) from api
    if (is_review && !maxed_out_reviews) {
      return reviews
    }
    if (is_interview && !maxed_out_interviews) {
      return interviews
    }

    // we have no more items to collect from api so we can sort in memory
    let sorted_items = items
    if (tag !== Rating.ALL.toUpperCase()) {
      sorted_items = items.filter(i => i.tag === tag)
    }
    else {
      sorted_items = items
      sorted_items.sort((a, b) => a.created_at >= b.created_at ? 1 : 0)
    }

    if (sort === PostSort.DOWNVOTES.toUpperCase()) {
      sorted_items.sort((a, b) => (a.upvotes.length - a.downvotes.length) >= (b.upvotes.length - b.downvotes.length) ? 1 : 0)
    }

    if (sort === PostSort.UPVOTES.toUpperCase()) {
      sorted_items.sort((a, b) => (a.upvotes.length - a.downvotes.length) <= (b.upvotes.length - b.downvotes.length) ? 1 : 0)
    }

    if (sort === PostSort.TENURE.toUpperCase()) {
        sorted_items.sort((a: Review, b: Review) => a.duration_years < b.duration_years ? 1 : 0)
    }

    if (sort === PostSort.STAGES.toUpperCase()) {
        sorted_items.sort((a: Interview, b: Interview) => a.stages < b.stages ? 1 : 0)
    }

    if (sort === PostSort.COMPENSATION.toUpperCase()) {
        sorted_items.sort((a: Post, b: Post) => a.compensation < b.compensation ? 1 : 0)
    }

    // sort by all positions
    if (position_id !== -1) {
      sorted_items = sorted_items.filter(i => i.position.id === position_id)
    }

    return sorted_items
  }

  $: filtered_reviews = sortItems({
    items: reviews,
    tag: review_selected_tag?.id,
    sort: review_selected_sort?.id,
    position_id: review_selected_position?.id
  }) as Review[]

  $: filtered_interviews = sortItems({
    items: interviews,
    tag: interview_selected_tag?.id,
    sort: interview_selected_sort?.id,
    position_id: interview_selected_position?.id
  }) as Interview[]

  const handleGetOrgPosts = (
    post_type: PostEnum,
    max_reached: boolean,
    reset: boolean = false,
  ) => {
    /*
     * We load reviews and interviews in batches of 50.
     * We need to pull in more data from the api everytime the select menu is
     * toggled because sorting may require new rows (not previously loaded)
     * to be displayed. If we have retrieved *all* data available we can avoid
     * calling the api and default to sortItems
     *
     * Data from the api will be returned to us in the required sorting order.
     */

    if (max_reached && !reset) {
      // we have no more data to pull in so just sort on client-side
      // not totally ideal because we may pull in some data unnecessarily but
      // it's a compromise for simplicity.
      return
    }

    const is_post_type_review = post_type === PostEnum.REVIEW
    const params: OrgQueryParamsType = {
      org_id: org.id,
      position_id: is_post_type_review ? review_selected_position?.id : interview_selected_position?.id,
      tag: is_post_type_review ? review_selected_tag?.id : interview_selected_tag?.id,
      sort_order: is_post_type_review ? review_selected_sort?.id : interview_selected_sort?.id,
      offset: reset ? 0 : is_post_type_review ? review_offset : interview_offset,
      post_type
    }

    onGetOrgPosts(params).then(r => {
      if (post_type === PostEnum.REVIEW) {
        reviews = reset ? r.posts : reviews.concat(r.posts)

        // reset the offsets back to initial 50
        review_offset = reviews.length
        filter_review_max_reached = r.max_reached
      }

      if (post_type === PostEnum.INTERVIEW) {
        interviews = reset ? r.posts : interviews.concat(r.posts)

        // reset the offsets back to initial 50
        interview_offset = interviews.length
        filter_interview_max_reached = r.max_reached
      }
    })
  }

  const onSortChange = () => {
    // pull in fresh, sorted data from scratch everytime filters change
    // not the most efficient but keeps the code simple
    const post_type =  is_review ? PostEnum.REVIEW : PostEnum.INTERVIEW
    const max_reached = is_review ? maxed_out_reviews : maxed_out_interviews
    const reset = true
    handleGetOrgPosts(post_type, max_reached, reset)
  }

  // ORG SETUP AND POST CREATION
  const initializeOrgData = (org_id: number) => {
    getOrg(org_id).then(r => {
      if (r.org && Object.keys(r.org).length === 0) {
        navigate('/')
        return
      }

      org = r.org
      reviews = r.reviews
      interviews = r.interviews
      positions = [ALL_POSITIONS].concat(
        org.positions.map((p: Position) => ({ id: p.id, label: p.name }))
      )

      review_offset = r.reviews.length
      interview_offset = r.interviews.length

      filter_review_max_reached = r.reviews.length < LIMIT
      filter_interview_max_reached = r.interviews.length < LIMIT
    })
  }

  const handlePost = async (params: PostQueryParams) => {
    params.org_id = org?.id
    const resp = await onPost(params)

    // completely reset org data (except filters)
    initializeOrgData(org.id)

    // set selected panel to review
    selected_panel = left_panels[0]
    return resp
  }

  // pull in org data on mount
  const int_id = Number(id)
  onMount(async () => {
    if (isNaN(Number(int_id))) {
      navigate('/')
      return
    }

    if (int_id)
      initializeOrgData(int_id)
  })
</script>

<PageContainer>
  {#if org}
  <div class="COMPANY_BIO w-full rounded-xl border px-6 py-4 space-y-2">
    <div class="w-full flex items-center space-x-2 pb-4">
      <div class="h-14 w-14 rounded-full bg-grey-300" />
      <p class="font-bold truncate w-48 sm:w-80">{org.name}</p>
    </div>
    <div class="flex items-center space-x-2">
      {@html icons.home.toSvg({ class: 'h-4 w-4'})}
      <p class="truncate">{org.headquarters}</p>
    </div>

    <div class="flex items-center space-x-2">
      {@html icons.user.toSvg({ class: 'h-4 w-4'})}
      <p>{getCompanySizeBracket(org.size)}</p>
    </div>

    <div class="flex items-center space-x-2">
      {@html icons.link.toSvg({ class: 'h-4 w-4'})}
      {#if org.url}
        <a href={org.url} target="_blank" rel="noreferrer" class="truncate">{org.url}</a>
      {:else}
        <p class="truncate">{'No url available'}</p>
      {/if}
    </div>

    <div class="flex items-center space-x-2">
      {@html icons.globe.toSvg({ class: 'h-4 w-4'})}
      <p class="truncate">{Industry[org.industry]}</p>
    </div>
  </div>

  <div
    class="POSITION_FILTER
      flex w-full grid grid-cols-8 gap-y-1 gap-x-2
      border rounded-xl px-6 py-4
    ">
      {#if is_review}
        <div class="REVIEW_SORT_OPTIONS col-span-8 sm:col-span-4 w-full pt-0">
          Position:
          <Select
            itemId='id'
            items={positions}
            bind:value={review_selected_position}
            clearable={false}
            on:change={onSortChange} />
        </div>
        <div class="col-span-4 sm:col-span-2 w-full pt-2 sm:pt-0">
          Tag:
          <Select
            itemId='id'
            items={tags}
            bind:value={review_selected_tag}
            clearable={false}
            on:change={onSortChange} />
        </div>

        <div class="col-span-4 sm:col-span-2 pt-2 sm:pt-0">
          Sort:
          <Select
            itemId='id'
            items={sorts}
            bind:value={review_selected_sort}
            clearable={false}
            on:change={onSortChange} />
        </div>
      {:else}
        <div class="INTERVIEW_SORT_OPTIONS col-span-8 sm:col-span-4 w-full pt-0">
          Position:
          <Select
            itemId='id'
            items={positions}
            bind:value={interview_selected_position}
            clearable={false}
            on:change={onSortChange} />
        </div>
        <div class="col-span-4 sm:col-span-2 w-full pt-2 sm:pt-0">
          Tag:
          <Select
            itemId='id'
            items={tags}
            bind:value={interview_selected_tag}
            clearable={false}
            on:change={onSortChange} />
        </div>

        <div class="col-span-4 sm:col-span-2 pt-2 sm:pt-0">
          Sort:
          <Select
            itemId='id'
            items={sorts}
            bind:value={interview_selected_sort}
            clearable={false}
            on:change={onSortChange} />
        </div>
      {/if}
    </div>

  <div
    class="REVIEWS_AND_INTERVIEWS
      w-full border rounded-xl px-6 py-4 space-y-2 divide-y
    ">
    <div class="w-full flex space-x-4 sm:space-x-2">
      <Tabs
        left_tabs={left_panels}
        symbols={right_panels}
        selected_tab={selected_panel}
        onTabSelect={(panel) => selected_panel = panel} />
    </div>
    {#if is_review}
      <Posts
        onVote={onVote}
        posts={filtered_reviews}
        post_type={PostEnum.REVIEW}
      />
    {:else if is_interview}
      <Posts
        onVote={onVote}
        posts={filtered_interviews}
        post_type={PostEnum.INTERVIEW}
      />
    {:else}
      <CreatePost
        positions={positions.filter(p => p.id !== -1)}
        onPost={handlePost}
      />
    {/if}
    {#if is_review && !filter_review_max_reached}
      <div class="w-full flex pt-4 justify-center">
        <Button
          on:click={() => (
          handleGetOrgPosts(PostEnum.REVIEW, maxed_out_reviews, false))
        }>Load more</Button>
      </div>
    {/if}
    {#if is_interview && !filter_interview_max_reached}
      <div class="w-full flex pt-4 justify-center">
        <Button
          on:click={() => (
          handleGetOrgPosts(PostEnum.INTERVIEW, maxed_out_interviews, false))
        }>Load more</Button>
      </div>
    {/if}
  </div>

  {:else}
    <p>No company data <a href="/">search again</a></p>

  {/if}
</PageContainer>
