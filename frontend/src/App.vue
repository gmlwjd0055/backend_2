<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { createBoard, getBoard, getBoards, logIn, signUp } from './api'

const route = ref(readRoute())
const boards = ref([])
const selected = ref(null)
const loading = ref(false)
const busy = ref(false)
const message = ref('')
const error = ref('')
const search = ref('')
const user = ref(null)
const account = reactive({ email: '', password: '', name: '' })
const post = reactive({ title: '', contents: '' })
const filteredBoards = computed(() => boards.value.filter((board) => `${board.title} ${board.contents}`.toLocaleLowerCase().includes(search.value.toLocaleLowerCase())))
const isAuth = computed(() => route.value.name === 'login' || route.value.name === 'signup')

function readRoute() {
  const path = window.location.pathname.replace(/\/$/, '') || '/'
  if (path === '/signup') return { name: 'signup' }
  if (path === '/login') return { name: 'login' }
  if (path === '/write') return { name: 'write' }
  const match = path.match(/^\/board\/(\d+)$/)
  if (match) return { name: 'detail', id: Number(match[1]) }
  return { name: 'list' }
}
function go(path) {
  if (`${window.location.pathname}${window.location.search}` !== path) window.history.pushState({}, '', path)
  route.value = readRoute()
  error.value = ''
  message.value = ''
  window.scrollTo({ top: 0, behavior: 'smooth' })
  loadRoute()
}
function onPopState() { route.value = readRoute(); error.value = ''; loadRoute() }
async function loadRoute() {
  if (route.value.name === 'list') {
    loading.value = true
    try { boards.value = await getBoards() || [] } catch (err) { error.value = err.message }
    finally { loading.value = false }
  } else if (route.value.name === 'detail') {
    selected.value = null
    loading.value = true
    try { selected.value = await getBoard(route.value.id) } catch (err) { error.value = err.message }
    finally { loading.value = false }
  }
}
async function submitAccount() {
  error.value = ''; busy.value = true
  try {
    if (route.value.name === 'signup') {
      await signUp({ email: account.email.trim(), password: account.password, name: account.name.trim() })
      account.password = ''
      go('/login')
      message.value = '가입이 완료됐어요. 로그인해 주세요.'
    } else {
      const result = await logIn({ email: account.email.trim(), password: account.password })
      user.value = { email: result.email, name: account.name || result.email.split('@')[0] }
      account.password = ''
      go('/')
      message.value = `${user.value.name}님, 반가워요.`
    }
  } catch (err) { error.value = err.message }
  finally { busy.value = false }
}
async function publish() {
  if (!post.title.trim() || !post.contents.trim()) return
  error.value = ''; busy.value = true
  try {
    const created = await createBoard({ title: post.title.trim(), contents: post.contents.trim() })
    post.title = ''; post.contents = ''
    go(`/board/${created.idx}`)
    message.value = '게시글을 작성했어요.'
  } catch (err) { error.value = err.message }
  finally { busy.value = false }
}
function dateFor(idx) { return `기록 ${String(idx).padStart(2, '0')}` }
function excerpt(text) { return (text || '').replace(/\s+/g, ' ').trim() }
onMounted(() => { window.addEventListener('popstate', onPopState); loadRoute() })
onUnmounted(() => window.removeEventListener('popstate', onPopState))
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <button class="brand" aria-label="모아 홈" @click="go('/')"><span class="brand-mark">m</span><span>moa<span class="brand-dot">.</span></span></button>
      <nav class="nav-links" aria-label="주요 메뉴"><button :class="{ 'nav-active': route.name === 'list' }" @click="go('/')">둘러보기</button><span class="nav-divider"></span><span class="nav-caption">생각을 모으는 작은 공간</span></nav>
      <div class="top-actions"><span v-if="user" class="user-pill"><span class="avatar">{{ user.name.slice(0, 1) }}</span>{{ user.name }}</span><template v-else><button class="login-link" @click="go('/login')">로그인</button><button class="join-button" @click="go('/signup')">함께하기 <span>↗</span></button></template></div>
    </header>

    <main>
      <Transition name="page" mode="out-in">
        <section v-if="isAuth" :key="route.name" class="auth-page">
          <div class="auth-art" aria-hidden="true"><span class="auth-orbit"></span><span class="auth-sun"></span><div class="auth-paper"><span>MOA NOTE</span><i></i><i></i><i></i><b>✳</b></div><p>오늘의 생각도<br />천천히, 오래.</p></div>
          <div class="auth-panel"><button class="back-link" @click="go('/')">← 둘러보기</button><div class="eyebrow"><span class="eyebrow-line"></span>{{ route.name === 'login' ? 'WELCOME BACK' : 'JOIN THE NOTEBOOK' }}</div><h1>{{ route.name === 'login' ? '다시 만나 반가워요.' : '함께 기록해요.' }}</h1><p class="page-intro">{{ route.name === 'login' ? '로그인하고 이어서 기록해 보세요.' : '마음에 담아둔 이야기를 모아보세요.' }}</p>
            <div v-if="message" class="notice" role="status">{{ message }}</div><div v-if="error" class="error-box" role="alert">{{ error }}</div>
            <form class="form-stack" @submit.prevent="submitAccount"><label>이메일<input v-model="account.email" type="email" autocomplete="email" required placeholder="you@example.com" /></label><label v-if="route.name === 'signup'">이름<input v-model="account.name" autocomplete="name" required placeholder="어떻게 불러드릴까요?" /></label><label>비밀번호<input v-model="account.password" type="password" :autocomplete="route.name === 'login' ? 'current-password' : 'new-password'" required minlength="4" placeholder="비밀번호" /></label><button class="submit-button" :disabled="busy">{{ busy ? '잠시만요…' : route.name === 'login' ? '로그인' : '회원가입' }} <span>↗</span></button></form>
            <p class="auth-switch">{{ route.name === 'login' ? '아직 계정이 없나요?' : '이미 계정이 있나요?' }} <button @click="go(route.name === 'login' ? '/signup' : '/login')">{{ route.name === 'login' ? '회원가입' : '로그인' }}</button></p>
          </div>
        </section>

        <section v-else-if="route.name === 'write'" key="write" class="editor-page"><button class="back-link" @click="go('/')">← 모든 게시글</button><div class="editor-heading"><div class="eyebrow"><span class="eyebrow-line"></span> A NEW PAGE</div><h1>무슨 생각을 하고 있나요?</h1><p class="page-intro">떠오른 이야기를 편하게 적어주세요.</p></div><div v-if="error" class="error-box" role="alert">{{ error }}</div><form class="editor-form" @submit.prevent="publish"><label>제목<input v-model="post.title" maxlength="100" required placeholder="오늘의 한 줄" /></label><label>내용<textarea v-model="post.contents" required rows="10" placeholder="마음에 담아둔 이야기를 써보세요…"></textarea></label><div class="editor-actions"><span>작은 생각도 오래 남도록.</span><button class="submit-button" :disabled="busy">{{ busy ? '저장 중…' : '게시글 올리기' }} <span>↗</span></button></div></form></section>

        <section v-else-if="route.name === 'detail'" key="detail" class="detail-wrap"><button class="back-link" @click="go('/')">← 모든 게시글</button><div v-if="error" class="error-box" role="alert">{{ error }} <button @click="loadRoute">다시 시도</button></div><article v-else-if="loading" class="detail-card skeleton" aria-label="게시글 불러오는 중"><i class="sk-line sk-short"></i><i class="sk-line sk-title"></i><i class="sk-line"></i><i class="sk-line"></i><i class="sk-line sk-medium"></i></article><article v-else-if="selected" class="detail-card"><div class="eyebrow"><span class="eyebrow-line"></span>{{ dateFor(selected.idx) }}</div><h1>{{ selected.title }}</h1><div class="detail-rule"></div><p>{{ selected.contents }}</p><div class="detail-end">✳</div></article></section>

        <div v-else key="list" class="list-page"><section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="eyebrow-line"></span> A PLACE FOR YOUR THOUGHTS</div><h1>오늘의 생각을<br /><span>가볍게 남겨요.</span></h1><p>크고 작은 이야기들이 모여<br class="mobile-break" /> 나만의 페이지가 됩니다.</p><button class="hero-cta" @click="go('/write')">나의 이야기 남기기 <span>↗</span></button></div><div class="hero-art" aria-hidden="true"><div class="sun"></div><div class="art-label">NO. 01<br />DAILY NOTE</div><div class="paper paper-back"></div><div class="paper paper-front"><div class="paper-date">A NOTE TO SELF</div><div class="paper-lines"><i></i><i></i><i></i></div><div class="paper-flower">✳</div></div><span class="art-spark spark-one">✳</span><span class="art-spark spark-two">✳</span><span class="art-orbit"></span></div><div class="hero-bottom"><span><b>01</b> &nbsp; 기록은 언제나 환영이에요</span><span>SCROLL TO EXPLORE <b>↓</b></span></div></section>
          <section class="notes-section"><div class="section-head"><div><div class="eyebrow"><span class="eyebrow-line"></span> THE NOTEBOOK</div><h2>최근 기록 <span class="count">{{ String(boards.length).padStart(2, '0') }}</span></h2></div><div class="section-tools"><label class="search-box"><span aria-hidden="true">⌕</span><input v-model="search" aria-label="기록 검색" placeholder="어떤 이야기를 찾나요?" /></label><button class="write-button" @click="go('/write')"><span>＋</span> 기록 남기기</button></div></div><div v-if="message" class="notice" role="status">{{ message }}</div><div v-if="error" class="error-box" role="alert">{{ error }} <button @click="loadRoute">다시 시도</button></div><div v-else-if="loading" class="notes-grid" aria-label="게시글 불러오는 중"><div v-for="n in 6" :key="n" class="note-card skeleton" aria-hidden="true"><i class="sk-line sk-short"></i><i class="sk-line sk-title"></i><i class="sk-line"></i><i class="sk-line sk-medium"></i></div></div><div v-else-if="filteredBoards.length" class="notes-grid"><button v-for="(board, index) in filteredBoards" :key="board.idx" class="note-card" :class="`tone-${index % 4}`" @click="go(`/board/${board.idx}`)"><div class="card-meta"><span class="note-index">{{ dateFor(board.idx) }}</span><span class="card-arrow">↗</span></div><h3>{{ board.title }}</h3><p>{{ excerpt(board.contents) }}</p><div class="card-bottom"><span>기록 읽기</span><span class="read-arrow">→</span></div></button></div><div v-else class="empty-state"><span class="empty-symbol">✳</span><h3>{{ search ? '검색 결과가 없어요' : '아직 첫 기록이 없어요' }}</h3><p>{{ search ? '다른 단어로 다시 찾아보세요.' : '먼저 작은 생각 하나를 남겨볼까요?' }}</p><button v-if="!search" class="text-action" @click="go('/write')">첫 기록 쓰기 <span>↗</span></button></div><div class="list-footer"><span>작은 생각도 오래 남도록.</span><span>MOA NOTEBOOK · 2026</span></div></section>
        </div>
      </Transition>
    </main>
    <footer class="site-footer"><span class="footer-brand">moa<span>.</span></span><span>생각을 모으는 작은 공간</span><span>MADE FOR SLOW MOMENTS&nbsp; ✳</span></footer>
  </div>
</template>
