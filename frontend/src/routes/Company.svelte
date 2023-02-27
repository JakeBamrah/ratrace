<script lang="ts">
  import axios from 'axios'
  import { onMount } from 'svelte'


  export let id: string
  export let navigate: any

  const int_id = Number(id)
  onMount(async () => {
    if (isNaN(Number(int_id))) {
      navigate('/')
    }

    let config = { headers: {
                      'Content-Type': 'application/json',
                      'Access-Control-Allow-Origin': '*'},
             }
    const resp = await axios.get(`http://127.0.0.1:8080/orgs/${id}`, config)
    console.log(resp.data)
  })


</script>

<div>
  Companies
</div>
