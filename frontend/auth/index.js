import blockchains from '../blockchains'
import store from 'store'
import {User, http} from '../services'
import {showErrors} from '../utils'


const JWT_AUTH_URL = '/api-auth/'
const JWT_REFRESH_URL = '/api-auth-refresh/'

export default {
  // TODO Выпилить всю логику с блокчейнами в отдельный модуль
  isAuth: false,
  balance: '0 GOLOS',

  user: {
    username: ' '
  },

  refreshJWT() {
    return http.post(JWT_REFRESH_URL, {token: store.get('jwt')})
  },

  update() {
    return User.update({username: this.user.username}, this.user)
  },

  login(context, creds, redirect) {
    context.$http.post(JWT_AUTH_URL, creds).then(res => {
      store.set('jwt', res.body.token)

      this.isAuth = true
      this.user = res.body.user
      blockchains.initBlockchains()
      if (redirect) { context.$router.push(redirect) }

    }, res => {
      showErrors(res.body, context)
    })
  },

  existngSignUp(context, creds, redirect) {
    User.existngSignUp(creds).then(res => {
      store.clearAll()

      store.set('jwt', res.body.token)
      this.isAuth = true
      this.user = res.body.user

      // Добавляем ключ для голоса
      store.set(`golos_${this.user.username}_posting_key`, creds.wif)
      blockchains.initBlockchains()

      if (redirect) { context.$router.push(redirect) }

    }, res => {
      showErrors(res.body, context)
    })
  },

  signUp(context, creds, redirect) {
    User.signUp(creds).then(res => {
      store.clearAll()

      store.set('jwt', res.body.token)
      this.isAuth = true
      this.user = res.body.user

      // Добавляем ключ для голоса
      store.set(`golos_${this.user.username}_posting_key`, res.body.posting_key)
      blockchains.initBlockchains()

      context.$alert(
        res.body.posting_key,
        'Сохраните ваш приватный постинг ключ от golos.io', {
          confirmButtonText: 'Я сохранил ключ',
          callback: () => {
            if (redirect) { context.$router.push(redirect) }
          }
        }
      )

    }, res => {
      showErrors(res.body, context)
    })
  },

  logout(context) {
    this.isAuth = false
    this.user = {}

    store.remove('jwt')
  },

  checkAuth() {
    this.isAuth = !!store.get('jwt') ? true : false

    // Обновим токен и запросим юзера при старте приложения
    // Токен обновляется при каждом запуске приложения
    if (this.isAuth) {
      this.refreshJWT().then(res => {
        store.set('jwt', res.body.token)

        this.user = res.body.user
        blockchains.initBlockchains()
      }, res => {
        // Если токен просрочен или не правильный
        console.log('Auth error: ', res.body)
        this.logout()
      })
    }
  },

  getAuthToken() {
    let token = store.get('jwt')
    return !!token ? 'JWT ' + token : null
  }
}
