<template lang="pug">
  post-form(isEditForm="false", @createPost="createPost(post)")
</template>

<script>
  import PostForm from './__parts/form.vue'
  import bc from '../blockchains'
  import { mapMutations } from 'vuex'

  export default {
    methods: {
      ...mapMutations('resetPostForm'),

      async createPost (post) {
        try {
          post.permlink = bc.getPermlink(post.title)
          await bc.createPost(this, post)

          this.resetPostForm()
          this.$parent.closeModal()

          this.$notify({ message: this.$t('published'), type: 'success' })
        } catch (error) {
          this.$notify({ message: error, type: 'warning' })
        }
      }
    },
    components: {
      PostForm
    }
  }
</script>
