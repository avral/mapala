<template>
  <div>
    <header class="main_header">

      <div class="top_left_block">
        <router-link class="main_logo" v-bind:class="{ main_logoMobile: detectmob() }" :to="'/'">
          <img src="../assets/MapalaLogo.png"><span>MAPALA</span>
        </router-link>

        <div class="change_lang">
          <input type="radio" value="ru" id="rus" v-model="locale">
          <label for="rus" @click="cahngeLang('ru')">rus/golos</label>
          <input type="radio" value="en" id="eng" v-model="locale">
          <label for="eng" @click="cahngeLang('en')">eng/steem</label>
        </div>
      </div>

      <div class="top-right-block">

        <a href="https://fest.mapala.net" class="el-button mapala-fest-link">
          <span>MapalaFest</span>
        </a>

        <popover></popover>
        <div v-if="auth.isAuth" class="username_wrapper">
          <router-link v-if="auth.isAuth" :to="'/'+auth.user.username" >
            <div class="user">
              <span class="user_name">
                {{auth.user.username}}
              </span>
              <img v-if="auth.user.has_avatar" class="user_logo" :src="auth.user.avatar">
              <img v-if="!auth.user.has_avatar" class="no_avatar" src="../assets/icon-profile-w.svg">
            </div>
          </router-link>
        </div>

        <div class="divider"></div>

        <router-link v-if="!auth.isAuth" class="login" :to="{name: 'login'}">
          {{ $t('log_in') }}
        </router-link>

        <div v-if="auth.isAuth" class="right_button" v-on-click-outside="menuClose">
          <div v-if="auth.isAuth" @click="menuOpen" class="open_menu">{{ $t('menu') }}</div>
          <div v-if="auth.isAuth" :class="{active : menu_opened, user_menuMobile: detectmob() }" class="user_menu">

            <router-link class="wal" :to="{name: 'userWallet', params: {user: auth.user.username}}" >
              <i class="purce"></i>
              <span class="txt_i">{{ $t('my_wallett') }}</span>
              <span class="amount">{{ auth.balance }}</span>
            </router-link>
            <div class="divd"></div>
            <div class="mn">
              <router-link class="m_item" :to="{name: 'userSettings', params: {user: auth.user.username}}" >
                {{ $t('setting') }}
              </router-link>

              <router-link class="m_item" :to="'/ico/'">
                ICO
              </router-link>

              <a href="" v-if="auth.isAuth" class="m_item" @click="logout">{{ $t("log_out") }}</a>
            </div>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<script>
import Vue from 'vue';
import auth from '../auth'
import { icon } from 'vue-fontawesome'
import bc from '../blockchains'
import {detectmob} from '../utils'
import * as localStore from 'store'
import moment from 'moment'
import popover from './__parts/popover.vue'

import { mixin as onClickOutside } from 'vue-on-click-outside'

export default {
 mixins: [onClickOutside],
 data() {
   return {
    auth: auth,
    menu_opened: false,
    locale: 'ru',
   }
 },
  methods: {
    cahngeLang(locale) {
      auth.user.locale = locale
      this.locale = locale
      localStore.set('locale', locale)
      moment.locale(localStore.get('locale'))
      Vue.config.lang = localStore.get('locale')
      this.$store.dispatch('authorPosts', this.$store.state.posts.author)
      bc.setBlockchain()
    },
   menuOpen () {
    this.menu_opened = !this.menu_opened
   },
   menuClose() {
    if (this.menu_opened) {
      this.menu_opened = false
    }
   },
   logout() {
     auth.logout(this)
   },
   changeLocale() {
    Vue.config.lang == 'en' ? Vue.config.lang = 'ru' : Vue.config.lang = 'en'
    this.auth.user.locale=Vue.config.lang
   },
    //TODO перенести в utils и раcширить данный метод
    /**
     * detect mobile device
     * @return boolean
     */
    detectmob() {
       if(window.innerWidth <= 1000 && window.innerHeight <= 600) {
         return true;
       } else {
         return false;
       }
    }
 },
  created() {
    this.locale = Vue.config.lang
  },

  components: {
    'vf-icon': icon,
    popover
  }
}
</script>

<style lang="scss" scoped>
.main_header{
  width: 100%;
  width: -moz-available;
  width: -webkit-fill-available;
  height: 42px;
  background-image: linear-gradient(180deg,#5d7394,#4b5e7a);
  position: fixed;
  z-index: 100;
  top: 0;
  left: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 30px;
  padding-right: 30px;
}

.top_left_block {
  display: flex;
}
.main_logo{
  display: flex;
  height: 42px;
  margin-left: 0;
  justify-content: center;
  align-items: center;
  padding-right: 20px;
  margin-right: 20px;
}
.main_logoMobile {
  margin-left: 0!important;
}
.main_logo img{
  height: 34px;
  margin-right: 6px;
}

.main_header .user{
  right: 0;
  top: 0;
  position: relative;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0;
  line-height: 42px;
}
.main_header a {
  color: #fff;
  text-decoration: none;
}

.main_header .user_name{
  color: #fff;
  font-size: 14px;
  font-weight: 700;
}
.main_header .user_logo{
  margin-left: 12px;
  width: 27px;
  height: 27px;
  border-radius: 50%;
  overflow: hidden;
}

.main_header .no_avatar{
  margin-left: 12px;
  width: 27px;
  height: 27px;
  border-radius: 50%;
  overflow: hidden;
  background-repeat: no-repeat;
  background-size: contain;
}

.main_header .user_logo img{
  display: block;
  width: 100%;
}

.main_header .open_menu{
  color: #88ade0;
  font: 700 14px PT Sans;
  display: flex;
  align-items: center;
  width: 70px;
  padding-left: 0;
  height: 100%;
  position: relative;
  line-height: 42px;
  right: 0;
  top: 0;
  box-sizing: border-box;
  background: url(../assets/icon-menu.svg) no-repeat 53px center;
  cursor: pointer;
  transition: color .2s ease;
}

.main_header .open_menu:hover{
  color: #fff;
}

.main_header .open_menuMobile{
  width: 69px;
}

.main_header .login{
  color: #88ade0;
  font: 700 14px PT Sans;
  display: block;
  align-items: center;
  width: 70px;
  padding-left: 7px;
  height: 102%;
  line-height: 42px;
  box-sizing: border-box;
  background: url(../assets/icon-login.svg) no-repeat 53px center;
  cursor: pointer;
  transition: color .2s ease;
  text-decoration: none;
  margin-left: 10px;
}

.main_header .login:hover{
  color: #fff;
}


.main_header .divider{
  width: 1px;
  background: #4d5169;
  height: 42px;
  box-shadow: 0 -2px 7px 0 #2a2c3e;
}

.right_button {
  padding-left: 20px;
}

.user_menu.active{
  display: flex;
}

.user_menu{
  background: #5d7394;
  width: 350px;
  display: none;
  padding: 35px 0 16px;
  position: absolute;
  right: 30px;
  top: 50px;
  border-radius: 6px;
  color: #fff;
}

.user_menuMobile{
  right: 5px!important;
  width: 300px!important;
}

.user_menu:before{
  content: '';
  position: absolute;
  top: -8px;
  right: 35px;
  width: 0px;
  height: 0px;
  border-top: 18px solid #5d7394;
  border-left: 18px solid transparent;
  transform: rotateZ(-45deg);
  z-index: 100;
}

.user_menu .wal{
  width: 50%;
  display: flex;
  align-items: center;
  flex-direction: column;
  border-right: 1px solid #526683;
  padding-top: 27px;
  text-decoration: none;
  color: #ffffff;
}

.user_menu .mn{
  padding-left: 20px;
}

.user_menu .m_item{
  text-decoration: none;
  display: block;
  opacity: 0.87;
  color: #fff;
  margin-bottom: 23px;
  font: 700 16px 'PT Sans';
  padding: 2px 12px;
  transition: opacity 200ms ease;
}

.user_menu .m_item:hover{
  opacity: 1;
}

.user_menu .m_item:last-of-type{
  margin-bottom: 8px;
}

.user_menu .purce{
  width: 45px;
  height: 38px;
  display: block;
  background: url(../assets/icon-purce.svg) no-repeat;
  margin-bottom: 10px;
}

.user_menu .txt_i{
  font: 700 16px 'PT Sans';
  opacity: 0.87;
  width: 100%;
  text-align: center;
  margin-bottom: 18px;
}

.user_menu .amount{
  font: 700 24px 'PT Sans';
  text-align: center;
}

.change_lang{
  margin: 0;
  height: 42px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 20px;
}

.change_lang .lab{
  font: 700 18px/58px 'PT Sans';
  color: white;
}

.change_lang [type="radio"]{
  display: none;
}

.change_lang label{
  font: 700 14px/58px PT Sans;
  letter-spacing: .3px;
  color: #fff;
  opacity: 0.5;
  padding-left: 35px;
  margin-left: 0;
  cursor: pointer;
  position: relative;
  height: 42px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-right: 15px;
}

.change_lang label:before{
  width: 25px;
  height: 25px;
  position: absolute;
  display: block;
  content: "";
  background-color: #eaeaea;
  background-repeat: no-repeat;
  border-radius: 50%;
  left: 0;
}

.top-right-block {
  display: flex;
}
.top-right-block .username_wrapper {
  padding: 0 20px;
}
.change_lang [type="radio"]:checked + label{
  opacity: 1;
}
.change_lang [type="radio"]:checked + label:before{
  background-image: url(../assets/icon-checked-blue.svg);
}

@media screen and (max-width: 600px) {
  .username_wrapper {
    display: none;
  }

  .top_left_block {
    flex: 1;
  }

  .top-right-block {
    justify-content: space-between;
  }

}


@media screen and (max-width: 767px) {
  .change_lang {
    display: none;
  }

  .top_left_block {
    flex: 0.5;
  }

  .top-right-block {
    flex: 1;
    justify-content: space-around;
  }
}

.mapala-fest-link {
  display: flex;
  align-items: center;
  background: transparent !important;
  border: none !important;
  font-size: 12px !important;
}

.mapala-fest-link span {
  color: #fff;
  font-style: oblique;
}

@media screen and (max-width: 500px) {
  .mapala-fest-link {
    display: none;
  }
}
</style>
