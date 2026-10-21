<script>
export default {
  props: {
    categories: { type: Array, default: () => [] },
    modelValue: { type: String, default: '' },
  },
  emits: ['update:modelValue', 'filter'],
  setup(props, { emit }) {
    return { emit }
  },
}
</script>

<template>
  <nav class="stay-categories" aria-label="숙소 유형">
    <div class="stay-categories__items">
      <button v-for="category in categories" :key="category.id || category.label" type="button" class="stay-categories__item" :class="{ 'stay-categories__item--active': modelValue === (category.id || category.label) }" @click="emit('update:modelValue', category.id || category.label)">
        <span class="stay-categories__icon" aria-hidden="true">{{ category.icon || '⌂' }}</span>
        <span>{{ category.label }}</span>
      </button>
    </div>
    <button class="stay-categories__filter" type="button" @click="emit('filter')"><span aria-hidden="true">☷</span> 필터</button>
  </nav>
</template>

<style scoped>
.stay-categories{display:flex;align-items:center;gap:14px;min-width:0;border-bottom:1px solid #eee;padding:8px 0 14px;color:#222}.stay-categories__items{display:flex;flex:1;gap:28px;overflow-x:auto;scrollbar-width:none}.stay-categories__items::-webkit-scrollbar{display:none}.stay-categories__item{position:relative;display:grid;flex:0 0 auto;justify-items:center;gap:8px;min-width:56px;padding:3px 2px 9px;border:0;background:none;color:#717171;font-size:11px;font-weight:600;line-height:1.2;cursor:pointer}.stay-categories__item:hover,.stay-categories__item--active{color:#222}.stay-categories__item--active:after{position:absolute;right:0;bottom:-15px;left:0;height:2px;background:#FAED7D;content:""}.stay-categories__icon{font-size:22px;line-height:1}.stay-categories__filter{display:flex;align-items:center;gap:8px;flex:0 0 auto;padding:10px 14px;border:1px solid #ddd;border-radius:10px;background:#fff;font-size:12px;font-weight:600;cursor:pointer}.stay-categories__filter:hover{border-color:#222}
@media(max-width:600px){.stay-categories{gap:10px}.stay-categories__items{gap:19px}.stay-categories__filter{padding:9px 10px}}
</style>
