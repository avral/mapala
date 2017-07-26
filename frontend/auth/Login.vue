<template>
    <form class="tab" action="" method="post" @submit.prevent="login">
        <div class="inpt_w">
            <input type="text" placeholder="Login" v-model="credentials.username" class="inpt i-user" required><label></label>
        </div>
        <div class="inpt_w">
            <input type="password" placeholder="Password" v-model="credentials.password" class="inpt i-pass" required><label></label>
        </div>
        <div v-for="error in Object.keys(errors)">
            <i class="el-icon-warning"></i> {{error}}: {{errors[error][0]}}
        </div>
        <button type="submit" class="submit-button">Войти</button>

        <router-link class="forgot" :to="{name: 'resetPassword'}">Забыли пароль?</router-link>
    </form>
</template>

<script>
    import auth from './index'

    export default {
        name: 'login',
        data() {
            return {
                credentials: {},
                errors: []
            }
        },
        methods: {
            login() {
                auth.login(this, this.credentials, this.$store.state.route.from.fullPath)
            }
        }
    }

</script>
<style lang="scss">
</style>

