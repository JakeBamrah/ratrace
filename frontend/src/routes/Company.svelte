<script lang="ts">
  import { icons } from 'feather-icons'
  import { onMount } from 'svelte'
  import Select from 'svelte-select'

  import { Industry, Rating, ReviewSort } from '../utils/apiService'
  import type { Review, Interview, ReviewSortKey, RatingKey, Position } from '../utils/apiService'
  import Interviews from './Interviews.svelte'
  import PageContainer from '../lib/PageContainer.svelte'
  import Reviews from './Reviews.svelte'
  import Tabs from '../lib/Tabs.svelte'


  type SelectedPanel = 'Reviews' | 'Interviews'

  export let id: string
  export let navigate: any
  export let getOrg: (org_id: number) => Promise<any>

  // review and interview filter options
  let selected_panel: SelectedPanel = 'Reviews'
  let panels: SelectedPanel[] = ['Reviews', 'Interviews']

  let tags = Object.keys(Rating).map(k => ({ id: k, label: Rating[k]}))
  let selected_tag: { id: RatingKey, label: Rating } = {
    id: Rating.ALL.toUpperCase() as RatingKey,
    label: Rating.ALL
  }

  $: sorts = Object.keys(ReviewSort).map(k => {
    // tenure is only available as a choice for the reviews panel
    const is_tenure = ReviewSort[k] === ReviewSort.TENURE
    return {
      id: k,
      label: ReviewSort[k],
      selectable: !(is_tenure && selected_panel === 'Interviews')
    }})
  let selected_sort = null

  let positions = []
  let selected_position = null

  $: org = null
  let reviews: Review[] = []
  let interviews: Interview[] = []

  const sortItems = (args : {
    items: (Review | Interview)[]
    tag: RatingKey
    sort: ReviewSortKey
    position_id: number
    requires_api: boolean
    selected_panel: SelectedPanel
  }) => {
    /*
     * We load reviews and interviews in batches of 50. If we have <= 50 reviews
     * or interviews, we can sort the items without pulling in more data.
     * If however, there are more than 50, we need to pull in more data from the
     * api because sorting may require new rows (not previously loaded) to
     * be displayed.
     *
     * Data from the api will be returned to us in the required sorting order.
     */
    const {
      items,
      tag,
      sort,
      position_id,
      requires_api,
      selected_panel,
    } = args

    let sorted_items = items
    if (requires_api) {
      console.log("Do api sort")
      // return items
    }

    // filter for reviews with specific ratings or send them all through
    if (tag !== Rating.ALL.toUpperCase()) {
      sorted_items = items.filter(i => i.tag === tag)
    }
    else {
      sorted_items = items
      sorted_items.sort((a, b) => a.created_at >= b.created_at ? 1 : 0)
    }

    if (sort === ReviewSort.DOWNVOTES.toUpperCase()) {
      sorted_items.sort((a, b) => (a.upvotes.length - a.downvotes.length) >= (b.upvotes.length - b.downvotes.length) ? 1 : 0)
    }

    if (sort === ReviewSort.UPVOTES.toUpperCase()) {
      sorted_items.sort((a, b) => (a.upvotes.length - a.downvotes.length) <= (b.upvotes.length - b.downvotes.length) ? 1 : 0)
    }

    if (sort === ReviewSort.TENURE.toUpperCase()) {
      if (selected_panel === 'Interviews')
        selected_sort = null

      if (selected_panel === 'Reviews')
        sorted_items.sort((a: Review, b: Review) => a.duration_years < b.duration_years ? 1 : 0)
    }

    if (sort === ReviewSort.COMPENSATION.toUpperCase()) {
      if (selected_panel === 'Interviews')
        sorted_items.sort((a: Interview, b: Interview) => a.offer < b.offer ? 1 : 0)

      if (selected_panel === 'Reviews')
        sorted_items.sort((a: Review, b: Review) => a.salary < b.salary ? 1 : 0)
    }

    if (position_id) {
      sorted_items = sorted_items.filter(i => i.position.id === position_id)
    }

    return sorted_items
  }

  $: requires_api = org?.total_reviews > reviews.length || org?.total_interviews > reviews.length
  $: filtered_reviews = sortItems({
    items: reviews,
    tag: selected_tag?.id,
    sort: selected_sort?.id,
    position_id: selected_position?.id,
    requires_api: requires_api,
    selected_panel: selected_panel
  }) as Review[]

  $: filtered_interviews = sortItems({
    items: interviews,
    tag: selected_tag?.id,
    sort: selected_sort?.id,
    position_id: selected_position?.id,
    requires_api: requires_api,
    selected_panel: selected_panel
  }) as Interview[]

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
        positions = org.positions.map((p: Position) => ({id: p.id, label: p.name}))
      })
  })

  const getCompanySizeBracket = (size: number) => {
    if (size > 5000)
      return "5000-1000"
    if (size > 1000)
      return "1000-5000"
    if (size > 500)
      return "500-1000"
    if (size > 200)
      return "200-500"
    if (size > 100)
      return "100-200"
    if (size > 50)
      return "50-100"
    if (size > 10)
      return "10-50"

    return "1-10"
  }
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
      <p class="text-sm truncate">{org.headquarters}</p>
    </div>

    <div class="flex items-center space-x-2">
      {@html icons.user.toSvg({ class: 'h-4 w-4'})}
      <p class="text-sm">{getCompanySizeBracket(org.size)}</p>
    </div>

    <div class="flex items-center space-x-2">
      {@html icons.link.toSvg({ class: 'h-4 w-4'})}
      {#if org.url}
        <a href={org.url} target="_blank" rel="noreferrer" class="text-sm truncate">{org.url}</a>
      {:else}
        <p class="text-sm truncate">{'No url available'}</p>
      {/if}
    </div>

    <div class="flex items-center space-x-2">
      {@html icons.globe.toSvg({ class: 'h-4 w-4'})}
      <p class="text-sm truncate">{Industry[org.industry]}</p>
    </div>
  </div>

  <div
    class="POSITION_FILTER
      flex w-full grid grid-cols-8 gap-y-1 gap-x-2
      border rounded-xl px-6 py-4 divide-y sm:divide-y-0
    ">
    <div class="col-span-8 sm:col-span-4 w-full pt-2 sm:pt-0">
      Position:
      <Select
        placeholder='Filter position'
        itemId='id'
        items={positions}
        bind:value={selected_position} />
    </div>
    <div class="col-span-4 sm:col-span-2 w-full pt-2 sm:pt-0">
      Tag:
      <Select
        itemId='id'
        items={tags}
        bind:value={selected_tag}
        clearable={false} />
    </div>

    <div class="col-span-4 sm:col-span-2 pt-2 sm:pt-0">
      Sort:
      <Select
        placeholder='Select sort'
        itemId='id'
        items={sorts}
        bind:value={selected_sort}
        clearable={false} />
    </div>
  </div>

  <div
    class="REVIEWS_AND_INTERVIEWS
      w-full border rounded-xl px-6 py-4 space-y-2 divide-y
    ">
    <div class="w-full flex space-x-4 sm:space-x-2">
      <Tabs
        tabs={panels}
        selected_tab={selected_panel}
        onTabSelect={(panel) => selected_panel = panel} />
    </div>
    {#if selected_panel === 'Reviews'}
      <Reviews reviews={filtered_reviews} />
    {:else}
      <Interviews interviews={filtered_interviews} />
    {/if}

    {#if selected_panel == 'Reviews' && reviews.length < org.total_reviews}
        LOAD MORE REVIEWS
    {/if}
    {#if selected_panel == 'Interviews' && interviews.length < org.total_interviews}
        LOAD MORE INTERVIEWS
    {/if}

  </div>
  {:else}
    <p>No company data <a href="/">search again</a></p>
  {/if}
</PageContainer>
