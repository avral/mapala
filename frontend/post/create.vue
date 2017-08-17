<template lang="pug">
  post-form(:isEditForm="false", @createPost="createPost")
</template>

<script>
  import PostForm from './__parts/form.vue'
  import bc from '../blockchains'
  import { mapMutations, mapState } from 'vuex'

  export default {
    computed: mapState(['postForm']),

    methods: {
      ...mapMutations(['resetPostForm', 'setPostSavingStateTo', 'addPost']),

      async createPost () {
        try {
          this.setPostSavingStateTo(true)
          const { body } = await bc.createPost(this, this.postForm)

          this.setPostSavingStateTo(false)
          this.addPost(body)

          this.$parent.closeModal()
          this.resetPostForm()

          this.$notify({ message: this.$t('published'), type: 'success' })
        } catch (error) {
          this.setPostSavingStateTo(false)
          this.$notify({ message: error, type: 'warning' })
        }
      }
    },
    components: {
      PostForm
    }
  }
</script>
