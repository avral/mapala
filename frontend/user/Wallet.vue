<template>
  <div>
    <div class="pop_back" @click.self="close">
      <div class="wallet">
        <i class="refresh"></i>
				<div class="in_wallet">В кошельке на {{ moment().format('DD.MM.YYYY') }}</div>
        <div class="coins">{{wallet.personal_tokens}} Монет</div>
        <!-- <div class="currency">{{ balance.golos }} <i class="down"></i></div> -->
        <div class="currency">{{ balance.golos }}</div>
				<div class="currency">{{ balance.gbg }}</div>
        <!-- <hr> -->
        <!-- <div class="info">
          Из чего состоит GBG: <br>
          Конвертация Монеты - GBG <br>
          Конвертация Голос - GBG <br>
          Чистые GBG
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import moment from 'moment'

import auth from '../auth'
import bc from '../blockchains'
import steem from 'steem'
import {User} from '../services'

import api from '../api'

export default {
  data () {
		return {
			moment: moment,
      error: false,
      auth: auth,
			balance: {
        golos: null,
        gbg: null,
      },
      wallet: null
		}
  },
	created() {
    bc.getUser().then(res => this.balance.golos = res.balance)
		bc.getUser().then(res => this.balance.gbg = res.sbd_balance)
    let that = this
      api.ico.wallet(auth.user.username, function(data) {
        that.wallet = data
      });
	},
  methods: {
		close() {
			this.$router.go(-1)
		}
  }
}
</script>

<style>
.wallet{
  margin: 0 auto;
  max-width: 480px;
  width: 100%;
  border-radius: 6px;
  background-color: #ffffff;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
  border: solid 1px rgba(72, 84, 101, 0.2);
  position: relative;
}

.wallet .refresh{
  position: absolute;
  width: 30px;
  height: 30px;
  display: block;
  cursor: pointer;
  right: 35px;
  top: 35px;
  background: url(../assets/icon-refresh.svg) no-repeat;
}

.wallet .in_wallet{
  font-size: 16px;
  letter-spacing: -0.5px;
  color: #545454;
  margin: 55px 0 5px 40px;
}

.wallet .coins{
  font-size: 40px;
    letter-spacing: -1.3px;
    line-height: 50px;
    margin: 0 0 5px 40px;
}

.wallet .currency{
  font-size: 20px;
  letter-spacing: -0.7px;
  margin-bottom: 50px;
  margin-left: 40px;
  position: relative;
  display: inline-block;
}

.wallet .down{
  position: absolute;
  background: url(../assets/icon-arrow-down-circle.svg) no-repeat;
  width: 19px;
  height: 19px;
  cursor: pointer;
  right: -45px;
  top: 3px;
}

.wallet .info{
  font-size: 14px;
  letter-spacing: -0.5px;
  color: #6b6b6b;
  margin-left: 30px;
  margin-bottom: 45px;
}

.wallet hr{
  margin: 0 14px 19px;
  border: 0;
  border-bottom: solid 1px rgba(72, 84, 101, 0.2);
}
</style>
