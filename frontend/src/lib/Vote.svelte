<script lang="ts">
    export let upvotes: number[]
    export let downvotes: number[]
    export let onVote: (vote: string) => void

    const votes: number = upvotes.length - downvotes.length
</script>

<div class="flex space-x-4">
  <div class="flex space-x-2">
    <button class="text-xl">+</button>
    <p class="mt-1 text-grey-400">({votes})</p>
    <button class="text-xl">-</button>
  </div>
</div>
