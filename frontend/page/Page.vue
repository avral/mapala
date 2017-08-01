<template> 
  <!-- <div class="full_post pop_back" @click.self="close"> -->
  <!-- <div> -->
    <div class="post_block" v-loading.body="!page.body">
      <router-link v-if="page.next_page" class="prev_post" :to="page.next_page"></router-link>
      <router-link v-if="page.prev_page" class="next_post" :to="page.prev_page"></router-link>
      <div class="top_block">
        <div class="t_col">
          <div class="img_wrap">
            <router-link :to="'/'+page.author.username">
              <img class="user_av" :src="page.author.avatar">
            </router-link>
          </div>
          <div class="name_block">
            <router-link :to=" '/'+ page.author.username" class="name"> {{page.author.bc_username}}</router-link>
            <div class="date">{{page.created_at || page.updated_at | formatDate}}</div>
          </div>
          <div class="location" v-if="page.position_text">{{page.position_text}}</div>
        </div>
        <div class="t_col">
          <router-link class="edit"
          v-if="page.author.username == auth.user.username"
          :to="{name: 'edit', params: {author: page.author.username, permlink: page.permlink}}">Редактировать</router-link>
          <div class="close" @click="close"></div>
        </div>
      </div>
      <div v-if="page.miniature" class="main_image"><img :src="page.miniature"></div>
      <div class="content">
        <h1 class="c_header">{{page.title}}</h1>
        <!-- <article v-html="postBody" class="c_text"></article> -->
        <!-- <article v-html="page.body" class="c_text"></article> -->
        <!-- <vue-markdown :source="'<script>console.log('test')</script>'" class="c_text"></vue-markdown> -->
        <vue-markdown :source="postBody" class="c_text"></vue-markdown>
        <!-- <vue-markdown :source="'![Фото0112.jpg](https://images.golos.io/DQmd3kyy3sMNZ64iXMqYhAYto2GfRXcXXAwZqaKfNx9MtPM/%D0%A4%D0%BE%D1%82%D0%BE0112.jpg)'" class="c_text"></vue-markdown> -->
        <!-- <vue-markdown :source="page.body" class="c_text"></vue-markdown> -->
      </div>
      <div class="bottom_block">
        <div class="icons">
          <div class="icon comment">{{ page.comments_count }} {{ numeral(page.comments_count) }}</div>
          <a class="icon repost" @click="share(page)">Рассказать</a>
        </div>
        <!-- <el-button v-if="auth.isAuth" :loading="loading" class="support" @click="vote(page)">Поддержать <span>₽ {{page.payout | toRub}}</span></el-button> -->
        <el-button-group class="support_block" :loading="loading" v-bind:class="{ isDisabled: !auth.isAuth }">
          <el-button v-if="auth.isAuth" @click="vote(page)"><img style="height: 12px" src="../assets/like.png"></el-button>
          <el-button v-else :plain="true" :disabled="true" icon="check"></el-button>
          <el-button type="primary" class="support">{{page.payout | toRub}} ₽</el-button>
        </el-button-group>
      </div>
      <CommentsBlock id="comments" :page="page"></CommentsBlock>
    </div>
  </div>
<!-- </div> -->
</template>

<script>
  import Vue from 'vue'
  import VueMarkdown from 'vue-markdown'

  import bc from '../blockchains'
  import {vkShare, commentsNumeral} from '../utils'

  import Top from '../base/Top.vue'
  import auth from '../auth'
  import CommentsBlock from './CommentBlock.vue'
  import {Page,  Comment} from '../services'

  export default {
    components: {
      Comment,
      CommentsBlock,
      VueMarkdown
    },
    metaInfo () {
      return {
        meta: this.meta
      }
    },
    data () {
      return {
        navigate: {
          next: {},
          prev: {}
        },
        new_comment: {},
        page: {
          author: {},
          comments: [],
        },
        auth: auth,
        comments: [],
        mark_view:"",
        error:false,
        loading: false,
        meta: [
              { property: 'og:title', content: 'title' },
              { property: 'og:site_name', content: 'Title' },
              { property: 'og:description', content: 'Title' },
              { property: 'og:image', content: 'Title' },
          ]
      }
    },
    computed: {
      /**
       * TODO перенести в отдельную vue директиву
       * 
       * parce url to <img>
       * @return <img> tag
       */
      postBody() {
        var body = this.page.body ? this.page.body.replace(
            /(https?:\S*?\.(?:png|jpe?g|gif)(?:\?[^"']+?)?(?=<|\s))/igm,
            '<img src="$1"></img>'
        ) : ''
        return body
      }
    },
    methods: {
      vote (page) {
        if (!bc.current.key_valid) {
          // TODO Вынести проверку ключа в блокчейн модуль
          return this.$notify({message: `Необходимо добавить ключ ${bc.current.name} в настройках`, type: 'warning'})
        }

        this.loading = true

        bc.vote(page).then(res => {
          this.loading = false
          this.$notify({message: `Голос принят`, type: 'success'})
          Page.updatePost({author: page.blockchain_author, permlink: page.permlink}).then(res => {
            page.payout = res.body.payout
          })
        }, err => {
          this.loading = false
          this.$notify({title: 'Ошибка голосования', message: err, type: 'warning'})
        })
      },
      close() {
        // this.$emit('close')
        this.$parent.closeModal()
      },
      fetchComments(page){
        Page.comments_tree({permlink: this.$route.params.user + '*@*' + this.$route.params.permlink}).then(res => {
          page.comments = res.body
        })
      },
      addComment() {
        this.new_comment.page = this.page.id

        Comment.save(this.new_comment).then(res => {
          this.page.comments.push(res.body)
        })
      },
      get_page() {
        Page.get({permlink: this.$route.params.author + '*@*' + this.$route.params.permlink}).then(res => {
          this.page = res.body
          this.make_navigate()
          // this.scrollTop()
          document.title = res.body.title
          this.meta = [
              { property: 'og:title', content: res.body.title },
              { property: 'og:site_name', content: 'mapala.net' },
              { property: 'og:description', content: res.body.body .substring(0,70) },
              { property: 'og:image', content: res.body.meta.image[0] },
          ]

          // TODO почему функция лежит в Vue.options ?
          this.mark_view = Vue.options.filters.markdown(this.page.body)
        })
      },

      // scrollTop(){
      //   document.querySelector('.full_post').scrollTop = 0
      // },

      make_navigate() {
        this.page.prev_page = this.page.prev_page ? {
          name: 'page',
          params: {
            author: this.page.prev_page.author__username,
            permlink: this.page.prev_page.permlink
          }
        } : null

        this.page.next_page = this.page.next_page ? {
          name: 'page',
          params: {
            author: this.page.next_page.author__username,
            permlink: this.page.next_page.permlink
          }
        } : null
      },
      share(page) {
        vkShare(page)
      },
      numeral(num){
        return commentsNumeral(num)
      },
      getPageUrl(page){
        return('http://'+window.location.hostname+'/'+page.author+'/'+page.permlink)
      }
    },
    watch: {
      '$route'() {
        this.get_page()
      },
    },
    created() {
      this.get_page()
    },
  }
</script>


<style lang="scss">
  .ql-video {
    width: 100%;
    height: 400px;
  }
  .user_av {
    border-radius: 50%;
  }
  .prev_post{
    width: 70px;
    height: 70px;
    position: fixed;
    top: 48%;
    left: calc((100% - 866px)/2 - 130px);
    z-index: 102;
    background: url(../assets/icon-prev.svg) no-repeat;
    cursor: pointer;
  }

  .next_post{
    background: url(../assets/icon-prev.svg) no-repeat;
    transform: rotateZ(180deg);
    width: 70px;
    height: 70px;
    position: fixed;
    cursor: pointer;
    z-index: 102;
    top: 48%;
    right: calc((100% - 866px)/2 - 130px);
  }

  .post_block .close{
    background: url(../assets/icon-close-black.svg) no-repeat center center;
    width: 40px;
    height: 40px;
    cursor: pointer;
  }

  .post_block .edit{
    font: 700 14px/36px 'PT Sans';
    box-sizing: border-box;
    padding: 0 16px;
    cursor: pointer;
    user-select: none;
    margin-right: 30px;
    margin-left: 20px;
	width: 123px;
	height: 40px;
	border-radius: 23px;
	border: solid 2px #000000;
	font-family: PTSans;
	font-size: 14px;
	font-weight: bold;
	text-align: left;
	color: #000000;
	text-decoration: none;
  }

  .post_block{
    border-radius: 6px;
    background-color: #ffffff;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    border: solid 1px rgba(72, 84, 101, 0.2);
    max-width: 866px;
    width: 100%;
    margin: 0 auto 80px;
    position: relative;
  }

  .post_block .c_header{
    font: 700 40px 'PT Sans';
    letter-spacing: -0.8px;
    color: #20252d;
    margin: 0 30px 20px;
  }

  .post_block .c_text{
    font: 21px/1.52 'PT Sans';
    letter-spacing: -1px;
    color: #141823;
    margin: 0 30px 40px;
  }

  .post_block .top_block{
    display: flex;
    margin: 40px 30px 35px;
    justify-content: space-between;
  }

  .post_block .t_col{
    display: flex;
  }

  .post_block .top_block .img_wrap{
    border-radius: 50%;
    margin-right: 8px;
    width: 40px;
    height: 40px;
    flex-shrink: 0;
  }

  .post_block img{
    display: block;
  }

  .post_block .name_block{
    margin-right: 8px;
    margin-top: 1px;
  }

  .post_block .name{
    font: 700 16px/20px 'PT Sans';
    letter-spacing: -0.5px;
    color: #6d9ee1;
    text-decoration: none;
  }

  .post_block .date{
    font-size: 12px;
    letter-spacing: -0.5px;
    color: rgba(72, 84, 101, 0.7);
    line-height: 16px;
  }

  .post_block .top_block .location{
    margin-top: 4px;
    font-size: 16px;
    line-height: 18px;
    letter-spacing: -0.5px;
    color: #7e8793;
    padding-left: 12px;
    position: relative;
    background: url(../assets/icon-location-small.svg) no-repeat left 3px;
  }

  .post_block .bottom_block{
    display: flex;
    align-items: center;
    padding: 0 30px;
    margin-bottom: 30px;
  }

  .post_block .icons{
    display: flex;
    align-items: center;
  }

  .post_block .icon{
    display: block;
    cursor: pointer;
    font: 14px/34px 'PT Sans';
    letter-spacing: -0.5px;
    color: rgba(72, 84, 101, 0.7);
    padding-left: 23px;
    text-decoration: none;
  }

  .post_block .icon.comment{
    background: url(../assets/icon-comment.svg) no-repeat left center;
    margin-right: 18px;
  }

  .post_block .icon.repost{
    background: url(../assets/icon-repost.svg) no-repeat left center;
    margin-right: 18px;
  }

  .post_block .support{
    font: 14px/34px 'PT Sans';
    letter-spacing: -0.5px;
    color: rgba(255, 255, 255, 0.7);
    padding: 0 12px 0 12px;
    border-radius: 3px;
    text-decoration: none;
    // background: url(../assets/icon-support.svg) #6d9ee1 no-repeat 12px center;
    background: #6d9ee1;
    margin-right: 35px;
    cursor: pointer;
  }

  .support_block button {
    height: 31px;
  }

  .post_block .is-disabled{
      color: #bfcbd9;
      cursor: not-allowed;
      background-image: none;
      background-color: #eef1f6;
      border-color: #d1dbe5;
  }

  .post_block .support span{
    color: #ffffff;
    // padding-left: 10px;
    // border-left: 1px solid #fff;
    // margin-left: 14px;
  }

  .post_block .main_image{
    overflow: hidden;
    margin: 0 -1px 25px;
  }

  .post_block .main_image img{
    width: 100%;
  }

  .post_block .content{
    overflow: hidden;
  }

  .post_block .c_text img{
    /*max-height: 492px;*/
    max-width: 100%;
    text-align: center;
    margin: 24px auto;
    width: auto;
  }
</style>
