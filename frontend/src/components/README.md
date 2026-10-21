# Stay UI components

Airbnb-style discovery, listing detail, and account components for Vue 3. The components are presentation-focused and communicate through props, slots, and emitted events so they can be reused without coupling to a page or API. The brand accent is `#FAED7D`.

```vue
<script setup>
import { StayHeader, StaySearchBar, StayCategoryNav, StayListingCard } from '../components'
import { ref } from 'vue'

const category = ref('all')
const categories = [
  { id: 'all', label: '전체', icon: '⌂' },
  { id: 'cabin', label: '통나무집', icon: '⌂' },
]
</script>

<template>
  <StayHeader @login="openLogin" />
  <StaySearchBar @search="loadListings" />
  <StayCategoryNav v-model="category" :categories="categories" @filter="openFilters" />
  <StayListingCard :listing="listing" @select="openDetail" @favorite="toggleFavorite" />
</template>
```

`StayPhotoGallery`, `StayListingSummary`, and `StayBookingCard` compose the listing detail page. `StayAuthForm` handles both sign-in and sign-up through its `mode` prop and emits form data via `submit`.
