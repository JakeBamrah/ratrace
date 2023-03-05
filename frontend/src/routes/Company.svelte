<script lang="ts">
  import { icons } from 'feather-icons'
  import { onMount } from 'svelte'

  import { Industry } from '../utils/apiService'
  import PageContainer from '../lib/PageContainer.svelte'
  import Reviews from './Reviews.svelte'


  export let id: string
  export let navigate: any
  export let getOrg: (org_id: number) => Promise<any>

  let info_panel = 'reviews'

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
  <div class="COMPANY_BIO w-full rounded-xl border px-6 py-4">
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
      flex w-full grid grid-cols-6 gap-y-1
      border rounded-xl px-6 py-4 divide-y sm:divide-y-0
    ">
    <div class="col-span-6 sm:col-span-3 w-full">Position: </div>
    <div class="col-span-3 sm:col-span-1 w-full pt-2 sm:pt-0">Tag: </div>
    <div class="col-span-3 sm:col-span-2 w-full pt-2 sm:pt-0">Sort: </div>
  </div>

  <div
    class="REVIEWS_AND_INTERVIEWS
      w-full border rounded-xl px-6 py-4 space-y-2 divide-y
    ">
    <div class="w-full flex space-x-4 sm:space-x-2">
      <button on:click={() => info_panel = 'reviews' }>Reviews</button>
      <button on:click={() => info_panel = 'interviews' }>Interviews</button>
    </div>
    {#if info_panel === 'reviews'}
      <Reviews reviews={reviews} />
    {:else}
      <p>Interiews: {interviews.length}</p>
    {/if}
  </div>
  {:else}
    <p>No company data <a href="/">search again</a></p>
  {/if}
</PageContainer>
