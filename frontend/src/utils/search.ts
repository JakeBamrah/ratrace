export const createFilter = (search_index, original_items) => {
  /*
   * Accepts a flexsearch index and returns a filter callback which is used to
   * search and index filter values for a svelte-select search component.
   * The original_items list is also passed because the select dropdown is only
   * given 500 items max and therefore is not capable of searching more than
   * 500 items.
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
        .map((idx: number) => original_items[idx])
    }

    if (groupBy) {
        filterResults = filterGroupedItems(filterResults);
    }

    return filterResults;
  }

  return filter
}


export const default_filter = ({
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
  label
}) => {

  if (items && loadOptions) return items;

  if (!items) return [];

  if (items && items.length > 0 && typeof items[0] !== 'object') {
    items = convertStringItemsToObjects(items);
  }

  let filterResults = items.filter((item) => {
    let matchesFilter = itemFilter(item[label], filterText, item);
    if (matchesFilter && multiple && value?.length) {
      matchesFilter = !value.some((x) => {
        return filterSelectedItems ? x[itemId] === item[itemId] : false;
      });
    }
    return matchesFilter;
  });

  if (groupBy) {
    filterResults = filterGroupedItems(filterResults);
  }

  return filterResults;
}
