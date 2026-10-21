<script>
import {computed, onMounted, onUnmounted, reactive, ref, watch} from 'vue'
import {getCourse, getCourses, getCurrentUser, kakaoLogin, logIn, logout, signUp, createPaymentOrder, confirmPayment} from '../api'
import {authorizeKakao} from '../api/kakao'
import {resolveRoute} from '../router/index.js'
import {createSessionStore} from '../stores/session.js'

export default {
  setup() {
    const route = ref(resolveRoute()), courses = ref([]), selected = ref(null), loading = ref(false), kakaoBusy = ref(false),
        search = ref(''), activeCategory = ref('전체')
    const {user, busy, error, message, paymentBusy, clearSession} = createSessionStore()
    const account = reactive({email: '', password: '', name: ''})

    const routeName = computed(() => route.value?.name || 'list');
    const isAuth = computed(() => ['login', 'signup'].includes(routeName.value));
    const categories = computed(() => ['전체', ...new Set(courses.value.map(c => c.category).filter(Boolean))]);
    const filteredCourses = ref([])

    function applyCourseFilters() {
      const q = search.value.trim().toLocaleLowerCase();
      filteredCourses.value = courses.value.filter(c => (!q || `${c.title} ${c.summary} ${c.category}`.toLocaleLowerCase().includes(q)) && (activeCategory.value === '전체' || c.category === activeCategory.value))
    }

    watch([courses, search, activeCategory], applyCourseFilters, {immediate: true})

    function formatPrice(v) {
      return `${Number(v || 0).toLocaleString('ko-KR')}원`
    }

    function go(path) {
      if (window.location.pathname !== path) window.history.pushState({}, '', path);
      route.value = resolveRoute();
      error.value = '';
      message.value = '';
      loadRoute()
    }

    async function loadRoute() {
      if (route.value.name === 'kakaoCallback') return finishKakaoLogin();
      loading.value = true;
      error.value = '';
      try {
        if (route.value.name === 'list') courses.value = await getCourses() || [];
        if (route.value.name === 'detail') selected.value = await getCourse(route.value.id)
      } catch (e) {
        error.value = e.message;
        if (route.value.name === 'detail') selected.value = null
      } finally {
        loading.value = false
      }
    }

    function onPopState() {
      route.value = resolveRoute();
      loadRoute()
    }

    function retry() {
      loadRoute()
    }

    async function restoreSession() {
      if (route.value.name === 'kakaoCallback') return
      try {
        const currentUser = await getCurrentUser()
        user.value = currentUser?.name ? {name: currentUser.name} : null
      } catch {
        user.value = null
      }
    }

    function loginWithKakao() {
      try {
        const state = window.crypto.randomUUID();
        window.sessionStorage.setItem('kakao_login_state', state);
        authorizeKakao(window.Kakao, window.__KAKAO_JS_KEY__ || '', `${window.location.origin}/login/kakao/callback`, state)
      } catch (e) {
        error.value = e.message
      }
    }

    async function finishKakaoLogin() {
      const p = new URLSearchParams(window.location.search),
          expected = window.sessionStorage.getItem('kakao_login_state');
      window.sessionStorage.removeItem('kakao_login_state');
      kakaoBusy.value = true;
      try {
        if (p.has('error') || !p.get('code') || !expected || p.get('state') !== expected) throw new Error('카카오 로그인을 확인할 수 없습니다. 다시 시도해 주세요.');
        const r = await kakaoLogin(p.get('code'));
        user.value = {name: r.nickname};
        window.history.replaceState({}, '', '/');
        route.value = resolveRoute();
        await loadRoute()
      } catch (e) {
        window.history.replaceState({}, '', '/login');
        route.value = resolveRoute();
        error.value = e.message
      } finally {
        kakaoBusy.value = false
      }
    }

    async function submitAccount() {
      busy.value = true;
      error.value = '';
      try {
        if (route.value.name === 'signup') {
          await signUp({email: account.email.trim(), password: account.password, name: account.name.trim()});
          go('/login');
          message.value = '가입이 완료됐어요. 로그인해 주세요.'
        } else {
          const r = await logIn({email: account.email.trim(), password: account.password});
          user.value = {name: r.email};
          go('/')
        }
      } catch (e) {
        error.value = e.message
      } finally {
        busy.value = false
      }
    }

    async function logoutUser() {
      error.value = ''
      try {
        await logout()
      } catch (e) {
        // The local session is cleared even when the server is unavailable.
        // This prevents the UI from retaining an authenticated state.
        error.value = e.message
      } finally {
        clearSession()
        go('/')
      }
    }

    async function purchaseCourse() {
      if (!user.value) {
        try {
          const currentUser = await getCurrentUser()
          if (currentUser?.name) user.value = {name: currentUser.name}
        } catch {
          user.value = null
        }
      }
      if (!user.value) {
        go('/login');
        message.value = '로그인 후 강의를 구매할 수 있어요.';
        return
      }
      if (!window.PortOne?.requestPayment) {
        error.value = '결제 모듈을 불러오지 못했습니다. 새로고침 후 다시 시도해 주세요.';
        return
      }
      paymentBusy.value = true;
      error.value = '';
      message.value = '';
      try {
        const order = await createPaymentOrder(selected.value.id);
        const result = await window.PortOne.requestPayment({
          storeId: order.store_id,
          channelKey: order.channel_key,
          paymentId: order.payment_id,
          orderName: order.order_name,
          totalAmount: order.amount_krw,
          currency: 'KRW',
          payMethod: 'CARD',
          redirectUrl: window.location.href
        });
        if (result?.code) throw new Error(result.message || '결제가 취소되었거나 실패했습니다.');
        await confirmPayment(order.payment_id);
        message.value = '강의 구매가 완료됐어요.'
      } catch (e) {
        error.value = e.message || '결제 처리 중 오류가 발생했습니다.'
      } finally {
        paymentBusy.value = false
      }
    }

    async function finishRedirectPayment() {
      // OAuth authorization codes also use the `code` query parameter.
      if (route.value.name === 'kakaoCallback') return;
      const params = new URLSearchParams(window.location.search), paymentId = params.get('paymentId'),
          code = params.get('code'), detail = params.get('message');
      if (!paymentId && !code) return;
      window.history.replaceState({}, '', window.location.pathname);
      if (code) {
        error.value = detail || '결제가 취소되었거나 실패했습니다.';
        return
      }
      paymentBusy.value = true;
      try {
        await confirmPayment(paymentId);
        message.value = '강의 구매가 완료됐어요.'
      } catch (e) {
        error.value = e.message || '결제 확인 중 오류가 발생했습니다.'
      } finally {
        paymentBusy.value = false
      }
    }

    onMounted(() => {
      window.addEventListener('popstate', onPopState);
      finishRedirectPayment();
      restoreSession();
      loadRoute()
    });
    onUnmounted(() => window.removeEventListener('popstate', onPopState))
    return {
      route,
      courses,
      selected,
      loading,
      error,
      search,
      activeCategory,
      user,
      busy,
      paymentBusy,
      kakaoBusy,
      message,
      account,
      routeName,
      isAuth,
      categories,
      filteredCourses,
      formatPrice,
      go,
      loadRoute,
      retry,
      loginWithKakao,
      submitAccount,
      logoutUser,
      purchaseCourse
    }
  }
}
</script>
<template>
  <div class="app-shell">
    <header class="topbar">
      <button class="brand" aria-label="모아 홈" @click="go('/')"><span class="brand-mark">m</span> moa<span
          class="brand-dot">.</span></button>
      <nav>
        <button @click="go('/')">강의 둘러보기</button>
      </nav>
      <div class="top-actions"><template v-if="user"><span>{{ user.name }}</span><button @click="logoutUser">로그아웃</button></template>
        <template v-else>
          <button @click="go('/login')">로그인</button>
          <button class="join-button" @click="go('/signup')">회원가입</button>
        </template>
      </div>
    </header>
    <main>
      <section v-if="routeName==='kakaoCallback'" class="auth-page" aria-live="polite">
        <div class="auth-panel">
          <div v-if="kakaoBusy" class="loading" role="status">카카오 로그인 확인 중…</div>
        </div>
      </section>
      <section v-else-if="isAuth" class="auth-page">
        <div class="auth-panel">
          <button class="back-link" @click="go('/')">← 강의 둘러보기</button>
          <h1>{{ routeName === 'login' ? '다시 만나 반가워요.' : '회원가입' }}</h1>
          <div v-if="error" class="error-box" role="alert">{{ error }}</div>
          <form @submit.prevent="submitAccount"><label>이메일<input v-model="account.email" type="email"
                                                                 required></label><label
              v-if="routeName==='signup'">이름<input v-model="account.name" required></label><label>비밀번호<input
              v-model="account.password" type="password" required minlength="4"></label>
            <button class="submit-button" :disabled="busy">
              {{ busy ? '처리 중…' : routeName === 'login' ? '로그인' : '회원가입' }}
            </button>
          </form>
          <button v-if="routeName==='login'" class="kakao-login-button" @click="loginWithKakao">카카오로 로그인</button>
          <p>{{ routeName === 'login' ? '아직 계정이 없나요?' : '이미 계정이 있나요?' }}
            <button @click="go(routeName==='login'?'/signup':'/login')">{{ routeName === 'login' ? '회원가입' : '로그인' }}
            </button>
          </p>
        </div>
      </section>
      <section v-else-if="routeName==='detail'" class="detail-wrap">
        <button class="back-link" @click="go('/')">← 강의 목록</button>
        <div v-if="loading" class="loading">강의를 불러오는 중…</div>
        <div v-else-if="error" class="error-box" role="alert">{{ error }}
          <button @click="retry">다시 시도</button>
        </div>
        <article v-else-if="selected" class="detail-card">
          <div class="course-category">{{ selected.category }}</div>
          <h1>{{ selected.title }}</h1>
          <p class="course-summary">{{ selected.summary }}</p>
          <p class="course-description">{{ selected.description }}</p>
          <div class="course-meta"><span>강사 {{ selected.instructor_name }}</span><span>{{ selected.level }}</span><span>{{ selected.duration_minutes }}분</span><strong>{{ formatPrice(selected.price_krw) }}</strong>
          </div>
          <div v-if="error" class="error-box" role="alert">{{ error }}</div>
          <p v-if="message" class="purchase-message" role="status">{{ message }}</p>
          <button class="submit-button purchase-button" :disabled="paymentBusy" @click="purchaseCourse">
            {{ paymentBusy ? '결제 처리 중…' : `구매하기 · ${formatPrice(selected.price_krw)}` }}
          </button>
        </article>
      </section>
      <section v-else class="catalog">
        <div class="hero"><p>LEARN AT YOUR OWN PACE</p>
          <h1>성장을 시작하는<br><span>실전 강의</span></h1>
          <p>필요한 기술을 골라 차근차근 배워보세요.</p></div>
        <div class="catalog-toolbar">
          <div class="categories">
            <button v-for="c in categories" :key="c" :class="{selected:activeCategory===c}" @click="activeCategory=c">
              {{ c }}
            </button>
          </div>
          <input v-model="search" aria-label="강의 검색" placeholder="강의 제목이나 분야 검색"></div>
        <div v-if="error" class="error-box" role="alert">{{ error }}
          <button @click="retry">다시 시도</button>
        </div>
        <div v-else-if="loading" class="loading">강의를 불러오는 중…</div>
        <div v-else-if="filteredCourses.length" class="course-grid">
          <button v-for="course in filteredCourses" :key="course.id" class="course-card"
                  @click="go(`/courses/${course.id}`)">
            <div class="thumbnail"><img v-if="course.thumbnail_url && !course.imageError" :src="course.thumbnail_url"
                                        :alt="course.title" @error="course.imageError=true"><span v-else>✦</span></div>
            <div class="course-category">{{ course.category }}</div>
            <h2>{{ course.title }}</h2>
            <p>{{ course.summary }}</p>
            <div class="course-card-bottom">
              <span>{{ course.instructor_name }} · {{ course.level }}</span><strong>{{ formatPrice(course.price_krw) }}</strong>
            </div>
          </button>
        </div>
        <div v-else class="empty-state"><h2>강의가 없어요</h2>
          <p>검색어나 카테고리를 바꿔보세요.</p></div>
      </section>
    </main>
  </div>
</template>
