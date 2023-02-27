<script lang="ts" context="module">
  export type SelectRow = {
    id: string | number
    value: string
  }
</script>

<script lang="ts">
  import Input from './Input.svelte'
  import { onMount } from 'svelte'


  export let id: string
  export let value: string
  export let placeholder: string
  export let canClear: boolean = false
  export let onClear: () => void = () => null
  export let onSelect: (row: SelectRow) => void = () => null
  export let shortcut: string = ""
  export let use_window_shortcut: boolean = false
  export let focus_input_on_mount: boolean = false
  export let rows: SelectRow[] = []

  $: menu_open = false

  let dropdown_ref: HTMLElement
  let input_ref: HTMLInputElement

  onMount(async () => {
    if (focus_input_on_mount) {
      input_ref.focus()
    }
  })

  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape' || e.key == 'Tab') {
      menu_open = false
      return
    }

    if (e.key === 'Enter') {
      // if we allow any free_text act as normal
      // if we have to select something, take the top item from filtered list
      // or take nothing
      menu_open = false
      return
    }

    menu_open = true
  }

  const onHandleFocus = (e: Event) => {
    const target = e.target as HTMLElement
    if (dropdown_ref.contains(target)) {
        menu_open = true
        return
    }
  }

  const onHandleBlur = (e: Event) => {
    // if div children aren't focused then close
    setTimeout(() => menu_open = false, 100)
  }

  const onHandleSelect = (row: SelectRow) => {
    onSelect(row)
    input_ref.focus()
    menu_open = false
  }
</script>

<div bind:this={dropdown_ref}>
  <Input
    id={id}
    bind:value={value}
    placeholder={placeholder}
    canClear={canClear}
    onClear={onClear}
    onFocus={onHandleFocus}
    onBlur={onHandleBlur}
    onKeyDown={onKeyDown}
    shortcut={shortcut}
    use_window_shortcut={use_window_shortcut}
    bind:ref={input_ref}
  />

  <div>
    {#if menu_open}
      {#each rows as row}
        {#if row.value.includes(value)}
          <div on:click={() => onHandleSelect(row)}>{row.value}</div>
        {/if}
      {/each}
    {/if}
  </div>
</div>
