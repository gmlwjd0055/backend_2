import { createBoard, getBoards, getCourse, getCourses, getCurrentUser, kakaoLogin, logout, createPaymentOrder, confirmPayment } from './index.js'
import { jest } from '@jest/globals'

const originalFetch = global.fetch
describe('API envelope handling', () => {
  beforeEach(() => { global.fetch = jest.fn() })
  afterEach(() => {
    if (originalFetch === undefined) delete global.fetch
    else global.fetch = originalFetch
  })

  it('returns the result field from a successful backend envelope', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => ({ code: 200, message: 'success', result: [{ idx: 3, title: '산책', contents: '바람이 좋았다' }] }) })
    await expect(getBoards()).resolves.toEqual([{ idx: 3, title: '산책', contents: '바람이 좋았다' }])
    expect(fetch).toHaveBeenCalledWith('/board/list', expect.objectContaining({ credentials: 'include' }))
  })

  it('surfaces the backend message on an error response', async () => {
    global.fetch.mockResolvedValue({ ok: false, json: async () => ({ code: 400, message: '이미 가입된 이메일입니다.', result: null }) })
    await expect(createBoard({ title: '제목', contents: '내용' })).rejects.toThrow('이미 가입된 이메일입니다.')
  })

  it('exchanges a Kakao authorization code with the backend', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => ({ code: 200, message: 'success', result: { nickname: '모아' } }) })

    await expect(kakaoLogin('auth-code')).resolves.toEqual({ nickname: '모아' })
    expect(fetch).toHaveBeenCalledWith('/user/kakao-login', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ code: 'auth-code' }),
      credentials: 'include',
    }))
  })

  it('fetches the current user through the same-origin session endpoint', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => ({ code: 200, message: 'success', result: { name: '모아' } }) })
    await expect(getCurrentUser()).resolves.toEqual({ name: '모아' })
    expect(fetch).toHaveBeenCalledWith('/user/me', expect.objectContaining({ credentials: 'include' }))
  })

  it('clears the server session through the logout endpoint', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => ({ code: 200, result: null }) })
    await expect(logout()).resolves.toBeNull()
    expect(fetch).toHaveBeenCalledWith('/user/logout', expect.objectContaining({
      method: 'POST',
      credentials: 'include',
    }))
  })

  it('getCourses requests the public catalog', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => ({ code: 200, message: 'success', result: [{ id: 1, title: 'FastAPI' }] }) })
    await expect(getCourses()).resolves.toEqual([{ id: 1, title: 'FastAPI' }])
    expect(fetch).toHaveBeenCalledWith('/courses', expect.objectContaining({ credentials: 'include' }))
  })

  it('getCourse requests the selected detail and propagates errors', async () => {
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ code: 200, result: { id: 2, description: '상세' } }) })
    await expect(getCourse(2)).resolves.toEqual({ id: 2, description: '상세' })
    global.fetch.mockResolvedValueOnce({ ok: false, json: async () => ({ code: 404, message: '강의를 찾을 수 없습니다.' }) })
    await expect(getCourse(99)).rejects.toThrow('강의를 찾을 수 없습니다.')
  })

  it('creates a course payment order and confirms it with the backend', async () => {
    global.fetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({ code: 200, result: { payment_id: 'course-1-test', amount_krw: 79000 } }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ code: 200, result: { status: 'PAID' } }) })
    await expect(createPaymentOrder(1)).resolves.toMatchObject({ amount_krw: 79000 })
    expect(fetch).toHaveBeenNthCalledWith(1, '/payments/orders', expect.objectContaining({ method: 'POST', body: JSON.stringify({ course_id: 1 }), credentials: 'include' }))
    await expect(confirmPayment('course-1-test')).resolves.toEqual({ status: 'PAID' })
    expect(fetch).toHaveBeenNthCalledWith(2, '/payments/confirm', expect.objectContaining({ method: 'POST', body: JSON.stringify({ payment_id: 'course-1-test' }), credentials: 'include' }))
  })
})
