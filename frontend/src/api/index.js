const apiBaseUrl = (import.meta.env?.VITE_API_BASE_URL ?? '').replace(/\/$/, '')

async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`${apiBaseUrl}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
      credentials: 'include',
    })
  } catch {
    throw new Error('서버에 연결할 수 없습니다. 백엔드가 실행 중인지 확인해 주세요.')
  }
  const payload = await response.json().catch(() => null)
  if (!response.ok || payload?.code >= 400) {
    throw new Error(payload?.message || '요청을 처리하지 못했습니다.')
  }
  return payload?.result
}

export const getBoards = () => request('/board/list')
export const getBoard = (idx) => request(`/board/read/${idx}`)
export const createBoard = (data) => request('/board/register', { method: 'POST', body: JSON.stringify(data) })
export const signUp = (data) => request('/user/signup', { method: 'POST', body: JSON.stringify(data) })
export const logIn = (data) => request('/user/login', { method: 'POST', body: JSON.stringify(data) })
export const kakaoLogin = (code) => request('/user/kakao-login', { method: 'POST', body: JSON.stringify({ code }) })
export const getCurrentUser = () => request('/user/me')
export const getCourses = () => request('/courses')
export const getCourse = (id) => request(`/courses/${id}`)
export const createPaymentOrder = (courseId) => request('/payments/orders', { method: 'POST', body: JSON.stringify({ course_id: courseId }) })
export const confirmPayment = (paymentId) => request('/payments/confirm', { method: 'POST', body: JSON.stringify({ payment_id: paymentId }) })
