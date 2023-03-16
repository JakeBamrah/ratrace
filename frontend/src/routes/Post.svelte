<script lang="ts">
  import { marked } from 'marked'
  import DOMPurify from 'dompurify'
  import { Trash, Flag } from 'lucide-svelte';

  import { account, PostEnum } from '../utils/apiService'
  import type { Post, onVote } from '../utils/apiService'
  import { salaryMapper, ratingsMapper, numCommaFormatter, yearFormatter } from '../utils/mappers'
  import Vote from '../lib/Vote.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'

  export let post: Post
  export let onVote: onVote
  export let post_type: PostEnum
  export let onDeletePost: (post_id: number) => void
  export let onReportPost: (post_id: number) => void

  let read_more = false
  const long_post = post.post.length > 700

  const sanitize_config = { USE_PROFILES: { html: true } }
  $: is_review = post_type === PostEnum.REVIEW

  let reported = false
</script>

<div class="REVIEW_CONTENT pt-4 space-y-4">
  <div class="flex justify-between items-center">
    <p class="text-xs font-light italic text-grey-400">{post.account.username}</p>
    <div class="flex space-x-2">
        {#if $account?.id === post.account.id}
          <SecondaryButton
            on:click={() => onDeletePost(post.id)}>
            <Trash class="h-4 w-4 text-grey-500" />
          </SecondaryButton>
        {/if}
        {#if $account?.id}
          <SecondaryButton
            on:click={() => { onReportPost(post.id); reported = true }}>
            <Flag class="h-4 w-4 { reported? 'text-red-400' : 'text-grey-500 ' }" />
          </SecondaryButton>
        {/if}
      <p class="
        text-xs font-light italic px-2 py-1
        rounded-md bg-grey-100
      ">
        {ratingsMapper(post.tag)}</p>
      </div>
  </div>
  <div class="flex flex-col grid grid-cols-4 gap-x-2 w-full">
    <p class="col-span-4 sm:col-span-2 truncate"><b>Position:</b> {post.position.name}</p>
    <p class="col-span-4 sm:col-span-2 truncate">
        <b>{is_review ? 'Salary' : 'Offer'}</b>
        {`${salaryMapper(post.currency)}${post.compensation > 0 ? numCommaFormatter(post.compensation, 0) : 'n.a'}`}
    </p>
    <p class="col-span-4 sm:col-span-2 truncate">
      <b>Location:</b>
      {post.location.length > 0 ? post.location : 'n.a'}
    </p>
    {#if is_review}
      <p class="col-span-4 sm:col-span-2 truncate">
        <b>Tenure:</b>
        {post.duration_years > 0 ? `${yearFormatter(post.duration_years)}` : 'n.a'}
      </p>
    {:else}
      <p class="col-span-4 sm:col-span-2 truncate">
        <b>Stages completed:</b>
        {post.stages > 0 ? post.stages : 'n.a'}
      </p>
    {/if}
  </div>
  <div class="text-justify relative">
      <b class="font-bold">
        {is_review ? 'Review:' : 'Interview:'}
      </b>
      <div
        class="
          space-y-4
          {long_post ? read_more ? 'h-full' : 'h-56 overflow-hidden' : 'h-full'}
          ">
        {@html DOMPurify.sanitize(marked.parse(post.post), sanitize_config)}
      </div>
      {#if long_post}
        <div
          class="
            READ_MORE_BUTTON
            space-y-4 w-full h-10 absolute bottom-0
            text-center pt-12
            {read_more ? '' : 'bg-gradient-to-t from-white to-transparent'}
          ">
            <SecondaryButton
              on:click={() => read_more = !read_more}>
              { read_more ? 'Hide' : 'Read more' }
            </SecondaryButton>
        </div>
      {/if}
  </div>
  <div class="w-full flex justify-end">
    <Vote
      post={post}
      onVote={onVote} />
  </div>
</div>
