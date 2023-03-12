<script lang="ts">
  import { marked } from 'marked'

  import { VoteModelEnum } from '../utils/apiService'
  import type { Review, onVote, VoteParams } from '../utils/apiService'
  import { salaryMapper, ratingsMapper, numCommaFormatter, yearFormatter } from '../utils/mappers'
  import { formatTimestamp } from '../utils/timeago'
  import Vote from '../lib/Vote.svelte'

  export let reviews: Review[]
  export let onVote: onVote

  const handleReviewVote = async (params: VoteParams) => {
    onVote({ ...params, vote_model_type: VoteModelEnum.REVIEW })
    return
  }
 // [{formatTimestamp(review.created_at)}]
</script>

<div class="REVIEW_CONTAINER w-full divide-y space-y-4">
  {#if reviews.length > 0}
    {#each reviews as review}
      <div class="REVIEW_CONTENT pt-4 space-y-4">
        <div class="flex justify-between items-center">
          <p class="
            text-xs italic w-24 w:28 truncate
            font-light text-grey-400
          ">{review.account.username}</p>
          <p class="
            text-xs font-light italic px-2 py-1
            rounded-md bg-grey-100
          ">
            {ratingsMapper(review.tag)}</p>
        </div>
        <div class="flex flex-col grid grid-cols-4 gap-x-2 w-full">
          <p class="col-span-2 truncate"><b>Position:</b> {review.position.name}</p>
          <p class="col-span-2 truncate">
            <b>Salary:</b>
            {`${salaryMapper(review.currency)}${review.salary > 0 ? numCommaFormatter(review.salary, 0) : 'NA'}`}
          </p>
          <p class="col-span-2 truncate">
            <b>Location:</b>
            {review.location.length > 0 ? review.location : 'NA'}
          </p>
          <p class="col-span-2 truncate">
            <b>Tenure:</b>
            {review.duration_years > 0 ? `${yearFormatter(review.duration_years)}` : 'NA'}
          </p>
        </div>
        <p class="text-justify">
            <span class="font-bold">
                Review:
            </span>
            {@html marked.parse(review.post)}
        </p>
        <div class="w-full flex justify-end">
          <Vote
            post={review}
            onVote={handleReviewVote} />
        </div>
      </div>
    {/each}
  {:else}
    <div>No reviews for this company</div>
  {/if}
</div>
