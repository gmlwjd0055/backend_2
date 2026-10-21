export function authorizeKakao(sdk, jsKey, redirectUri, state) {
  if (!sdk) throw new Error('카카오 JavaScript SDK를 불러오지 못했습니다.')
  if (!jsKey) throw new Error('카카오 로그인을 설정하지 않았습니다.')
  if (!sdk.isInitialized()) sdk.init(jsKey)

  sdk.Auth.authorize({
    redirectUri,
    scope: 'profile_nickname',
    state,
  })
}
