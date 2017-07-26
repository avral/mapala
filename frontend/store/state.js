import MobileDetect from 'mobile-detect'
var MD = new MobileDetect(window.navigator.userAgent)
console.log(MD.mobile())

export default {
    modal: {
        show: false,
        data: null,
    },
    posts: {
        data: [],
        author: null,
        page: 1,
        has_not_pages: false,
        loading: false,
        range: {
            gte: null,
            lte: null,
        },
        tags: null,
    },
    mobile: MD,
}