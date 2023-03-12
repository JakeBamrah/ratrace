<script lang="ts">
  import  { VoteModelEnum } from '../utils/apiService'
  import type { Interview, VoteParams, onVote } from '../utils/apiService'
  import { salaryMapper, ratingsMapper, numCommaFormatter } from '../utils/mappers'
  import Vote from '../lib/Vote.svelte'

  export let interviews: Interview[]
  export let onVote: onVote

  const handleInterviewVote = async (params: VoteParams) => {
    onVote({ ...params, vote_model_type: VoteModelEnum.INTERVIEW })
    return
  }
</script>

<div class="REVIEW_CONTAINER w-full divide-y space-y-4">
  {#if interviews.length > 0}
    {#each interviews as interview}
      <div class="REVIEW_CONTENT pt-4 space-y-4">
        <div class="flex justify-between items-center">
          <p class="text-xs font-light italic text-grey-400">{interview.account.username}</p>
          <p class="
            text-xs font-light italic px-2 py-1
            rounded-md bg-grey-100
          ">
            {ratingsMapper(interview.tag)}</p>
        </div>
        <div class="flex flex-col grid grid-cols-4 gap-x-2 w-full">
          <p class="col-span-2 truncate"><b>Position:</b> {interview.position.name}</p>
          <p class="col-span-2 truncate">
            <b>Offer:</b>
            {`${salaryMapper(interview.currency)}${interview.offer > 0 ? numCommaFormatter(interview.offer, 0) : 'NA'}`}
          </p>
          <p class="col-span-2 truncate"><b>Location:</b> {interview.location.length > 0 ? interview.location : 'NA'}</p>
        </div>
        <p class="text-justify">
            <span class="font-bold">
                Interview:
            </span>
            {interview.interview}
        </p>
        <div class="w-full flex justify-end">
          <Vote
            post={interview}
            onVote={handleInterviewVote} />
        </div>
      </div>
    {/each}
  {:else}
    <div>No interviews for this company</div>
  {/if}
</div>
