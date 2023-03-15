<script lang="ts" context="module">
  export const createFocusInputShortcut = (input_id: string, use_window_shortcut: boolean) => {
    if (!use_window_shortcut) {
        return
    }

    const is_apple = /(Mac|iPhone|iPod|iPad)/i.test(navigator.userAgent);
    const onWindowKeyDown = (e: any) => {
      if (is_apple && e.metaKey && e.key === '/') {
        const input_el = document.getElementById(input_id)
        input_el.focus()
        return
      }
      if (e.ctrlKey && e.key === '/') {
        const input_el = document.getElementById(input_id)
        input_el.focus()
        return
      }
    }

    return onWindowKeyDown
  }
</script>

<script setup lang="ts">
  import { current_component } from "svelte/internal"
  import { icons } from 'feather-icons'

  import { getEventsAction } from "../utils/events"


  export let id: string
  export let value: string
  export let label: string = null
  export let placeholder: string
  export let canClear: boolean = false
  export let onClear: () => void = () => null
  export let onFocus: (e: Event) => void = () => null
  export let onBlur: (e: Event) => void = () => null
  export let onKeyDown: (e: Event) => void = () => null
  export let shortcut: string = ''
  export let use_window_shortcut: boolean = false
  export let ref: HTMLInputElement = null
  export let type: string = 'text'
  export let text_area: boolean = false
  export let error: boolean = false
  export let errorMessage: string = null

  let original_value = ""
  $: empty = value?.length === 0

  const events = getEventsAction(current_component);

  const onHandleInput =(e: Event) => {
    const target = e.target as HTMLInputElement
    value = target.value
  }

  const onHandleBlur = (e: Event) => {
    // store original value on clickaways too
    // the new_value has been handled by either the onChange or keyHandler
    // by this point so we can be sure of value correctness
    original_value = value.trim()
    onBlur(e)
  }

  const onHandleKeyDown = (e: KeyboardEvent) => {
    onKeyDown(e)

    const target = e.target as HTMLInputElement
    if (e.key === 'Escape') {
      // restore the original value on escape, unless the input was left empty
      if (value.trim().length === 0) {
        target.blur()
        value = ""
        original_value = ""
        return
      }
      value = original_value
      target.blur()
      return
    }
    if (e.key === 'Enter') {
      value = value.trim()
      target.blur()
      return
    }
  }
</script>

<svelte:window on:keydown={createFocusInputShortcut(id, use_window_shortcut)}/>

<div>
  {#if label}
    <p class="text-xs font-extralight pb-1 text-grey-400">{label}</p>
  {/if}
  <div
    class="
      w-full px-4 py-2 relative flex items-center text-black
      bg-grey-100 dark:bg-dark-400 rounded-lg border
      { error ? 'border-red-300' : 'border-grey-100' }
    ">
    {#if text_area}
      <textarea
        id={id}
        placeholder={placeholder}
        on:input={onHandleInput}
        on:blur={onHandleBlur}
        on:keydown={onHandleKeyDown}
        on:focus={onFocus}
        bind:value={value}
        class="
          w-full bg-grey-100 h-24 resize-none pt-1
          border-none focus:outline-none ring-0
        "
        ></textarea>
    {:else}
      <input
        id={id}
        placeholder={placeholder}
        on:input={onHandleInput}
        on:blur={onHandleBlur}
        on:keydown={onHandleKeyDown}
        on:focus={onFocus}
        bind:this={ref}
        type={type}

        use:events
        {value}
        class="
          {canClear && !empty ? 'mr-6' : ''}
          border-none focus:outline-none ring-0 w-full
          font-light placeholder-grey-350 dark:placeholder-dark-300 truncate
          bg-transparent dark:bg-dark-400
        "/>
    {/if}
    {#if empty && shortcut}
      <div class="hidden sm:block absolute right-0 text-xs mr-4">
        <span class="flex text-grey-350 dark:text-dark-300 ">
          <span>{shortcut}</span>
        </span>
        <span class="shortcut-slash ml-1 font-semibold"> / </span>
      </div>
    {/if}
    {#if !empty && canClear}
      <button
        on:click={onClear}
        class="
          absolute right-0 text-xs mr-4 cursor-pointer
          hover:bg-white dark:hover:bg-dark-500 rounded-xl p-0.5
        " >
        <span class="text-grey-350 dark:text-dark-300 ">
          {@html icons.x.toSvg({ height: 24, width: 24 })}
        </span>
      </button>
    {/if}
  </div>
    {#if error && errorMessage}
    <p
      class="
        absolute text-xs w-full truncate font-extralight pb-1 text-grey-400
      ">
        {errorMessage}
    </p>
    {/if}
</div>
