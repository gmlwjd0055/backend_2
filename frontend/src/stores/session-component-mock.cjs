const { ref } = require('vue')

module.exports = {
  createSessionStore: () => ({
    user: ref(null),
    busy: ref(false),
    error: ref(''),
    message: ref(''),
    paymentBusy: ref(false),
  }),
}
