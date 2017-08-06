<template>
<div>
	<div class="pf">
		<div class="head_img" style="background-image: url();">
			<i class="back"></i>
		</div>
		<div class="user">
			<div class="round_av">
				<img class="user_av" :src="user.avatar">
			</div>
			<div class="name verified">{{ user.bc_username }}</div>
		</div>
		<div class="bottom_bl" v-if="auth.user.username == user.username">
			<router-link :to="{name: 'userWallet', params: {user: auth.user.username}}" class="but ic wal">
        {{ $t('my_wallett') }}
			</router-link>

			<i class="divd"></i>

			<router-link :to="{name: 'userSettings', params: {user: auth.user.username}}" class="but ic set">
        {{ $t('setting') }}
			</router-link>
		</div>

	</div>
</div>
</template>

<script>
import auth from '../auth'
import bc from '../blockchains'
import {Page, User} from '../services'

import Top from '../base/Top.vue'


export default {
	props: ['has_not_pages'],

	data() {
		return {
			user: {},
			auth: auth,
		}
	},
	methods: {
      fetchUser() {
          User.get({username: this.$route.params.user}).then(res => {
              this.user = res.body
          })
      },
	},
	watch: {
      '$route'() {
        this.fetchUser()
      },
	},
	created() {
      this.fetchUser()
	}
}

</script>
<style scoped>
.change_lang{
  max-width: 494px;
  width: 100%;
  height: 60px;
  margin-bottom: 20px;
  border-radius: 6px;
  background-color: #fafafa;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
  border: solid 1px rgba(72, 84, 101, 0.2);
  display: flex;
  justify-content: space-between;
  padding: 0 26px;
  box-sizing: border-box;
}

.change_lang .lab{
  font: 700 18px/58px 'PT Sans';
  color: #485465;
}

.change_lang [type="radio"]{
  display: none;
}

.change_lang label{
  font: 700 14px/58px 'PT Sans';
  letter-spacing: 0.3px;
  color: #34495e;
  opacity: 0.5;
  padding-left: 35px;
  margin-left: 20px;
  cursor: pointer;
  position: relative;
}

.change_lang label:before{
  width: 25px;
  height: 25px;
  position: absolute;
  display: block;
  content: '';
  background-color: #eaeaea;
  background-repeat: no-repeat;
  border-radius: 50%;
  top: -3px;
  left: 0;
}

.change_lang [type="radio"]:checked + label{
  opacity: 1;
}
.change_lang [type="radio"]:checked + label:before{
  background-image: url(../assets/icon-checked-blue.svg);
}

.pf{
  border-radius: 6px;
  background-color: #fafafa;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
  border: solid 1px rgba(72, 84, 101, 0.2);
  box-sizing: border-box;
  max-width: 494px;
  width: 100%;
  margin-bottom: 20px;
}

.pf .head_img{
  background-color: #6d9ee1;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 160px;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
  position: relative;
}
.pf .user{
  position: relative;
  z-index: 5;
  margin: -60px auto 65px;
  text-align: center;
}
.pf .round_av{
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin: 0 auto 20px;
  display: block;
  background: url(../assets/icon-profile.svg) #fff no-repeat;
  background-size: cover;
  position: relative;
  overflow: hidden;
}
.pf .round_av img{
  display: block;
  width: 100%;
}
.pf .user .name{
  font-size: 26px;
  font-weight: 700;
  color: #485465;
  text-align: center;
  position: relative;
  display: inline-block;
}

.pf .user .name.verified:before{
  position: absolute;
  content: '';
  width: 21px;
  height: 21px;
  background: url(../assets/icon-blue-check.svg) no-repeat;
  top: -9px;
  right: -24px;
}

.pf .bottom_bl{
  border-top: solid 1px rgba(72, 84, 101, 0.2);
  height: 60px;
  display: flex;
  align-items: center;
}

.pf .bottom_bl .but{
  font: 700 18px/60px 'PT Sans';
  text-align: center;
  color: #485465;
  display: block;
  text-decoration: none;
  width: 50%;
}

.pf .bottom_bl .wal{
  background: url(../assets/icon-wallet.svg) no-repeat 16% center;
}

.pf .bottom_bl .set{
  background: url(../assets/icon-settings.svg) no-repeat 22% center;
}

.pf .bottom_bl .divd{
  width: 1px;
  background: rgba(72, 84, 101, 0.2);
  height: 48px;
}

.no_post{
  border-radius: 6px;
  background-color: #fafafa;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
  border: solid 1px rgba(72, 84, 101, 0.2);
  max-width: 494px;
  width: 100%;
  box-sizing: border-box;
  padding: 36px 45px 26px;
  text-align: center;
  margin-bottom: 20px;
}

.no_post p{
  font: 700 18px 'PT Sans';
  margin: 0 0 23px;
}

.no_post .blue_btn{
  letter-spacing: -0.5px;
  font: 700 14px/34px 'PT Sans';
  color: #fff;
  padding: 0 27px;
  border-radius: 3px;
  background-color: #6d9ee1;
  text-decoration: none;
  display: inline-block;
}
</style>
