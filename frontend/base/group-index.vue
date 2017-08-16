<template>
  <div>
    <div class="wrapper">
      <div class="tape" v-bind:class="{ tapeMobile: detectmob() }" >


        <div class="group_avatar">
          <p>Ростов на Дону</p>
        </div>

        <router-link :to="{ name: 'add', params: { user: auth.user.username }}"
                     v-if="auth.isAuth"
                     class="add_post_to_group">

          <div class="av_wrap">
            <img class="user_av" :src="auth.user.avatar">
          </div>
          <div class="write_post">{{ $t("add_post_to_group") }} RND</div>
        </router-link>

        <post-list></post-list>

        <MugenScroll v-if="!has_not_pages" tag="mu" :handler="nextPosts" :should-handle="!loading">&nbsp;</MugenScroll>
      </div>

      <component v-if="!isMobile" v-bind:is="rightView"></component>
    </div>

    <modal></modal>
  </div>
</template>

<script>
  import auth from '../auth'
  import MugenScroll from 'vue-mugen-scroll'
  import { mapActions } from 'vuex'
  import PostMap from '../base/PostMap.vue'
  import PostList from '../post/post-list.vue'
  import UserProfile from '../user/UserProfile.vue'

  import Modal from './Modal.vue'
  import BlogMain from '../blog/BlogMain.vue'

  import blockchains from '../blockchains'

  export default {
    metaInfo () {
      return {
        title: 'mapala.net'
      }
    },
    data () {
      return {
        auth: auth,
        rightView: null
      }
    },
    methods: {
      ...mapActions(['fetch_group_posts']),

      nextPosts () {
        this.$store.dispatch('nextPosts')
      },
      authorPosts (user) {
        this.$store.dispatch('authorPosts', user)
          .then(this.setRight())
      },

      setRight () {
        const user = this.$store.state.posts.author
        if (user === 'mapala') {
          this.rightView = BlogMain
        } else {
          this.rightView = PostMap
        }
      },

      /**
       * detect mobile device
       * @return boolean
       */
      detectmob () {
        return window.innerWidth <= 1000 && window.innerHeight <= 600
      }
    },

    computed: {
      loading () {
        return this.$store.state.posts.loading
      },
      has_not_pages () {
        return this.$store.state.posts.has_not_pages
      },
      user () {
        return this.$route.params.user
      },
      isMobile() {
        return this.detectmob()
      }
    },
    //TODO Костыль, в ближайшее время перенести хранение ключей в VUEX, логику блокчейн в отдельный модуль, и хуки роутинга тоже отдельно!!!
    //TODO Дичь
    beforeRouteEnter (to, from, next) {
      if (to.matched.some(record => record.meta.needPosting && !blockchains.current.wif)) {
        this.$alert(
          'Добавьте, пожалуйста, ПРИВАТНЫЙ постинг ключ в настройках аккаунта', {
            confirmButtonText: 'Хорошо'
          }
        )
        next('/settings')
      } else {
        next()
      }
    },
    beforeRouteUpdate (to, from, next) {
      var user = to.params.user
      var userFrom = from.params.user
      if (to.matched.some(record => record.meta.isModal) || from.matched.some(record => record.meta.isModal)) {
        if (to.matched.some(record => record.meta.needPosting && !blockchains.current.wif)) {
          this.$alert(
            'Добавьте, пожалуйста, ПРИВАТНЫЙ постинг ключ в настройках аккаунта.', {
              confirmButtonText: 'Хорошо'
            }
          )
          next('/settings')
        }
        if (userFrom && userFrom === 'mapala') {
          this.rightView = BlogMain
        }
        if (user && user !== this.$store.state.posts.author && from.name === 'page') {
          this.authorPosts(user)
          next()
        } else {
          next()
        }
      } else {
        this.authorPosts(user)
        next()
      }
    },
    created () {
      console.log('test from created hook')
      this.fetch_group_posts()
    },
    components: {
      MugenScroll,
      PostList,
      UserProfile,
      PostMap,
      Modal,
      BlogMain
    }
  }
</script>

<style>
  .hideScroll {
    overflow-y: hidden;
  }
  .blog-nav {
    margin-bottom: 25px;
    text-align: center;
  }
  .blog-nav button {
    width: 100%;
  }
  .blog-nav .router-link-exact-active button {
    border-color: #50bfff;
    color: #50bfff;
  }
  .el-notification__content {
    text-align: left;
  }
  .tapeMobile {
    margin-left: 0!important;
  }

  .group_avatar {
    display: flex;
    justify-content: center;
    background-image: url(http://rostov-na-donu.igid.ru/img/upload/photos/www.ultrastar.ru.jpg);
    width: 100%;
    height: 150px;
    background-size: cover;
    background-position-y: -30px;
    border-radius: 10px 10px 0 0;
    margin: 0 auto;
    align-items: center;
  }

  .group_avatar p{
    font-size: 29px;
    font-weight: 600;
    color: white;
    text-shadow: 3px 2px 0px rgb(0, 0, 0);
  }

  .add_post_to_group {
    width: 100%;
    height: 60px;
    border-radius: 0 0 6px 6px;
    background-color: #ffffff;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    border: solid 1px rgba(72, 84, 101, 0.2);
    border-top: none !important;
    padding: 0 16px;
    display: flex;
    align-items: center;
    box-sizing: border-box;
    margin-bottom: 20px;
    cursor: pointer;
    justify-content: center;
    text-decoration: none;
  }
  .user_av {
    margin-right: 8px;
    width: 40px;
    height: 40px;
    overflow: hidden;
    border-radius: 50%;
  }
</style>
