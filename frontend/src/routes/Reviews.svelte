<script lang="ts">
  export let reviews
</script>

<div class="w-full divide-y space-y-4">
  {#if reviews.length > 0}
    {#each reviews as review}
    <div class="pt-4">
      <div class="flex justify-between">
        <p class="text-xs font-light italic">{review.account.username}</p>
        <p class="text-xs font-light italic">{review.tag}</p>
      </div>
      <div class="flex flex-col grid grid-cols-4 gap-y-2 pt-2">
      <p class
      </div>
      </div>
    {/each}
  {:else}
    <div>No reviews for this company</div>
  {/if}
</div>
