<template>
  <div>
    <header class="main_header">
      <router-link class="main_logo" v-bind:class="{ main_logoMobile: detectmob() }" :to="'/'" ><img src="../assets/MapalaLogo.png"><span>MAPALA</span></router-link>

      <router-link v-if="auth.isAuth" :to="'/'+auth.user.username" >
        <div class="user">
          <span class="user_name">
            {{auth.user.username}}
          </span>
          <img v-if="auth.user.has_avatar" class="user_logo" :src="auth.user.avatar">
          <img v-if="!auth.user.has_avatar" class="no_avatar" src="../assets/icon-profile-w.svg">
        </div>
      </router-link>

      <div class="divider"></div>

      <router-link v-if="!auth.isAuth" class="login" :to="{name: 'login'}">
        Вход
      </router-link>

      <div v-on-click-outside="menuClose">
        <!-- <div v-if="auth.isAuth" @click="menuOpen" class="open_menu" v-bind:class="{ open_menuMobile: detectmob() }">Меню</div> -->
        <div v-if="auth.isAuth" @click="menuOpen" class="open_menu">Меню</div>
        <div v-if="auth.isAuth" :class="{active : menu_opened, user_menuMobile: detectmob() }" class="user_menu">

          <router-link class="wal" :to="{name: 'userWallet', params: {user: auth.user.username}}" >
            <i class="purce"></i>
            <span class="txt_i">Кошелек</span>
            <span class="amount">{{ auth.balance }}</span>
          </router-link>
          <div class="divd"></div>
          <div class="mn">
            <router-link class="m_item" :to="{name: 'userSettings', params: {user: auth.user.username}}" >
              Настройки
            </router-link>


            <!-- Закрыто до возобновления работы шлюза
            <router-link class="m_item" :to="'/ico/'">
              ICO
            </router-link>
            -->

            <!-- <a class="m_item" href="">FAQ</a> -->

            <a href="" v-if="auth.isAuth" class="m_item" @click="logout">
              {{ $t("base.logout") }}
            </a>
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
// import { mapActions } from 'vuex'
import {detectmob} from '../utils'

import { mixin as onClickOutside } from 'vue-on-click-outside'

export default {
 mixins: [onClickOutside],
 data() {
   return {
    auth: auth,
    menu_opened:false,
   }
 },
 methods: {
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
 components: {
  'vf-icon': icon,
 },
}
</script>

<style lang="scss" scoped>
.main_header{
  width: 100%;
  height: 42px;
  background-image: linear-gradient(to bottom, #5d7394, #4b5e7a);
  position: fixed;
  z-index: 100;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
}
.main_logo{
  display: block;
  // width: 85px;
  height: 34px;
  margin-left: 30px;
}
.main_logoMobile {
  margin-left: 0!important;
}
.main_logo img{
  // display: block;
  height: 34px;
}

.main_header .user{
  right: 100px;
  top: 0;
  position: absolute;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 17px 0 0;
  // padding-right: 100px;
}
.main_header a {
  color: #fff;
  text-decoration: none;
}
.main_header .main_logo span {
  padding-left: 5px;
  position: absolute;
  top: 30%;
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
  font: 700 14px 'PT Sans';
  display: flex;
  align-items: center;
  width: 99px;
  padding-left: 8px;
  height: 100%;
  position: absolute;
  right: 0;
  top: 0;
  box-sizing: border-box;
  background: url(../assets/icon-menu.svg) no-repeat 53px center;
  cursor: pointer;
  transition: color 200ms ease;
}

.main_header .open_menu:hover{
  color: #fff;
}

.main_header .open_menuMobile{
  width: 69px;
}

.main_header .login{
  color: #88ade0;
  font: 700 14px 'PT Sans';
  display: flex;
  align-items: center;
  width: 99px;
  padding-left: 8px;
  height: 100%;
  position: absolute;
  right: 0;
  top: 0;
  box-sizing: border-box;
  background: url(../assets/icon-login.svg) no-repeat 53px center;
  cursor: pointer;
  transition: color 200ms ease;
  text-decoration: none;
}

.main_header .login:hover{
  color: #fff;
}


.main_header .divider{
  width: 1px;
  position: absolute;
  top: 0;
  right: 100px;
  background: #4d5169;
  height: 100%;
  box-shadow: 0 -2px 7px 0px #2a2c3e;
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

</style>
