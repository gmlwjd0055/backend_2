import { authorizeKakao } from './kakao.js'
import { jest } from '@jest/globals'

describe('Kakao JavaScript SDK authorization', () => {
  it('requests nickname consent and returns to the configured callback', () => {
    const sdk = {
      isInitialized: jest.fn(() => true),
      init: jest.fn(),
      Auth: { authorize: jest.fn() },
    }

    authorizeKakao(sdk, 'javascript-key', 'http://localhost:5173/login/kakao/callback', 'csrf-state')

    expect(sdk.Auth.authorize).toHaveBeenCalledWith({
      redirectUri: 'http://localhost:5173/login/kakao/callback',
      scope: 'profile_nickname',
      state: 'csrf-state',
    })
  })

  it('initializes the SDK before starting authorization', () => {
    const sdk = {
      isInitialized: jest.fn(() => false),
      init: jest.fn(),
      Auth: { authorize: jest.fn() },
    }

    authorizeKakao(sdk, 'javascript-key', 'http://localhost:5173/login/kakao/callback', 'csrf-state')

    expect(sdk.init).toHaveBeenCalledWith('javascript-key')
    expect(sdk.Auth.authorize).toHaveBeenCalled()
  })
})
