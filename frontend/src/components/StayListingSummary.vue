<script>
export default {
  props: {
    listing: { type: Object, required: true },
    amenities: { type: Array, default: () => [] },
  },
  emits: ['reviews', 'host'],
}
</script>

<template>
  <section class="stay-summary" aria-labelledby="stay-summary-title">
    <div class="stay-summary__main">
      <div>
        <h1 id="stay-summary-title">{{ listing.title }}</h1>
        <p class="stay-summary__subtitle">{{ listing.subtitle || listing.location }}</p>
        <p class="stay-summary__facts">
          <span v-if="listing.guests">최대 {{ listing.guests }}명</span>
          <span v-if="listing.bedrooms">침실 {{ listing.bedrooms }}개</span>
          <span v-if="listing.beds">침대 {{ listing.beds }}개</span>
          <span v-if="listing.baths">욕실 {{ listing.baths }}개</span>
        </p>
      </div>
      <button v-if="listing.host" class="stay-summary__host" type="button" :aria-label="`${listing.host} 호스트 정보 보기`" @click="$emit('host', listing.host)">
        {{ listing.hostInitial || listing.host.slice(0, 1) }}
      </button>
    </div>
    <button class="stay-summary__rating" type="button" @click="$emit('reviews')">
      <span aria-hidden="true">★</span> {{ listing.rating || '새로운 숙소' }}
      <span v-if="listing.reviewCount" class="stay-summary__reviews">· 후기 {{ listing.reviewCount }}개</span>
    </button>
    <div v-if="listing.highlight" class="stay-summary__highlight">
      <span class="stay-summary__sparkle" aria-hidden="true">✦</span>
      <div><strong>{{ listing.highlight }}</strong><p>{{ listing.highlightDescription }}</p></div>
    </div>
    <ul v-if="amenities.length" class="stay-summary__amenities" aria-label="숙소 편의시설">
      <li v-for="amenity in amenities" :key="amenity.id || amenity.label">
        <span aria-hidden="true">{{ amenity.icon || '✓' }}</span>{{ amenity.label }}
      </li>
    </ul>
  </section>
</template>

<style scoped>
.stay-summary{display:grid;gap:18px;padding:26px 0;border-bottom:1px solid #ddd;color:#222}.stay-summary__main{display:flex;align-items:center;justify-content:space-between;gap:20px}.stay-summary h1{margin:0;font-size:25px;line-height:1.25}.stay-summary__subtitle,.stay-summary__facts{margin:8px 0 0;color:#555;font-size:14px}.stay-summary__facts{display:flex;flex-wrap:wrap;gap:7px}.stay-summary__facts span+span:before{content:'·';margin-right:7px;color:#777}.stay-summary__host{flex:0 0 54px;width:54px;height:54px;border:0;border-radius:50%;background:#FAED7D;font-size:22px;font-weight:700;cursor:pointer}.stay-summary__rating{justify-self:start;padding:0;border:0;background:none;color:#222;font-size:14px;font-weight:700;cursor:pointer}.stay-summary__rating>span:first-child{color:#222}.stay-summary__reviews{font-weight:500;text-decoration:underline}.stay-summary__highlight{display:flex;align-items:center;gap:14px;padding:17px;border:1px solid #eee;border-radius:12px}.stay-summary__sparkle{display:grid;place-items:center;flex:0 0 38px;height:38px;border-radius:50%;background:#FAED7D;font-size:20px}.stay-summary__highlight strong{font-size:14px}.stay-summary__highlight p{margin:4px 0 0;color:#666;font-size:12px}.stay-summary__amenities{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0;padding:0;list-style:none}.stay-summary__amenities li{display:flex;align-items:center;gap:10px;font-size:13px}.stay-summary__amenities li span{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#FAED7D;font-size:15px}
@media(max-width:600px){.stay-summary{gap:15px;padding:20px 0}.stay-summary h1{font-size:21px}.stay-summary__host{flex-basis:46px;width:46px;height:46px}.stay-summary__amenities{grid-template-columns:1fr}}
</style>
