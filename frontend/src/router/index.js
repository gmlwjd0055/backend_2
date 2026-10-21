export function resolveRoute(pathname = window.location.pathname) {
  const path = pathname.replace(/\/$/, '') || '/'
  if (path === '/signup') return { name: 'signup' }
  if (path === '/login/kakao/callback') return { name: 'kakaoCallback' }
  if (path === '/login') return { name: 'login' }
  const course = path.match(/^\/courses\/(\d+)$/)
  return course ? { name: 'detail', id: Number(course[1]) } : { name: 'list' }
}
