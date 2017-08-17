import { Page, Comment, User, Group } from '../services'

export default {
  getModal ({ commit }, data) {
    console.log(data)
    commit('showModal')
    commit('setModal', data)
  },
  setPosts ({ commit, state }, params = {}) {
    commit('toglePostLoading')
    commit('noPage', false)

    // let params = {}
    params.page = state.posts.page
    params.author__username = state.posts.author
    params.created_at__lte = state.posts.range.lte
    params.created_at__gte = state.posts.range.gte

    Page.get(params).then(res => {
      let posts = res.body.results
      if (state.posts.page > 1) {
        posts = state.posts.data.concat(posts)
      }
      commit('setPosts', posts)
      let noPage = state.posts.data.length ? false : true
      if (!res.body.next) {
        commit('noPage', true)
      }

      commit('toglePostLoading')
    })
  },
  setRange ({ dispatch, commit, state }, range) {
    commit('resetPage')
    commit('resetTags')
    if (range.lte) {commit('setLte', range.lte)}
    commit('setGte', range.gte)
    return dispatch('setPosts')
  },
  setTags ({ dispatch, commit, state }, tag) {
    commit('resetRange')
    commit('resetPage')
    commit('setTags', tag)

    const params = {
      tag: tag
    }

    return dispatch('setPosts', params)
  },
  nextPosts ({ dispatch, commit, state }) {
    commit('nextPage')
    return dispatch('setPosts')
  },
  authorPosts ({ dispatch, commit, state }, author) {
    commit('resetRange')
    commit('resetPage')
    commit('resetTags')
    commit('setAuthor', author)
    return dispatch('setPosts')
  },

  fetch_group_posts ({ commit, state }) {
    console.log('test1')
    commit('resetRange')
    commit('resetPage')
    commit('resetTags')
    commit('toglePostLoading')
    const params = {}
    params.page = state.posts.page // Page, not post
    params.group = 'rnd' // Дичь, убрать.

    Page.get(params).then(res => {
      console.log('test2')
      let posts = res.body.results
      if (state.posts.page > 1) {
        posts = state.posts.data.concat(posts)
      }
      commit('setPosts', posts)

      if (!res.body.next) {
        commit('noPage', true)
      }
      commit('toglePostLoading')
    })
  },
  fetch_group_info ({ dispatch, commit }, group_name) {
    Group.get({ name: group_name }).then((response) => {
      commit('SET_GROUP_NAME', response.data.name)
      commit('SET_GROUP_LOGO', response.data.logo)
      commit('SET_GROUP_TITLE', response.data.title)

      dispatch('fetch_group_posts')
    })
  }
}
