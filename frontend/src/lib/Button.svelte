<script lang="ts">
  import { current_component } from "svelte/internal"

  import { getEventsAction } from "../utils/events"


  export let disabled = false

  const events = getEventsAction(current_component);
</script>

<button
  use:events
  disabled={disabled}
  class="
    px-3 py-1.5
    border border-grey-200 active:bg-grey-100 font-medium rounded-lg
    focus:outline-none focus:border-grey-300 text-grey-700
    disabled:text-grey-300
  ">
  <slot></slot>
</button>
