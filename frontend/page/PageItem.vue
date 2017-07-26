<template>
    <div class="post" :id="'page_id_'+ page.id" :class="page.miniature ? 'w_i' : '' ">
        <router-link :to="{name: 'page', params: {author: page.author.username, permlink: page.permlink} }" v-if="page.miniature">
            <div class="post_image">
                <img class="post-image" :src="page.miniature" alt="" onerror="this.style.display='none'">
            </div>
        </router-link>
        <div class="short">
            <div class="top_block">
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
            <router-link :to="{name: 'page', params: {author: page.author.username, permlink: page.permlink} }">
                <h2 class="write_header">{{page.title}}</h2>
                <p class="write_text">{{page.body.replace(/<\/?[^>]+(>|$)/g, "")}}</p>
            </router-link>
        </div>
        <div class="bottom_block" v-bind:class="{mobileBlock: isMobile}">
            <div class="icons">
                <router-link :to="{name: 'page', params: {author: page.author.username, permlink: page.permlink }}" class="icon comment">{{ page.comments_count }} {{ numeral(page.comments_count) }}</router-link>
                <a class="icon repost" @click="share(page)">Рассказать</a>
            </div>
            <!-- <el-button v-if="!auth.isAuth" :loading="loading" class="support" @click="vote(page)">Поддержать <span>{{page.payout | toRub}} ₽</span></el-button> -->
            <el-button-group class="support_block" :loading="loading" v-bind:class="{ isDisabled: !auth.isAuth }">
              <el-button v-if="auth.isAuth" @click="vote(page)"><img style="height: 12px" src="../assets/like.png"></el-button>
              <el-button v-else :plain="true" :disabled="true" icon="check"></el-button>
              <el-button type="primary" class="support">{{page.payout | toRub}} ₽</el-button>
            </el-button-group>
            <!-- h4 v-else >Поддержали на ₽ {{page.payout | toRub}}</h4> -->
        </div>
        <CommentsBlock :page="page"></CommentsBlock>
    </div>
</template>

<script>
import bc from '../blockchains'
import auth from '../auth'
import {vkShare, commentsNumeral} from '../utils'

import {Page} from '../services'
import CommentsBlock from './CommentBlock.vue'

export default {
    props: ['page'],

    data() {
        return {
            loading: false,
            auth: auth
        }
        },
        computed: {
            isMobile() {
                return this.detectmob()
            }
        },
        methods: {

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
            },
            share(page){
                vkShare(page)
        },
        numeral(num){
          return commentsNumeral(num)
        },
        vote (page) {
                if (!bc.current.key_valid) {
                    // TODO Вынести проверку ключа в блокчейн модуль
                    return this.$notify({message: `Необходимо добавить ключ ${bc.current.name} в настройках`, type: 'warning'})
                }

                this.loading = true

                bc.vote(page).then(res => {
                    this.loading = false
                            this.$notify({message: `Голос принят`, type: 'success'})
                            Page.updatePost({author: page.author.bc_username, permlink: page.permlink}).then(res => {
                                page.payout = res.body.payout
                            })
                }, err => {
                    this.loading = false
                    this.$notify({title: 'Ошибка голосования', message: err, type: 'warning'})
          })
        }
    },
    components: {
        CommentsBlock
    }
}
</script>

<style scoped>
    .post_image {
        min-height: 100px;
    }
    .mobileBlock {
        display: block !important;
    }
</style>
