import App from '../App.vue'
import Index from '../base/Index.vue'
import UserProfile from '../user/UserProfile.vue'
// import Signup from '../auth/SignUp.vue'
// import Login from '../auth/Login.vue'
import UserSettings from '../user/UserSettings.vue'
import Page from '../page/Page.vue'
import EditPage from '../page/EditPage.vue'
import AddPage from '../page/AddPage.vue'
import Auth from '../auth/Auth.vue'
import UserWallet from '../user/Wallet.vue'
// import ResetPassword from '../auth/ResetPassword.vue'
import DacomAuth from '../dacom/Auth.vue'
import Ico from '../ico/Ico.vue'
import MainIco from '../ico/MainIco.vue'
import AucIco from '../ico/AucIco.vue'
import InvestIco from '../ico/InvestIco.vue'
import TestMap from '../base/TestMap.vue'

export default [
    {
      path: '/dacom',
      component: DacomAuth
    },
    {
      path: '/test-map',
      component: TestMap
    },
    {
        path: '/ico',
        // name: 'ico',
        component: Ico,
        children: [
            {
                path: '',
                name: 'ico',
                // components: [
                //   top: MainIco,
                // ]
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
            },
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
                    isModal: true,
                },
               components: {
                modal: Auth
               }
            },
            {
                path: 'sign-up',
                name: 'signUp',
                meta: {
                    isModal: true,
                },
               components: {
                modal: Auth
               }
            },
            {
                path: 'reset',
                name: 'resetPassword',
                meta: {
                    isModal: true,
                },
               components: {
                modal: Auth
               }
            },
            {
               path: '/settings',
               name: 'userSettings',
               meta: {
                 isModal: true,
               },
               components: {
                modal: UserSettings
               }
           },
           {
               path: 'wallet',
               name: 'userWallet',
               meta: {
                 isModal: true,
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
                 needPosting: true,
               },
               components: {
                modal: AddPage
               }
           },
            {
                path: ':author/:permlink',
                name: 'page',
                meta: {
                    isModal: true,
                    // data: 'page'
                },
                // component: Page
                components: {
                  modal: Page
                }
            },
            {
                // FIXME Тут уже полная дичь, нужно все рефакторить..
                path: ':author/:permlink/edit',
                name: 'edit',
                meta: {
                    isModal: true,
                    needPosting: true,
                },
               components: {
                modal: EditPage
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
