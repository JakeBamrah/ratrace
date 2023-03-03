<script lang="ts">
  import { onMount } from 'svelte'
  import { Industry } from '../lib/data/apiService'


  export let id: string
  export let navigate: any
  export let getOrg: (org_id: number) => Promise<any>

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
        if (!r) {
          return
        }

        console.log(r)
        org = r.org
        reviews = r.reviews
        interviews = r.interviews
      })
  })
</script>

<div>
  Companies info
  {#if org}
    <p class="text-xl">{org.name}</p>
    <p>Company size: {org.size}</p>
    <p>Company url: {org.url ?? 'No url available'}</p>
    <p>Company industry: {Industry[org.industry]}</p>

    <p>Reviews: {reviews.length}</p>
    <p>Interiews: {interviews.length}</p>
  {:else}
    <p>No company data</p>
  {/if}
</div>
