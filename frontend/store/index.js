import Vue from 'vue'
import Vuex from 'vuex'
import state from './state'
import actions from './actions'
import mutations from './mutations'

import MobileDetect from 'mobile-detect'
var MD = new MobileDetect(window.navigator.userAgent)
// console.log(MD.mobile())

Vue.use(Vuex)

export default new Vuex.Store({
  state,
  actions,
  mutations
})