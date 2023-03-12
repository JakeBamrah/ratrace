<script lang="ts">
  import { account, Vote, Vote as VoteEnum } from '../utils/apiService'
  import type { Vote as VoteType, Post, onVote } from '../utils/apiService'


  export let post: Post
  export let onVote: onVote

  // prevent double spends by keeping track of upvotes and downvotes
  // disable vote button immediately after submit
  $: votes = post.upvotes.length - post.downvotes.length
  $: already_upvoted = post.upvotes.includes($account?.id)
  $: already_downvoted = post.downvotes.includes($account?.id)

  const handleVote = (vote: VoteType) => {
    // check if they have already given the same upvote prior
    if (
      vote === VoteEnum.UPVOTE && already_upvoted ||
      vote === VoteEnum.DOWNVOTE && already_downvoted
    )
      return

    const params = {
      post_id: post.id,
      vote,
      already_upvoted,
      already_downvoted
    }

    // try to remove votes from the other side (if they exist)
    if (vote === VoteEnum.UPVOTE) {
      post.upvotes.push($account.id)
      const idx = post.downvotes.indexOf($account.id)
      if (idx >= 0) {
        post.downvotes.splice(idx, 1)
      }
    }
    if (vote === VoteEnum.DOWNVOTE) {
      post.downvotes.push($account.id)
      const idx = post.upvotes.indexOf($account.id)
      if (idx >= 0) {
        post.upvotes.splice(idx, 1)
      }
    }
    post = post

    onVote(params)
  }
</script>

<div class="flex space-x-4">
  <div class="flex space-x-2">
    <button
      disabled={already_upvoted}
      on:click={() => handleVote(Vote.UPVOTE)}
      class="disabled:text-red-500 text-xl">+</button>
    <p class="mt-1 text-grey-400">({votes})</p>
    <button
      disabled={already_downvoted}
      on:click={() => handleVote(Vote.DOWNVOTE)}
      class="disabled:text-red-500 text-xl">-</button>
  </div>
</div>
