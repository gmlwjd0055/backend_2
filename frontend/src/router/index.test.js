import { resolveRoute } from './index.js'

test.each([
  ['/', { name: 'list' }],
  ['/login', { name: 'login' }],
  ['/signup', { name: 'signup' }],
  ['/login/kakao/callback', { name: 'kakaoCallback' }],
  ['/courses/42', { name: 'detail', id: 42 }],
])('resolves %s to its route', (path, route) => {
  expect(resolveRoute(path)).toEqual(route)
})
