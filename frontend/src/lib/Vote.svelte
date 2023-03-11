<script lang="ts">
  import { Vote } from '../utils/apiService'


  export let upvotes: number[]
  export let downvotes: number[]
  export let onVote: (vote: string) => void

  $: votes = upvotes.length - downvotes.length
</script>

<div class="flex space-x-4">
  <div class="flex space-x-2">
    <button on:click={() => onVote(Vote.UPVOTE)} class="text-xl">+</button>
    <p class="mt-1 text-grey-400">({votes})</p>
    <button on:click={() => onVote(Vote.DOWNVOTE)} class="text-xl">-</button>
  </div>
</div>
