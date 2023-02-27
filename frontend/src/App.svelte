<script lang="ts">

  import { Router, Route, Link } from 'svelte-navigator'
  import Home from './lib/Home.svelte'
  import Company from './routes/Company.svelte'
  import ApiService from './lib/data/apiService'


  const api = new ApiService(import.meta.env.VITE_API_BASE_URL)

</script>

<main>
  <Router primary={false} url="/">
    <Route path="org/*">
      <Route path=":id" let:params let:navigate>
        <Company id={params.id} navigate={navigate} />
      </Route>
    </Route>
    <Route>
        <Home getOrgs={api.getOrgs} />
    </Route>
  </Router>
</main>
