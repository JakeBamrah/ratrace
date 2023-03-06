<script lang="ts">
  import { salaryMapper, ratingsMapper, numCommaFormatter } from '../utils/mappers'
  import Vote from '../lib/Vote.svelte'

  export let reviews
</script>

<div class="REVIEW_CONTAINER w-full divide-y space-y-4">
  {#if reviews.length > 0}
    {#each reviews as review}
      <div class="REVIEW_CONTENT pt-4 space-y-4">
        <div class="flex justify-between items-center">
          <p class="text-xs font-light italic text-grey-400">{review.account.username}</p>
          <p class="
            text-xs font-light italic px-2 py-1
            rounded-md bg-grey-100
          ">
            {ratingsMapper(review.tag)}</p>
        </div>
        <div class="flex flex-col grid grid-cols-4 gap-x-2 w-full">
          <p class="col-span-2 text-sm truncate"><b>Position:</b> {review.position}</p>
          <p class="col-span-2 text-sm truncate">
            <b>Salary:</b>
            {`${salaryMapper(review.currency)}${review.salary > 0 ? numCommaFormatter(review.salary, 0) : 'NA'}`}
          </p>
          <p class="col-span-2 text-sm truncate"><b>Location:</b> {review.location.length > 0 ? review.location : 'NA'}</p>
          <p class="col-span-2 text-sm truncate"><b>Tenure:</b> {review.duration_years > 0 ? `${numCommaFormatter(review.duration_years, 0)}y` : 'NA'}</p>
        </div>
        <p class="text-justify text-sm">
            <span class="font-bold text-sm">
                Review:
            </span>
            {review.review}
        </p>
        <div class="w-full flex justify-end">
          <Vote
            upvotes={review.upvotes}
            downvotes={review.downvotes}
            onVote={(vote) => console.log(vote)} />
        </div>
      </div>
    {/each}
  {:else}
    <div>No reviews for this company</div>
  {/if}
</div>
