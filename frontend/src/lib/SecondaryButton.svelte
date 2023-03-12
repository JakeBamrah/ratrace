<script lang="ts">
  import { current_component } from "svelte/internal"

  import { getEventsAction } from "../utils/events"

  const events = getEventsAction(current_component);
</script>

<button use:events class="hover:underline">
  <slot></slot>
</button>
