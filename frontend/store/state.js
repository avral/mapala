import MobileDetect from 'mobile-detect'
const MD = new MobileDetect(window.navigator.userAgent)
console.log(MD.mobile())

export default {
  mobile: MD,
  modal: {
    show: false,
    data: null,
    redirectBackPath: ''
  },
  posts: {
    data: [],
    author: null,
    page: 1,
    has_not_pages: false,
    loading: false,
    range: {
      gte: null,
      lte: null
    },
    tags: null
  },

  group: {
    name: '',
    logo: '',
    title: ''
  },

  isPostSaving: false,

  postForm: {
    title: '',
    body: '',
    meta: {
      image: [],
      location: {
        name: '',
        lat: '',
        lng: ''
      },
      group: 'rnd',
      tags: []
    }
  }
}
