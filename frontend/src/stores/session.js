import { ref } from 'vue'

export function createSessionStore() {
  const user = ref(null)

  return {
    user,
    busy: ref(false),
    error: ref(''),
    message: ref(''),
    paymentBusy: ref(false),
    clearSession() {
      user.value = null
    },
  }
}
