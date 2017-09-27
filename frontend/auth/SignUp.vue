<template>
    <form class="tab">
        <label v-if="golosAlreadyReg === null">У вас есть аккаунт в Golos.io?</label>
        <el-button-group v-if="golosAlreadyReg === null">
            <el-button @click="golosAlreadyReg = true" class="button small" type="primary">Да</el-button>
            <el-button @click="golosAlreadyReg = false" class="button small" type="primary">Нет</el-button>
        </el-button-group>

        <div v-else>
            <div class="inpt_w" v-if="golosAlreadyReg">
                <input type="text" placeholder="Login" v-model="username" class="inpt i-user"><label></label>
            </div>
            <div class="inpt_w" v-if="golosAlreadyReg">
                <input type="password" placeholder="Password" v-model="password" class="inpt i-pass"><label></label>
            </div>

            <div v-if="golosAlreadyReg">
                <div class="inpt_w">
                  <input type="text" placeholder="private posting key" v-model="wif" class="inpt i-key"><label></label>
                </div>
            </div>
            <div v-else>
                <p>
                  Мы меняем логику регистрации аккаунтов в блокчейне, в связи с этим регистрация временно приостановлена.
                  Оставьте свой e-mail и мы уведомим вас о возобновлении регистрации.
                  <br>
                  <br>
                  Или ознакомтесь с 
                  <a
                    href="https://mapala.net/mapala.girl/registracziya-na-mapalanet-c-samostoyatelxnoij-registraczieij-na-golosio/"
                    target="_blank">инструкцией
                  </a>
                </p>

                <div class="inpt_w">
                    <input type="email" placeholder="email" v-model="email_request" class="inpt i-user"><label></label>
                    <!-- <input type="text" placeholder="Желаемый Golos.io username" v-model="bc_username" class="inpt i-user"><label></label>
                    -->
                </div>
            </div>
            <vue-recaptcha ref="recaptcha" sitekey="6LfKfS8UAAAAAHEecRYjwgsL7p2SDXriEC5m0Otc" @verify="success"></vue-recaptcha>
            <el-button class="submit-button" :loading="loading" @click="signUp">{{ $t('sign_in') }}</el-button>
        </div>
    </form>
</template>

<script>
  import VueRecaptcha from 'vue-recaptcha'
  import {showErrors} from '../utils'
    import Vue from 'vue'
    import auth from '../auth'
    import bc from '../blockchains'
    import {User, http, EmailRequest} from '../services'

    export default {
      components: { VueRecaptcha },
        data() {
            return {
              recaptcha: '',
              bc: bc,
              loading: false,
                username: '',
                password: '',
                //bc_username: '',
                email_request: '',
                wif: '',
                errors: [],
                golosAlreadyReg: Vue.config.lang == 'ru' ? null : true
            }
        },
        methods: {
          success(res) {
            this.recaptcha = res
          },
            signUp() {
                let creds = {
                    username: this.username,
                    password: this.password,
                    g_recaptcha_response: this.recaptcha
                }

                if (this.golosAlreadyReg === true) {
                    creds.wif = this.wif
                    auth.existngSignUp(this, creds, {name: 'index'})
                } else {
                  EmailRequest.save({email_request: this.email_request, g_recaptcha_response: this.recaptcha}).then(res => {
                    this.$alert('Вы получите письмо сразу после возобновления регистрации', 'Спасибо', {confirmButtonText: 'OK'})
                  }, err => {
                    console.log(err)
                    showErrors(err.body, this)
                    //this.$notify({title: 'Error', message: 'Почта уже добавлена', type: 'warning'})
                  })
                }
              this.$refs.recaptcha.reset()
            },

        // TODO Сделать подсказки по доступности логина/блокчейн юзернейма
        checkLogin() {
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
        }
    },
    watch: {
        'username'() {
            // this.checkLogin()
        },
    }
}
</script>

<style>
    .el-message-box {
        width: 520px;
    }
</style>
