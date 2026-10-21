<script>
import { computed, ref } from 'vue'

export default {
  props: {
    pricePerNight: { type: Number, required: true },
    rating: { type: [String, Number], default: null },
    reviewCount: { type: Number, default: 0 },
    maxGuests: { type: Number, default: 8 },
    disabled: { type: Boolean, default: false },
  },
  emits: ['reserve'],
  setup(props, { emit }) {
    const checkIn = ref('')
    const checkOut = ref('')
    const guests = ref(1)
    const nights = computed(() => {
      if (!checkIn.value || !checkOut.value) return 0
      return Math.max(0, Math.round((new Date(checkOut.value) - new Date(checkIn.value)) / 86400000))
    })
    const total = computed(() => props.pricePerNight * nights.value)
    function reserve() {
      emit('reserve', { checkIn: checkIn.value, checkOut: checkOut.value, guests: Number(guests.value), nights: nights.value, total: total.value })
    }
    return { checkIn, checkOut, guests, nights, total, reserve }
  },
}
</script>

<template>
  <aside class="stay-booking" aria-label="예약 정보">
    <div class="stay-booking__heading"><p><strong>₩{{ Number(pricePerNight).toLocaleString('ko-KR') }}</strong> / 박</p><span v-if="rating">★ {{ rating }} <span class="stay-booking__reviews">({{ Number(reviewCount).toLocaleString('ko-KR') }})</span></span></div>
    <div class="stay-booking__dates">
      <label><span>체크인</span><input v-model="checkIn" type="date" aria-label="예약 체크인"></label>
      <label><span>체크아웃</span><input v-model="checkOut" type="date" aria-label="예약 체크아웃"></label>
      <label class="stay-booking__guest"><span>인원</span><select v-model.number="guests" aria-label="예약 인원"><option v-for="count in maxGuests" :key="count" :value="count">게스트 {{ count }}명</option></select></label>
    </div>
    <button class="stay-booking__reserve" type="button" :disabled="disabled || nights < 1" @click="reserve">예약하기</button>
    <p class="stay-booking__notice">예약 요청 전에는 요금이 청구되지 않습니다.</p>
    <div v-if="nights" class="stay-booking__total"><span>₩{{ Number(pricePerNight).toLocaleString('ko-KR') }} × {{ nights }}박</span><strong>₩{{ total.toLocaleString('ko-KR') }}</strong></div>
  </aside>
</template>

<style scoped>
.stay-booking{position:sticky;top:24px;padding:23px;border:1px solid #ddd;border-radius:13px;background:#fff;box-shadow:0 5px 18px #00000012;color:#222}.stay-booking__heading{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:17px;font-size:12px}.stay-booking__heading p{margin:0}.stay-booking__heading strong{font-size:20px}.stay-booking__reviews{color:#717171}.stay-booking__dates{display:grid;grid-template-columns:1fr 1fr;overflow:hidden;border:1px solid #aaa;border-radius:9px}.stay-booking__dates label{display:grid;gap:5px;padding:10px;border-bottom:1px solid #ddd}.stay-booking__dates label:nth-child(odd){border-right:1px solid #ddd}.stay-booking__dates label span{font-size:9px;font-weight:750;text-transform:uppercase}.stay-booking__dates input,.stay-booking__dates select{width:100%;min-width:0;border:0;background:transparent;color:#444;font:inherit;font-size:11px}.stay-booking__guest{grid-column:1/-1;border-right:0!important}.stay-booking__reserve{width:100%;margin-top:15px;padding:13px;border:0;border-radius:8px;background:#FAED7D;color:#222;font-size:14px;font-weight:700;cursor:pointer}.stay-booking__reserve:hover:not(:disabled){background:#f4e45b}.stay-booking__reserve:disabled{cursor:not-allowed;opacity:.52}.stay-booking__notice{text-align:center;color:#717171;font-size:11px}.stay-booking__total{display:flex;justify-content:space-between;gap:10px;margin-top:16px;padding-top:15px;border-top:1px solid #eee;font-size:12px}
</style>
