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
  export let selected_row: SelectRow
  export let placeholder: string
  export let canClear: boolean = false
  export let onClear: () => void = () => null
  export let onSelect: (row: SelectRow) => void = () => null
  export let shortcut: string = ""
  export let use_window_shortcut: boolean = false
  export let focus_input_on_mount: boolean = false
  export let rows: SelectRow[] = []

  $: menu_open = false
  $: filtered_rows = rows

  let dropdown_ref: HTMLElement
  let input_ref: HTMLInputElement

  onMount(async () => {
    if (focus_input_on_mount) {
      input_ref.focus()
    }
  })

  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape' || e.key == 'Tab') {
      onSelect(selected_row ?? rows[0])
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
    // onSelect(selected_row ?? rows[0])
    setTimeout(() => menu_open = false, 100)
  }

  const buildFilteredRows = (rows: SelectRow[]) => {
    const new_rows = rows.slice()
    const selected_index = rows.findIndex(r => r.value === selected_row?.value) ?? 0
    if (selected_index > 0) {
      const new_top_row: SelectRow[] = new_rows.splice(selected_index, 1)
      new_rows.splice(0, 0, new_top_row[0])
    }
    return new_rows
  }

  const onHandleSelect = (row: SelectRow) => {
    onSelect(row)
    input_ref.focus()
    menu_open = false
    selected_row = row
    filtered_rows = buildFilteredRows(rows)
  }
</script>

<div class="relative" bind:this={dropdown_ref}>
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

  <div
    style="max-height:200px"
    class="absolute w-full overflow-scroll z-10 mt-2 shadow-lg rounded-lg">
    {#if menu_open}
      {#each filtered_rows as row, idx}
        {#if row.value.includes(value)}
          <button
            on:click={() => onHandleSelect(row)}
            class="py-1 px-2 truncate w-full text-left
            hover:bg-grey-100 hover:cursor-pointer
            {idx === 0 ? 'bg-red-500' : '' }
            "
          >
              {row.value}
            </button>
        {/if}
      {/each}
    {/if}
  </div>
</div>
