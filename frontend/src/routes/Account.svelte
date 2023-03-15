<script lang="ts">
  import { useNavigate } from 'svelte-navigator'
  import { onMount } from 'svelte'

  import PageContainer from '../lib/PageContainer.svelte'
  import { account } from '../utils/apiService'
  import type { AccountQueryParams } from '../utils/apiService'
  import Button from '../lib/Button.svelte'
  import Tabs from '../lib/Tabs.svelte'
  import SecondaryButton from '../lib/SecondaryButton.svelte'


  export let onAccountUpdate: (params: AccountQueryParams) => Promise<boolean>
  export let onLogout: () => void

  const navigate = useNavigate()

  const handleLogout = () => {
    onLogout()
    navigate('/')
  }

  const theme_tabs = [{ id: 'Dark', value: 'Dark'}, { id: 'Light', value: 'Light'}]
  let theme_selected_tab = $account?.dark_mode ? theme_tabs[0] : theme_tabs[1]

  const anonymous_tabs = [{ id: 'Yes', value: 'Yes'}, { id: 'No', value: 'No'}]
  let anonymous_selected_tab = $account?.anonymous ? anonymous_tabs[0] : anonymous_tabs[1]

  const onThemeSelect = async (tab: { id: any, value: string }) => {
    if (tab === theme_selected_tab)
      return

    theme_selected_tab = tab
    const dark_mode = tab.id === 'Dark'
    await onAccountUpdate({ dark_mode })
    return
  }

  const onAnonymousSelect = async (tab: { id: any, value: string }) => {
    if (tab === anonymous_selected_tab)
      return

    anonymous_selected_tab = tab
    const anonymous = tab.id === 'Yes'
    await onAccountUpdate({ anonymous })
    return
  }

  // check if account has access and pull in account data on mount
  onMount(() => {
    if (!$account?.id) {
      navigate('/login')
    }
  })
  /* reviews?: Review[] */
  /* interviews?: Interview[] */
</script>

<PageContainer>
  <div class="px-6 py-4 border w-full rounded-xl space-y-4">
    <p class="text-2xl text-grey-700">Account</p>
    <div class="space-y-2">
    <p><b>Username:</b> {$account?.username} <span class="text-grey-400 text-xs">(#{$account?.id})</span></p>
    <div>
      <b>Theme:</b>
      <Tabs
        left_tabs={theme_tabs}
        selected_tab={theme_selected_tab}
        onTabSelect={onThemeSelect} />
    </div>
    <div>
      <b>Anonymous posting:</b>
      <Tabs
        left_tabs={anonymous_tabs}
        selected_tab={anonymous_selected_tab}
        onTabSelect={onAnonymousSelect} />
    </div>
    </div>
    <div class="flex justify-end space-x-4 border-t pt-4">
      <SecondaryButton on:click={() => navigate('/')}>Back</SecondaryButton>
      <Button on:click={handleLogout}>Logout</Button>
    </div>
  </div>
</PageContainer>
