<script>
export default {
  props: {
    listing: { type: Object, required: true },
    currency: { type: String, default: '₩' },
  },
  emits: ['select', 'favorite'],
  setup(props) {
    function money(value) {
      return `${props.currency}${Number(value || 0).toLocaleString('ko-KR')}`
    }
    return { money }
  },
}
</script>

<template>
  <article class="stay-card">
    <button class="stay-card__photo" type="button" :aria-label="`${listing.title} 상세 보기`" @click="emit('select', listing)">
      <img :src="listing.image || listing.thumbnail_url" :alt="listing.imageAlt || listing.title" loading="lazy">
      <span v-if="listing.badge" class="stay-card__badge">{{ listing.badge }}</span>
    </button>
    <button class="stay-card__favorite" type="button" :aria-label="listing.favorite ? '위시리스트에서 삭제' : '위시리스트에 추가'" :aria-pressed="Boolean(listing.favorite)" @click="emit('favorite', listing)">{{ listing.favorite ? '♥' : '♡' }}</button>
    <button class="stay-card__body" type="button" @click="emit('select', listing)">
      <span class="stay-card__title">{{ listing.title }}</span>
      <span class="stay-card__rating"><span aria-hidden="true">★</span> {{ listing.rating || '신규' }}</span>
      <span class="stay-card__muted">{{ listing.location }}</span>
      <span class="stay-card__muted">{{ listing.dates }}</span>
      <span class="stay-card__price"><strong>{{ money(listing.pricePerNight ?? listing.price_krw) }}</strong> / 박</span>
    </button>
  </article>
</template>

<style scoped>
.stay-card{position:relative;min-width:0;color:#222}.stay-card__photo{position:relative;display:block;width:100%;aspect-ratio:1/1;border:0;border-radius:13px;overflow:hidden;background:#f4f1e8;cursor:pointer}.stay-card__photo img{width:100%;height:100%;object-fit:cover;transition:transform .25s}.stay-card__photo:hover img{transform:scale(1.025)}.stay-card__badge{position:absolute;top:12px;left:12px;padding:7px 10px;border-radius:20px;background:#fff;font-size:10px;font-weight:700}.stay-card__favorite{position:absolute;top:12px;right:12px;display:grid;place-items:center;width:34px;height:34px;border:0;background:transparent;color:#fff;text-shadow:0 1px 5px #0009;font-size:26px;cursor:pointer}.stay-card__favorite[aria-pressed=true]{color:#FAED7D;text-shadow:0 1px 3px #0008}.stay-card__body{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:5px 8px;width:100%;padding:10px 0 0;border:0;background:none;text-align:left;color:inherit;cursor:pointer}.stay-card__title{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:13px;font-weight:650}.stay-card__rating{font-size:12px;white-space:nowrap}.stay-card__rating span{color:#222}.stay-card__muted{grid-column:1/-1;color:#717171;font-size:12px}.stay-card__price{grid-column:1/-1;margin-top:4px;font-size:12px}.stay-card__price strong{font-size:13px}
</style>
