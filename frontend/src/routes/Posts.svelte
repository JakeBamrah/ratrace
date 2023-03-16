<script lang="ts">
  import { PostEnum } from '../utils/apiService'
  import type { Post as PostType, VoteParams, onVote } from '../utils/apiService'
  import Post from './Post.svelte'

  export let posts: PostType[]
  export let onVote: onVote
  export let post_type: PostEnum
  export let onDeletePost: (post_id: number) => void

  $: is_review = post_type === PostEnum.REVIEW

  const handlePostVote = async (params: VoteParams) => {
    onVote({ ...params, vote_model_type: post_type })
    return
  }
</script>

<div class="REVIEW_CONTAINER w-full divide-y space-y-4">
  {#if posts.length > 0}
    {#each posts as post}
      <Post
        post_type={post_type}
        post={post}
        onVote={handlePostVote}
        onDeletePost={onDeletePost}
      />
    {/each}
  {:else}
    <div class="w-full pt-6 pb-4 text-center">
      No {is_review ? 'reviews' : 'interviews'} found
    </div>
  {/if}
</div>
