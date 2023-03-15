<script lang="ts">
  import { marked } from 'marked'
  import DOMPurify from 'dompurify'
  import { icons } from 'feather-icons'

  import { account, PostEnum } from '../utils/apiService'
  import type { Post, VoteParams, onVote } from '../utils/apiService'
  import { salaryMapper, ratingsMapper, numCommaFormatter, yearFormatter } from '../utils/mappers'
  import Vote from '../lib/Vote.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'

  export let posts: Post[]
  export let onVote: onVote
  export let post_type: PostEnum
  export let onDeletePost: (post_id: number) => void

  const sanitize_config = { USE_PROFILES: { html: true } }
  $: is_review = post_type === PostEnum.REVIEW


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
          <div class="flex space-x-2">
            <p class="
              text-xs font-light italic px-2 py-1
              rounded-md bg-grey-100
            ">
              {ratingsMapper(post.tag)}</p>
              {#if $account?.id === post.account.id}
                <SecondaryButton
                  on:click={() => onDeletePost(post.id)}>
                  {@html icons.trash.toSvg({ class: 'h-4 w-4'})}
                </SecondaryButton>
              {/if}
            </div>
        </div>
        <div class="flex flex-col grid grid-cols-4 gap-x-2 w-full">
          <p class="col-span-4 sm:col-span-2 truncate"><b>Position:</b> {post.position.name}</p>
          <p class="col-span-4 sm:col-span-2 truncate">
              <b>{is_review ? 'Salary' : 'Offer'}</b>
              {`${salaryMapper(post.currency)}${post.compensation > 0 ? numCommaFormatter(post.compensation, 0) : 'NA'}`}
          </p>
          <p class="col-span-4 sm:col-span-2 truncate">
            <b>Location:</b>
            {post.location.length > 0 ? post.location : 'NA'}
          </p>
          {#if is_review}
            <p class="col-span-4 sm:col-span-2 truncate">
              <b>Tenure:</b>
              {post.duration_years > 0 ? `${yearFormatter(post.duration_years)}` : 'NA'}
            </p>
          {:else}
            <p class="col-span-4 sm:col-span-2 truncate">
              <b>Stages completed:</b>
              {post.stages > 0 ? post.stages : 'NA'}
            </p>
          {/if}
        </div>
        <p class="text-justify">
            <span class="font-bold">
              {is_review ? 'Review' : 'Interview'}
            </span>
            {@html DOMPurify.sanitize(marked.parse(post.post), sanitize_config)}
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
