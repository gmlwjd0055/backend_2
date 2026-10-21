<script>
export default {
  props: { images: { type: Array, default: () => [] }, title: { type: String, default: '숙소' } },
  emits: ['view-all'],
  setup(props, { emit }) {
    return { emit }
  },
}
</script>

<template>
  <section class="stay-gallery" :aria-label="`${title} 사진`">
    <button v-for="(image, index) in images.slice(0, 5)" :key="image.src || image" class="stay-gallery__tile" :class="{ 'stay-gallery__tile--main': index === 0 }" type="button" @click="emit('view-all', index)">
      <img :src="image.src || image" :alt="image.alt || `${title} 사진 ${index + 1}`" :loading="index === 0 ? 'eager' : 'lazy'">
    </button>
    <button v-if="images.length" class="stay-gallery__all" type="button" @click="emit('view-all', 0)"><span aria-hidden="true">▦</span> 사진 모두 보기</button>
    <div v-if="!images.length" class="stay-gallery__empty">사진을 준비 중입니다.</div>
  </section>
</template>

<style scoped>
.stay-gallery{position:relative;display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:repeat(2,minmax(130px,1fr));gap:8px;min-height:340px;overflow:hidden;border-radius:14px}.stay-gallery__tile{min-width:0;min-height:0;padding:0;border:0;background:#f3f1e8;cursor:pointer}.stay-gallery__tile--main{grid-row:1/3;grid-column:1}.stay-gallery__tile img{display:block;width:100%;height:100%;object-fit:cover;transition:filter .18s}.stay-gallery__tile:hover img{filter:brightness(.93)}.stay-gallery__all{position:absolute;right:18px;bottom:18px;padding:9px 13px;border:1px solid #222;border-radius:8px;background:#fff;color:#222;font-size:12px;font-weight:650;cursor:pointer}.stay-gallery__all:hover{background:#FAED7D}.stay-gallery__empty{display:grid;grid-column:1/-1;place-items:center;background:#f4f1e8;color:#717171;font-size:13px}
@media(max-width:650px){.stay-gallery{grid-template-columns:1fr 1fr;grid-template-rows:250px 110px;gap:4px;margin:0 -16px;border-radius:0}.stay-gallery__tile--main{grid-column:1/3;grid-row:1}.stay-gallery__tile:nth-child(n+4){display:none}.stay-gallery__all{right:14px;bottom:12px;padding:8px 10px;font-size:11px}}
</style>
