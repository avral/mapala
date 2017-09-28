import vue from 'vue'
import resource from 'vue-resource'

vue.use(resource)

export const http = vue.http

export const Locomotive = vue.resource('/api/locomotive/')
export const EmailRequest = vue.resource('/api/email_request/')
export const Tag = vue.resource('/api/tags{/id}/')
export const Comment = vue.resource('/api/comments{/id}/')
export const BlockChain = vue.resource('/api/blockchains{/id}/')
export const Marker = vue.resource('/api/markers{/id}/', {}, {
  query: { method: 'GET', url: '/api/markers{/bbox}{/identifier}/' }
})

export const UserBlockChain = vue.resource('/api/user-blockchains{/id}/', {}, {
  'getNameByPostingKey': {
    method: 'GET', url: '/api/user-blockchains/get_name_by_posting_key/'
  },
})

export const Page = vue.resource('/api/pages{/permlink}/', {}, {
  'comments_tree': { method: 'GET', url: '/api/pages{/permlink}/comments_tree/'},
  'updatePost': { method: 'POST', url: '/api/pages/update_post/'},
  'trPost': { method: 'POST', url: '/api/pages/tr_post/'},
})

export const MasterTag = vue.resource('/api/master-tags{/id}/', {}, {
  'tree': {
    method: 'GET', url: '/api/master-tags/tree/'
  },
  'ancestors': {
    method: 'GET', url: '/api/master-tags{/id}/ancestors/'
  }
})

export const User = vue.resource('/api/users{/username}/', {}, {
  'current': { method: 'GET', url: '/api/users/current/' },
  'signUp': { method: 'POST', url: '/sign-up/' },
  'setPassword': { method: 'POST', url: '/api/users/set_password/' },
  'resetPassword': { method: 'POST', url: '/api/users/reset_password/' },
  'existngSignUp': { method: 'POST', url: '/existng-sign-up/' },
  'setAvatar': { method: 'POST', url: '/api/users{/username}/set_avatar/' },
  'removeAvatar': { method: 'POST', url: '/api/users{/username}/remove_avatar/' },
  'initialBlockchains': { method: 'GET', url: '/api/users{/username}/initial_blockchains/' },
  'markers': { method: 'GET', url: '/api/users{/username}/markers/' }
})

export const Image = vue.resource('/api/images{/id}/', {}, {
  'upload': { method: 'POST', url: '/post_image/' }
})

export const Group = vue.resource('/api/groups{/name}/', {}, {
  'markers': { method: 'GET', url: '/api/markers/' }
})
