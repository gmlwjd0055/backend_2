import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const componentFiles = [
  'StayHeader.vue',
  'StaySearchBar.vue',
  'StayCategoryNav.vue',
  'StayListingCard.vue',
  'StayPhotoGallery.vue',
  'StayBookingCard.vue',
  'StayListingSummary.vue',
  'StayAuthForm.vue',
  'StayFilterButton.vue',
]

test.each(componentFiles)('%s is a scoped, reusable Vue component with the requested brand accent', filename => {
  const source = readFileSync(fileURLToPath(new URL(filename, import.meta.url)), 'utf8')
  expect(source).toContain('<template>')
  expect(source).toContain('<style scoped>')
  expect(source).toContain('#FAED7D')
})

test('components barrel exports discovery, detail, and account building blocks', () => {
  const exports = readFileSync(fileURLToPath(new URL('index.js', import.meta.url)), 'utf8')
  for (const component of ['StayHeader', 'StaySearchBar', 'StayCategoryNav', 'StayListingCard', 'StayPhotoGallery', 'StayBookingCard', 'StayListingSummary', 'StayAuthForm', 'StayFilterButton']) {
    expect(exports).toContain(`as ${component}`)
  }
})
