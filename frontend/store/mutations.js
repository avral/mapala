export default {
  showModal (state) {
    document.body.className = 'hideScroll'
    state.modal.show = true
  },
  hideModal (state) {
    document.body.removeAttribute('class')
    state.modal.show = false
  },
  setModal (state, data) {
    state.modal.data = data
  },
  setPosts (state, posts) {
    state.posts.data = posts
  },
  addPost (state, post) {
    state.posts.data.unshift(post)
  },
  setAuthor (state, author) {
    state.posts.author = author
  },
  setTags (state, tags) {
    state.posts.tags = tags
  },
  resetTags (state) {
    state.posts.tags = null
  },
  setLte (state, date) {
    state.posts.range.lte = date
  },
  setGte (state, date) {
    state.posts.range.gte = date
  },
  resetRange (state) {
    state.posts.range.gte = null
    state.posts.range.lte = null
  },
  nextPage (state) {
    state.posts.page ++
  },
  resetPage (state) {
    state.posts.page = 1
  },
  noPage (state, value) {
    state.posts.has_not_pages = value
  },
  toglePostLoading (state) {
    state.posts.loading = !state.posts.loading
  },
  setPostSavingStateTo (state, payload) {
    state.isPostSaving = payload
  },
  resetPostForm (state) {
    state.postForm = {
      title: '',
      body: '',
      meta: {
        images: [],
        location: {}
      }
    }
  },
  redirectBackPath (state, path) {
    state.modal.redirectBackPath = path
  },
  SET_GROUP_LOGO (state, logo) {
    state.group.logo = logo
  },
  SET_GROUP_TITLE (state, title) {
    state.group.title = title
  },
  SET_GROUP_NAME (state, name) {
    state.group.name = name
  },
  SET_LOCATION_NAME (state, name) {
    state.postForm.meta.location.name = name
  },
  SET_LOCATION_LAT (state, lat) {
    state.postForm.meta.location.lat = lat
  },
  SET_LOCATION_LNG (state, lng) {
    state.postForm.meta.location.lng = lng
  },
  SET_GROUP_META (state, name) {
    state.postForm.meta.group = name
  }
}
