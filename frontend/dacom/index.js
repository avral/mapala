import {Signature, ChainStore, FetchChain, Login} from 'graphenejs-lib'
import {Apis, ChainConfig} from 'graphenejs-ws'


const LOGIN_URL = '/auth/login/'
const SIGN_UP_URL = '/auth/sign_up/'


ChainConfig.networks.DACom = {
  core_asset: 'FLO',
  address_prefix: 'FLO',
  chain_id: '526880c720c677ef7b54f964fe68999d1e582a33c8636b0f3b4687d47ae2f67f'
}

let auth = {
  keys: {},
  authSig: '',
  account: {},

  init() {
    return new Promise((res, rej) => {
      Apis.instance('ws://144.217.15.182:11011', true).init_promise.then(() => {
        ChainStore.init().then(() => {
          res()
        }, err => rej(err))
      })
    })
  },

  getAuthSig(context) {
    let auth_hash = context.$cookie.get('authSigHash')
    return Signature.sign(auth_hash, this.keys.privKeys.active).toHex()
  },

  generateKeys(accountName, password) {
    this.keys = Login.generateKeys(accountName, password, ['active', 'owner', 'memo'])
  },

  signUp(accountName, password) {
    return new Promise((resolve, reject) => {
      FetchChain('getAccount', [accountName]).then(() => {
        reject('Account already exist')
      }, () => {
        try {
          this.generateKeys(accountName, password)
        } catch (e) {
          return reject(e.message)
        }

        resolve({
          account: accountName,
          owner_key: this.keys.pubKeys.owner,
          active_key: this.keys.pubKeys.active,
          memo_key: this.keys.pubKeys.memo,
        })
      })
    })
  },

  login(accountName, password) {
    return new Promise((resolve, reject) => {
      FetchChain('getAccount', [accountName]).then(res => {
        this.account = res.toJS()[0]

        try {
          var success = Login.checkKeys({
            accountName: accountName,
            password: password,
            auths: {
              active: this.account.active.key_auths
            }
          })
        } catch(e) {
          return reject(e.message)
        }

        if (success) {
          this.generateKeys(accountName, password)
          resolve()
        } else {
          reject('Invalid password')
        }
      }, () => {
        reject('User not exists')
      })
    })
  },
}

//auth.init().then(() => {
//  auth.login('avral96', 'P5Jcac1vcxBBhYanj3eUPU8MA94nZ2XjXUZ14KQX6DysH25f9BQL').then(() => {
//    console.log(auth.authSig)
//  })
//})

export default auth
