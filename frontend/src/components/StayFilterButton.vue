<script setup>
defineProps({ activeCount: { type: Number, default: 0 } })
const emit = defineEmits(['click'])
</script>

<template>
  <button class="stay-filter" type="button" @click="emit('click')"><span aria-hidden="true">☷</span> 필터 <span v-if="activeCount" class="stay-filter__count">{{ activeCount }}</span></button>
</template>

<style scoped>
.stay-filter{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border:1px solid #ddd;border-radius:10px;background:#fff;color:#222;font-size:12px;font-weight:600;cursor:pointer}.stay-filter:hover{border-color:#222}.stay-filter__count{display:grid;place-items:center;min-width:18px;height:18px;padding:0 4px;border-radius:9px;background:#FAED7D;font-size:10px}
</style>
