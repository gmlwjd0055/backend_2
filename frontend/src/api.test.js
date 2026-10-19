import { createBoard, getBoards } from './api'
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
})
