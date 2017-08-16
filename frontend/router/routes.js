import Index from '../base/Index.vue'
import UserSettings from '../user/UserSettings.vue'
import PostView from '../post/view.vue'
import EditPost from '../post/edit.vue'
import CreatePost from '../post/create.vue'
import Auth from '../auth/Auth.vue'
import UserWallet from '../user/Wallet.vue'
import DacomAuth from '../dacom/Auth.vue'
import Ico from '../ico/Ico.vue'
import MainIco from '../ico/MainIco.vue'
import AucIco from '../ico/AucIco.vue'
import InvestIco from '../ico/InvestIco.vue'
import GroupIndex from '../base/group-index.vue'
import IcoBlock from '../ico/IcoBlock.vue'

export default [
  {
    path: '/rnd',
    name: 'rnd',
    component: GroupIndex
  },
  {
    path: '/dacom',
    component: DacomAuth
  },
  {
    path: '/ico',
    component: Ico,
    children: [
      {
        path: '',
        name: 'ico',
        component: MainIco
      },
      {
        path: 'auction',
        name: 'auction',
        component: AucIco
      },
      {
        path: 'investors',
        name: 'investors',
        component: InvestIco
      }
    ]
  },
  {
    path: '/:user?',
    name: 'index',
    component: Index,
    children: [
      {
        path: 'login',
        name: 'login',
        meta: {
          isModal: true
        },
        components: {
          modal: Auth
        }
      },
      {
        path: 'sign-up',
        name: 'signUp',
        meta: {
          isModal: true
        },
        components: {
          modal: Auth
        }
      },
      {
        path: 'reset',
        name: 'resetPassword',
        meta: {
          isModal: true
        },
        components: {
          modal: Auth
        }
      },
      {
        path: '/settings',
        name: 'userSettings',
        meta: {
          isModal: true
        },
        components: {
          modal: UserSettings
        }
      },
      {
        path: 'wallet',
        name: 'userWallet',
        meta: {
          isModal: true
        },
        components: {
          modal: UserWallet
        }
      },
      {
        path: 'add',
        name: 'add',
        meta: {
          isModal: true,
          needPosting: true
        },
        components: {
          modal: CreatePost
        }
      },
      {
        path: ':author/:permlink',
        name: 'page',
        meta: {
          isModal: true
        },
        components: {
          modal: PostView
        }
      },
      {
        // FIXME Тут уже полная дичь, нужно все рефакторить..
        path: ':author/:permlink/edit',
        name: 'edit',
        meta: {
          isModal: true,
          needPosting: true
        },
        components: {
          modal: EditPost
        }
      }
    ]
  },
  {
    path: '*',
    component: {
      template: '<p>Page not found</p>'
    }
  }
]
