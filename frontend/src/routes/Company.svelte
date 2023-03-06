<script lang="ts">
  import { icons } from 'feather-icons'
  import { onMount } from 'svelte'
  import Select from 'svelte-select'

  import { Industry, Rating, ReviewSort } from '../utils/apiService'
  import Interviews from './Interviews.svelte'
  import PageContainer from '../lib/PageContainer.svelte'
  import Reviews from './Reviews.svelte'
  import Tabs from '../lib/Tabs.svelte'


  export let id: string
  export let navigate: any
  export let getOrg: (org_id: number) => Promise<any>

  let selected_panel = 'Reviews'
  let panels = ['Reviews', 'Interviews']

  let tags = Object.keys(Rating).map(k => ({ id: k, label: Rating[k]}))
  let selected_tag = Rating.ALL

  let sorts = Object.keys(ReviewSort).map(k => ({ id: k, label: ReviewSort[k] }))
  let selected_sort = null

  $: org = null
  let reviews = []
  let interviews = []

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

        console.log(r)
        console.log(r.reviews.length)
        console.log(r.interviews.length)
        org = r.org
        reviews = r.reviews
        interviews = r.interviews
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
      <Select itemId='id' items={tags} bind:value={selected_tag} clearable={false} />
    </div>
    <div class="col-span-4 sm:col-span-2 w-full pt-2 sm:pt-0">
      Tag:
      <Select itemId='id' items={tags} bind:value={selected_tag} clearable={false} />
    </div>

    <div class="col-span-4 sm:col-span-2 pt-2 sm:pt-0">
      Sort:
      <Select itemId='id' items={sorts} bind:value={selected_sort} clearable={false} />
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
      <Reviews reviews={reviews} />
    {:else}
      <Interviews interviews={interviews} />
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
