<template>
    <form class="tab">
        <label v-if="golosAlreadyReg === null">У вас есть аккаунт в Golos.io?</label>
        <el-button-group v-if="golosAlreadyReg === null">
            <el-button @click="golosAlreadyReg = true" class="button small" type="primary">Да</el-button>
            <el-button @click="golosAlreadyReg = false" class="button small" type="primary">Нет</el-button>
        </el-button-group>

        <div v-else>
            <div class="inpt_w">
                <input type="text" placeholder="Login" v-model="username" class="inpt i-user"><label></label>
            </div>
            <div class="inpt_w">
                <input type="password" placeholder="Password" v-model="password" class="inpt i-pass"><label></label>
            </div>

            <div v-if="golosAlreadyReg">
                <div class="inpt_w">
                  <input type="text" placeholder="private posting key" v-model="wif" class="inpt i-key"><label></label>
                </div>
            </div>
            <div v-else>

                <div class="inpt_w">
                    <!--<input type="email" placeholder="email" v-model="email_request" class="inpt i-user"><label></label>-->
                    <input type="text" placeholder="Желаемый Golos.io username" v-model="bc_username" class="inpt i-user"><label></label>
                </div>

              <!--<div class="inpt_w">-->
                <!--<masked-input class="inpt i-phone" v-model="phone" mask="\+ 1 (111) 111-11-111" :placeholder="$t('telephone')" @input="rawVal = arguments[1]"/><label></label>-->
              <!--</div>-->

              <div class="inpt_w">
                <country-input @phoneNumberChanged="updatePhoneNumber"></country-input>
              </div>

              <div class="inpt_w" v-if="isSmsCodeInputVisible">
                <input v-model="pass_code" :placeholder="$t('sms_code')" type="text" class="inpt i-sms"><label></label>
              </div>


            </div>
            <vue-recaptcha v-show="!isPhoneVerified" ref="recaptcha" sitekey="6LfKfS8UAAAAAHEecRYjwgsL7p2SDXriEC5m0Otc" @verify="success"></vue-recaptcha>
            <el-button class="submit-button" :disabled="isSubmitDisabled" :loading="loading" @click="signUp" v-text="buttonText"></el-button>

        </div>
    </form>
</template>

<script>
  import VueRecaptcha from 'vue-recaptcha'
  import MaskedInput from 'vue-masked-input'
  import CountryInput from '../base/__parts/country-input.vue'
  import { showErrors } from '../utils'
  import Vue from 'vue'
  import auth from '../auth'
  import bc from '../blockchains'
  import { User, Verifier } from '../services'

  export default {
    components: { VueRecaptcha, MaskedInput, CountryInput },
    data () {
      return {
        recaptcha: '',
        rawVal: '',
        isPhoneVerified: false,
        isPhoneValid: false,
        isSmsCodeInputVisible: false,
        bc: bc,
        loading: false,
        username: '',
        password: '',
        phone: '',
        pass_code: '',
        bc_username: '',
        wif: '',
        errors: [],
        golosAlreadyReg: Vue.config.lang === 'ru' ? null : true
      }
    },
    computed: {
      buttonText () {
        return this.isPhoneVerified || this.golosAlreadyReg ? this.$t('sign_in') : this.$t('verify_phone')
      },
      isSubmitDisabled () {
        return !this.isPhoneValid
      }
    },
    methods: {
      success(res) {
        this.recaptcha = res
      },
      signUp () {
        const creds = {
          username: this.username,
          password: this.password,
          g_recaptcha_response: this.recaptcha
        }

        if (this.golosAlreadyReg === true) {
          creds.wif = this.wif
          auth.existngSignUp(this, creds, { name: 'index' })
        } else if (!this.isPhoneVerified) {
          Verifier.phone({
            number: this.rawVal,
            g_recaptcha_response: this.recaptcha
          }).then(() => {
            this.isSmsCodeInputVisible = true
            this.isPhoneVerified = true
          }).catch(error => showErrors(error.data, this))
        } else if (this.isPhoneVerified) {
          auth.signUp(this, {
            username: this.username,
            bc_username: this.bc_username,
            password: this.password,
            g_recaptcha_response: this.recaptcha,
            number: this.rawVal,
            passcode: this.pass_code
          }, { name: 'index' })
        }
        this.$refs.recaptcha.reset()
      },
      checkLogin () {
        this.config.userExists = false

        if (this.config.bcHasAcc === null) {
          this.config.bcUsername = ''
          this.config.bcExist = false
        }

        bc.getUser(this.username).then(res => {
          if (res) {
            this.config.bcExist = true
            this.config.bcUsername = res.name
          }
        })

        User.get({username: this.username}).then(res => {
          this.config.userExists = true
        })
      },
      updatePhoneNumber (phone) {
        this.rawVal = phone
      }
    },
    watch: {
      'rawVal' () {
        this.rawVal.indexOf('_') === -1 ? this.isPhoneValid = true : this.isPhoneValid = false
      }
    }
  }
</script>

<style>
    .el-message-box {
        width: 520px;
    }

  .get_sms {
    text-align: center;
  }
</style>
