import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'

import routes from './routes'

Vue.use(Router)

export default new Router({
    routes: routes,
    mode: 'history',
    linkActiveClass: 'active',
    saveScrollPosition: true,
    scrollBehavior: function (to, from, savedPosition) {
            const position = {}
            var user = from.params.user
            if (user != store.state.posts.author && !from.matched.some(m => m.meta.isModal)) {
              position.x = 0
              position.y = 0
              return position
            }
          // }
    }
})
