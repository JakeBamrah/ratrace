<script lang="ts">
  import { marked } from 'marked'

  import { PostEnum } from '../utils/apiService'
  import type { Post, VoteParams, onVote } from '../utils/apiService'
  import { salaryMapper, ratingsMapper, numCommaFormatter } from '../utils/mappers'
  import Vote from '../lib/Vote.svelte'

  export let posts: Post[]
  export let onVote: onVote
  export let post_type: PostEnum

  const handlePostVote = async (params: VoteParams) => {
    onVote({ ...params, vote_model_type: post_type })
    return
  }
</script>

<div class="REVIEW_CONTAINER w-full divide-y space-y-4">
  {#if posts.length > 0}
    {#each posts as post}
      <div class="REVIEW_CONTENT pt-4 space-y-4">
        <div class="flex justify-between items-center">
          <p class="text-xs font-light italic text-grey-400">{post.account.username}</p>
          <p class="
            text-xs font-light italic px-2 py-1
            rounded-md bg-grey-100
          ">
            {ratingsMapper(post.tag)}</p>
        </div>
        <div class="flex flex-col grid grid-cols-4 gap-x-2 w-full">
          <p class="col-span-2 truncate"><b>Position:</b> {post.position.name}</p>
          <p class="col-span-2 truncate">
              <b>{post_type === PostEnum.REVIEW ? 'Salary' : 'Offer'}</b>
              {`${salaryMapper(post.currency)}${post.compensation > 0 ? numCommaFormatter(post.compensation, 0) : 'NA'}`}
          </p>
          <p class="col-span-2 truncate"><b>Location:</b> {post.location.length > 0 ? post.location : 'NA'}</p>
        </div>
        <p class="text-justify">
            <span class="font-bold">
                Interview:
            </span>
            {@html marked.parse(post.post)}
        </p>
        <div class="w-full flex justify-end">
          <Vote
            post={post}
            onVote={handlePostVote} />
        </div>
      </div>
    {/each}
  {:else}
    <div>No {post_type === PostEnum.INTERVIEW ? 'interviews' : 'reviews'} posts for this company</div>
  {/if}
</div>
