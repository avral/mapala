import App from './App.vue'

import auth from './auth'
import blockchains from './blockchains'

import Vue from 'vue'
import finance from './services/finance/'
import Preico from './preico/PreIco.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import VueCookie from 'vue-cookie'
import VueResource from 'vue-resource'
import VueLazyload from 'vue-lazyload'
import * as VueGoogleMaps from 'vue2-google-maps'
import showdown from 'showdown'
import VueScrollTo from 'vue-scrollto'
import * as localStore from 'store'
import VeeValidate from 'vee-validate'

// animate.css
import 'animate.css/animate.min.css'

import 'font-awesome/css/font-awesome.css'
import VueHighcharts from 'vue-highcharts'
import axios from 'axios'
// import VueAxios from 'vue-axios'
import Vuex from 'vuex'
import { sync } from 'vuex-router-sync'

import store from './store/'
import router from './router/'
import filters from './filters/'

import Meta from 'vue-meta'

Vue.use(ElementUI)
Vue.use(VueCookie)
Vue.use(VueResource)
Vue.use(VueLazyload)
Vue.use(VueHighcharts)
Vue.use(VueScrollTo)
Vue.use(Meta)
Vue.use(VeeValidate)

// Vue.use(VueAxios, axios)
// Vue.use(axios)

Vue.use(VueLazyload, {
  preLoad: 1.3,
  error: 'dist/error.png',
  loading: 'dist/loading.gif',
  attempt: 1
})

Vue.http.headers.common['X-CSRFToken'] = VueCookie.get('csrftoken')

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyBUggg4I6FWB6sHijJGpXvBDdoZKqi1J7Y',
    libraries: 'places',
  }
})

Vue.component('google-map', VueGoogleMaps.Map)
Vue.component('google-marker', VueGoogleMaps.Marker)
Vue.component('google-cluster', VueGoogleMaps.Cluster)


export const googleMapStyles = [
  {
    "stylers": [
      {
        "hue": "#007fff"
      },
      {
        "saturation": 89
      }
    ]
  },
  {
    "featureType": "water",
    "stylers": [
      {
        "color": "#ffffff"
      }
    ]
  },
  {
    "featureType": "administrative.country",
    "elementType": "labels",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  }
]

var VueI18n = require('vue-i18n')
import locales from './locales'
Vue.use(VueI18n)

if (!localStore.get('locale')) {
  localStore.set('locale', 'ru')
}

Vue.config.lang = localStore.get('locale')

Object.keys(locales).forEach(function (lang) {
  Vue.locale(lang, locales[lang])
})

Vue.http.interceptors.push((request, next) => {
  request.headers.set('Locale', localStore.get('locale'))

  // Добавить хедер авторизации при наличии токена
  let jwt_header = auth.getAuthToken()

  if (jwt_header) {
    request.headers.set('Authorization', jwt_header)
  }

  next()
})

blockchains.init()
auth.checkAuth()

window.bind = function(func, context) {
  return function() { // (*)
    return func.apply(context, arguments);
  };
}


router.beforeEach((to, from, next) => {
  //Первой идет проверка на то требователен ли url к наличию постинг ключа

  if (to.matched.some(record => record.meta.requiresPostingKey)) {
    if (auth.user.has_posting_key==true){
      next()
    } else {
      alert('Для публикации требуется Private posting key golos.io')
      next('/profile')
    }
  }

  //Второй идет проверка на то требователен ли url к наличию авторизации
  else if (to.matched.some(record => record.meta.requiresAuth)) {
    if (auth.isAuth) {
      next()
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  }

  else {
    next()
  }
})

//Modal window check
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.isModal)) {
      store.dispatch('getModal', to.meta.data)
      next()
  } else {
    store.commit('hideModal')
    next()
  }
})
console.log('app init')

sync(store, router)

new Vue({
  router: router,
  store: store,
  filters: filters,
  el: '#app',
  render: h => h(App)
})
