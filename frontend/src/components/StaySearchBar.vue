<script>
import { reactive } from 'vue'

export default {
  props: {
    initial: { type: Object, default: () => ({}) },
    compact: { type: Boolean, default: false },
  },
  emits: ['search'],
  setup(props, { emit }) {
    const criteria = reactive({ destination: '', checkIn: '', checkOut: '', guests: 1, ...props.initial })
    function submitSearch() {
      emit('search', { ...criteria, guests: Number(criteria.guests) })
    }
    return { criteria, submitSearch }
  },
}
</script>

<template>
  <form class="stay-search" :class="{ 'stay-search--compact': compact }" role="search" @submit.prevent="submitSearch">
    <label class="stay-search__field stay-search__destination">
      <span>목적지</span>
      <input v-model="criteria.destination" autocomplete="off" placeholder="어디로 여행가세요?" aria-label="목적지">
    </label>
    <label class="stay-search__field">
      <span>체크인</span>
      <input v-model="criteria.checkIn" type="date" aria-label="체크인 날짜">
    </label>
    <label class="stay-search__field">
      <span>체크아웃</span>
      <input v-model="criteria.checkOut" type="date" aria-label="체크아웃 날짜">
    </label>
    <label class="stay-search__field stay-search__guests">
      <span>여행자</span>
      <select v-model.number="criteria.guests" aria-label="여행자 수">
        <option v-for="count in 8" :key="count" :value="count">게스트 {{ count }}명</option>
      </select>
    </label>
    <button class="stay-search__submit" type="submit" aria-label="숙소 검색"><span aria-hidden="true">⌕</span></button>
  </form>
</template>

<style scoped>
.stay-search{display:grid;grid-template-columns:minmax(150px,1.4fr) repeat(3,minmax(115px,1fr)) 48px;align-items:center;max-width:850px;min-height:66px;margin:20px auto;padding:6px;border:1px solid #ddd;border-radius:36px;background:#fff;box-shadow:0 2px 6px #00000012;color:#222}.stay-search__field{display:grid;gap:4px;min-width:0;padding:8px 16px;border-right:1px solid #eee}.stay-search__field span{font-size:11px;font-weight:700}.stay-search__field input,.stay-search__field select{width:100%;min-width:0;border:0;outline:0;background:transparent;color:#717171;font:inherit;font-size:12px}.stay-search__field input[type=date]{font-size:11px}.stay-search__guests{border:0}.stay-search__submit{display:grid;place-items:center;width:48px;height:48px;border:0;border-radius:50%;background:#FAED7D;color:#222;font-size:25px;cursor:pointer}.stay-search__submit:hover{background:#f4e45b}.stay-search--compact{grid-template-columns:minmax(130px,1.3fr) 1fr 1fr 40px;max-width:520px;min-height:50px;margin:0;padding:4px}.stay-search--compact .stay-search__field{padding:6px 10px}.stay-search--compact .stay-search__guests{display:none}.stay-search--compact .stay-search__submit{width:40px;height:40px}
@media(max-width:680px){.stay-search{grid-template-columns:1fr 1fr 46px;gap:0;margin:14px 0;border-radius:18px}.stay-search__destination{grid-column:1/-1;border-right:0;border-bottom:1px solid #eee}.stay-search__field{padding:8px 10px}.stay-search__field span{font-size:10px}.stay-search__field input,.stay-search__field select{font-size:11px}.stay-search__guests{display:none}.stay-search__submit{width:40px;height:40px;grid-column:3;grid-row:2}.stay-search--compact{grid-template-columns:1fr 1fr 40px}.stay-search--compact .stay-search__destination{grid-column:auto;border:0}.stay-search--compact .stay-search__field:nth-child(2){display:none}.stay-search--compact .stay-search__submit{grid-column:3;grid-row:1}}
</style>
