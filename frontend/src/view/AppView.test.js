import { flushPromises, mount } from '@vue/test-utils'
import { jest } from '@jest/globals'
import App from './AppView.vue'
import api from '../api/api-component-mock.cjs'
const AppComponent = App.default || App

const { getCourse, getCourses, getCurrentUser, logIn, logout, kakaoLogin, createPaymentOrder, confirmPayment } = api

const catalog = [
  { id: 1, title: 'FastAPI', summary: '빠르게 API를 만들어요', category: '백엔드', thumbnail_url: null, instructor_name: '강사', price_krw: 79000, level: '초급', duration_minutes: 120 },
  { id: 2, title: 'Vue 3', summary: '반응형 프론트엔드', category: '프론트엔드', thumbnail_url: null, instructor_name: '강사', price_krw: 69000, level: '중급', duration_minutes: 90 },
  { id: 3, title: 'SQLite/SQLAlchemy', summary: '데이터베이스 기초', category: '데이터베이스', thumbnail_url: null, instructor_name: '강사', price_krw: 59000, level: '초급', duration_minutes: 80 },
]
const detail = { ...catalog[0], description: 'FastAPI로 실전 API를 구현합니다.' }

async function renderList(data = catalog) {
  window.history.replaceState({}, '', '/')
  getCourses.mockResolvedValue(data)
  const wrapper = mount(AppComponent)
  await flushPromises()
  return wrapper
}

afterEach(() => { jest.clearAllMocks(); window.history.replaceState({}, '', '/') })

test('renders course cards with formatted prices', async () => {
  const wrapper = await renderList()
  expect(wrapper.text()).toContain('FastAPI')
  expect(wrapper.text()).toContain('79,000원')
  expect(wrapper.text()).toContain('69,000원')
  expect(wrapper.text()).toContain('59,000원')
})

test('filters catalog by title and category', async () => {
  const wrapper = await renderList()
  await wrapper.get('[aria-label="강의 검색"]').setValue('Vue')
  expect(wrapper.text()).toContain('Vue 3')
  expect(wrapper.text()).not.toContain('FastAPI')
  await wrapper.get('[aria-label="강의 검색"]').setValue('')
  await wrapper.get('.categories button:nth-child(1)').trigger('click')
  await wrapper.get('.categories button:nth-child(2)').trigger('click')
  expect(wrapper.text()).toContain('FastAPI')
  expect(wrapper.text()).not.toContain('Vue 3')
})

test('shows empty catalog state', async () => {
  const wrapper = await renderList([])
  expect(wrapper.text()).toContain('강의가 없어요')
})

test('opens selected course detail', async () => {
  const wrapper = await renderList()
  getCourse.mockResolvedValue(detail)
  await wrapper.get('.course-card').trigger('click')
  await flushPromises()
  expect(window.location.pathname).toBe('/courses/1')
  expect(wrapper.text()).toContain('FastAPI')
  expect(wrapper.text()).toContain(detail.description)
})

test('shows missing thumbnail fallback', async () => {
  const wrapper = await renderList([catalog[0]])
  expect(wrapper.find('.thumbnail span').exists()).toBe(true)
})

test('shows fallback when thumbnail fails to load', async () => {
  const withImage = { ...catalog[0], thumbnail_url: '/missing.png' }
  const wrapper = await renderList([withImage])
  const image = wrapper.find('.thumbnail img')
  expect(image.exists()).toBe(true)
  await image.trigger('error')
  expect(wrapper.find('.thumbnail span').exists()).toBe(true)
  expect(wrapper.find('.thumbnail img').exists()).toBe(false)
})

test('shows unknown detail error', async () => {
  window.history.replaceState({}, '', '/courses/999')
  getCourse.mockRejectedValue(new Error('강의를 찾을 수 없습니다.'))
  const wrapper = mount(AppComponent)
  await flushPromises()
  expect(wrapper.find('[role="alert"]').text()).toContain('강의를 찾을 수 없습니다.')
})

test('asks a guest to log in before creating a payment', async () => {
  const wrapper = await renderList()
  getCourse.mockResolvedValue(detail)
  await wrapper.vm.go('/courses/1')
  await flushPromises()
  await wrapper.get('.purchase-button').trigger('click')
  expect(window.location.pathname).toBe('/login')
  expect(createPaymentOrder).not.toHaveBeenCalled()
})

test('requests a Toss test payment and confirms it with the server', async () => {
  window.history.replaceState({}, '', '/login')
  logIn.mockResolvedValue({ email: 'buyer@example.com' })
  getCourses.mockResolvedValue(catalog)
  const wrapper = mount(AppComponent)
  await wrapper.get('input[type="email"]').setValue('buyer@example.com')
  await wrapper.get('input[type="password"]').setValue('pass')
  await wrapper.get('form').trigger('submit')
  await flushPromises()
  getCourse.mockResolvedValue(detail)
  await wrapper.vm.go('/courses/1')
  await flushPromises()
  createPaymentOrder.mockResolvedValue({ payment_id: 'course-1-test', order_name: 'FastAPI', amount_krw: 79000, store_id: 'store-test', channel_key: 'channel-test' })
  confirmPayment.mockResolvedValue({ status: 'PAID' })
  window.PortOne = { requestPayment: jest.fn().mockResolvedValue({ paymentId: 'course-1-test' }) }

  await wrapper.get('.purchase-button').trigger('click')
  await flushPromises()

  expect(window.PortOne.requestPayment).toHaveBeenCalledWith(expect.objectContaining({ storeId: 'store-test', channelKey: 'channel-test', paymentId: 'course-1-test', totalAmount: 79000, currency: 'KRW', payMethod: 'CARD' }))
  expect(confirmPayment).toHaveBeenCalledWith('course-1-test')
  expect(wrapper.text()).toContain('강의 구매가 완료됐어요.')
  delete window.PortOne
})

test('confirms a payment returned by the mobile redirect', async () => {
  window.history.replaceState({}, '', '/courses/1?paymentId=course-1-redirect')
  getCourse.mockResolvedValue(detail)
  confirmPayment.mockResolvedValue({ status: 'PAID' })
  const wrapper = mount(AppComponent)
  await flushPromises()
  expect(confirmPayment).toHaveBeenCalledWith('course-1-redirect')
  expect(window.location.search).toBe('')
  expect(wrapper.text()).toContain('강의 구매가 완료됐어요.')
})

test('restores the authenticated session before allowing a course purchase', async () => {
  window.history.replaceState({}, '', '/courses/1')
  getCurrentUser.mockResolvedValue({ name: '모아' })
  getCourse.mockResolvedValue(detail)
  createPaymentOrder.mockResolvedValue({ payment_id: 'restored-session-order', order_name: 'FastAPI', amount_krw: 79000, store_id: 'store-test', channel_key: 'channel-test' })
  confirmPayment.mockResolvedValue({ status: 'PAID' })
  window.PortOne = { requestPayment: jest.fn().mockResolvedValue({ paymentId: 'restored-session-order' }) }

  const wrapper = mount(AppComponent)
  await flushPromises()
  await wrapper.get('.purchase-button').trigger('click')
  await flushPromises()

  expect(getCurrentUser).toHaveBeenCalled()
  expect(createPaymentOrder).toHaveBeenCalledWith(1)
  expect(window.location.pathname).toBe('/courses/1')
  expect(wrapper.text()).toContain('강의 구매가 완료됐어요.')
  delete window.PortOne
})

test('logs out through the backend and clears the authenticated header', async () => {
  window.history.replaceState({}, '', '/')
  getCurrentUser.mockResolvedValue({ name: '모아' })
  getCourses.mockResolvedValue(catalog)
  logout.mockResolvedValue(null)

  const wrapper = mount(AppComponent)
  await flushPromises()
  expect(wrapper.text()).toContain('로그아웃')

  const logoutButton = wrapper.findAll('button').find((button) => button.text() === '로그아웃')
  await logoutButton.trigger('click')
  await flushPromises()

  expect(logout).toHaveBeenCalled()
  expect(window.location.pathname).toBe('/')
  expect(wrapper.text()).not.toContain('로그아웃')
  expect(wrapper.text()).toContain('로그인')
})

test('preserves the Kakao authorization code and completes login from its callback', async () => {
  const authorizationCode = 'kakao-authorization-code'
  window.history.replaceState({}, '', `/login/kakao/callback?code=${authorizationCode}&state=csrf-state`)
  window.sessionStorage.setItem('kakao_login_state', 'csrf-state')
  kakaoLogin.mockResolvedValue({ nickname: '모아' })

  const wrapper = mount(AppComponent)
  await flushPromises()

  expect(kakaoLogin).toHaveBeenCalledWith(authorizationCode)
  expect(window.location.pathname).toBe('/')
  expect(wrapper.text()).toContain('모아')
  expect(wrapper.text()).not.toContain('결제가 취소되었거나 실패했습니다.')
})
