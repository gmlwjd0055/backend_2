import { ref } from 'vue'

export function createSessionStore() {
  return {
    user: ref(null),
    busy: ref(false),
    error: ref(''),
    message: ref(''),
    paymentBusy: ref(false),
  }
}
