<script lang="ts">
  import { icons } from 'feather-icons'
  import { onMount } from 'svelte'
  import Select from 'svelte-select'
  import { useNavigate } from 'svelte-navigator'

  import { Industry, Rating, PostSort, PostEnum } from '../utils/apiService'
  import type {
    Review, Interview, PostSortKey, onVote,
    RatingKey, Position, OrgQueryParamsType, Post
  } from '../utils/apiService'
  import Posts from './Posts.svelte'
  import PageContainer from '../lib/PageContainer.svelte'
  import Tabs from '../lib/Tabs.svelte'
  import PostCreate from './PostCreate.svelte'
  import { getCompanySizeBracket } from '../utils/mappers'


  const LIMIT = 50
  const ALL_POSITIONS = { id: -1, label: 'All'}
  const DEFAULT_SORT = { id: PostSort.DATE_CREATED.toUpperCase() as PostSortKey, label: PostSort.DATE_CREATED }

  enum SelectedPanelKey {
    REVIEWS = 'Reviews',
    INTERVIEWS = 'Interviews',
    CREATE = 'Create',
  }
  type SelectedPanel = { id: SelectedPanelKey, value: string }
  type SelectSort = { id: PostSortKey, label: PostSort }

  export let id: string
  export let getOrg: (org_id: number) => Promise<any>
  export let getReviewsAndInterviews: (org_id: OrgQueryParamsType) => Promise<any>
  export let onVote: onVote

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
  let selected_tag: { id: RatingKey, label: Rating } = {
    id: Rating.ALL.toUpperCase() as RatingKey,
    label: Rating.ALL
  }

  $: sorts = Object.keys(PostSort).map(k => {
    // tenure is only available as a choice for the reviews panel
    const is_tenure = PostSort[k] === PostSort.TENURE
    return {
      id: k,
      label: PostSort[k],
      selectable: !(is_tenure && selected_panel.id === 'Interviews')
    }}) as SelectSort[]
  let selected_sort: SelectSort = DEFAULT_SORT
  let positions = [ALL_POSITIONS]
  let selected_position: { id: number, label: string } = ALL_POSITIONS

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

  const sortItems = (args : {
    items: (Review | Interview)[]
    tag: RatingKey
    sort: PostSortKey
    position_id: number
    selected_panel: SelectedPanel
  }) => {
    /*
     * Items are pulled in from api (getOrg or onGetReviewsAndInterviews). If
     * data has come directly from the api it has already been sorted. If all
     * data has been loaded we sort in-app.
     */
    const {
      items,
      tag,
      sort,
      position_id,
      selected_panel
    } = args

    // if max not reached, we've had to pull in data (pre-sorted) from api
    if (selected_panel.id === SelectedPanelKey.REVIEWS && !maxed_out_reviews) {
      return reviews
    }
    if (selected_panel.id === SelectedPanelKey.INTERVIEWS && !maxed_out_interviews) {
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
      if (selected_panel.id === SelectedPanelKey.INTERVIEWS) {
        selected_sort = null
    }

      if (selected_panel.id === SelectedPanelKey.REVIEWS)
        sorted_items.sort((a: Review, b: Review) => a.duration_years < b.duration_years ? 1 : 0)
    }

    if (sort === PostSort.COMPENSATION.toUpperCase()) {
      if (selected_panel.id === SelectedPanelKey.INTERVIEWS)
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
    tag: selected_tag?.id,
    sort: selected_sort?.id,
    position_id: selected_position?.id,
    selected_panel: selected_panel
  }) as Review[]

  $: filtered_interviews = sortItems({
    items: interviews,
    tag: selected_tag?.id,
    sort: selected_sort?.id,
    position_id: selected_position?.id,
    selected_panel: selected_panel
  }) as Interview[]

  const onGetReviewsAndInterviews = (reset: boolean = false) => {
    /*
     * We load reviews and interviews in batches of 50.
     * We need to pull in more data from the api everytime the select menu is
     * toggled because sorting may require new rows (not previously loaded)
     * to be displayed. If we have retrieved *all* data available we can avoid
     * calling the api and default to sortItems
     *
     * Data from the api will be returned to us in the required sorting order.
     */

    if (maxed_out_interviews && maxed_out_reviews) {
      // we have no more data to pull in so just sort on client-side
      // not totally ideal because we may pull in some data unnecessarily but
      // it's a compromise for simplicity.
      return
    }

    const params: OrgQueryParamsType = {
      org_id: org.id,
      position_id: selected_position?.id,
      tag: selected_tag.id,
      sort_order: selected_sort?.id,
      // we take the max offset because it helps us avoid pulling in duplicate
      // rows for entity (interview or review) with less items
      offset: Math.max(review_offset, interview_offset)
    }
    getReviewsAndInterviews(params).then(r => {
      reviews = reset ? r.reviews : reviews.concat(r.reviews)
      interviews = reset ? r.interviews : interviews.concat(r.interviews)

      // reset the offsets back to initial 50
      review_offset = reviews.length
      interview_offset = interviews.length

      filter_review_max_reached = r.no_more_reviews
      filter_interview_max_reached = r.no_more_interviews
    })
  }

  const onSortChange = () => {
    // pull in fresh, sorted data from scratch everytime filters change
    // not the most efficient but keeps the code simple
    review_offset = 0
    interview_offset = 0
    onGetReviewsAndInterviews(true)
  }

  // pull in org data on mount
  const int_id = Number(id)
  onMount(async () => {
    if (isNaN(Number(int_id))) {
      navigate('/')
      return
    }

    if (int_id)
      getOrg(int_id).then(r => {
        if (r.org && Object.keys(r.org).length === 0) {
          navigate('/')
          return
        }

        org = r.org
        reviews = r.reviews
        interviews = r.interviews
        positions = positions.concat(
          org.positions.map((p: Position) => ({ id: p.id, label: p.name }))
        )

        review_offset = r.reviews.length
        interview_offset = r.interviews.length

        filter_review_max_reached = r.reviews.length < LIMIT
        filter_interview_max_reached = r.interviews.length < LIMIT
      })
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
    <div class="col-span-8 sm:col-span-4 w-full pt-0">
      Position:
      <Select
        itemId='id'
        items={positions}
        bind:value={selected_position}
        clearable={false}
        on:change={onSortChange} />
    </div>
    <div class="col-span-4 sm:col-span-2 w-full pt-2 sm:pt-0">
      Tag:
      <Select
        itemId='id'
        items={tags}
        bind:value={selected_tag}
        clearable={false}
        on:change={onSortChange} />
    </div>

    <div class="col-span-4 sm:col-span-2 pt-2 sm:pt-0">
      Sort:
      <Select
        itemId='id'
        items={sorts}
        bind:value={selected_sort}
        clearable={false}
        on:change={onSortChange} />
    </div>
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
    {#if selected_panel.id === SelectedPanelKey.REVIEWS}
      <Posts
        onVote={onVote}
        posts={filtered_reviews}
        post_type={PostEnum.REVIEW}
      />
    {:else if selected_panel.id === SelectedPanelKey.INTERVIEWS}
      <Posts
        onVote={onVote}
        posts={filtered_interviews}
        post_type={PostEnum.INTERVIEW}
      />
    {:else}
      <PostCreate
        positions={positions.filter(p => p.id !== -1)}
      />
    {/if}

      {#if selected_panel.id == 'Reviews' && !filter_review_max_reached}
        <div class="w-full flex justify-center">
          <button on:click={() => onGetReviewsAndInterviews()}>LOAD MORE REVIEWS</button>
        </div>
      {/if}
      {#if selected_panel.id == 'Interviews' && !filter_interview_max_reached}
        <div class="w-full flex justify-center">
          <button on:click={() => onGetReviewsAndInterviews()}>LOAD MORE INTERVIEWS</button>
        </div>
      {/if}

  </div>
  {:else}
    <p>No company data <a href="/">search again</a></p>
  {/if}
</PageContainer>
