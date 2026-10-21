const { ref } = require('vue')

module.exports = {
  createSessionStore: () => {
    const user = ref(null)
    return {
      user,
      busy: ref(false),
      error: ref(''),
      message: ref(''),
      paymentBusy: ref(false),
      clearSession: () => { user.value = null },
    }
  },
}
