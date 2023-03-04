export const createFilter = (search_index) => {
  /*
   * Accepts a flexsearch index and returns a filter callback that uses this
   * index to filter values for a svelte-select search component.
   * svelte-select dropdown component.
   *
   * All args are passed by svelte-select by default to fitler callback
   */
  const filter = (args) => {
    let {
        loadOptions,
        filterText,
        items,
        multiple,
        value,
        itemId,
        groupBy,
        filterSelectedItems,
        itemFilter,
        convertStringItemsToObjects,
        filterGroupedItems,
        label,
    } = args

    if (items && loadOptions) return items;
    if (!items) return [];

    if (items && items.length > 0 && typeof items[0] !== 'object') {
        items = convertStringItemsToObjects(items);
    }

    // filter results and map the resulting index against the org list index
    let filterResults = items
    if (filterText) {
        filterResults = search_index
        .search(filterText, 100)
        .map((idx: number) => items[idx])
    }

    if (groupBy) {
        filterResults = filterGroupedItems(filterResults);
    }

    return filterResults;
  }

  return filter
}
