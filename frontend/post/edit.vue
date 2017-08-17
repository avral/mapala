<template lang="pug">
  post-form(:isEditForm="true", @updatePost="updatePost")
</template>

<script>
import PostForm from './__parts/form.vue'
import bc from '../blockchains'
import { mapMutations, mapState } from 'vuex'

export default {
  computed: mapState(['postForm']),

  methods: {
    ...mapMutations(['resetPostForm', 'setPostSavingStateTo']),

    async updatePost () {
      try {
        this.setPostSavingStateTo(true)
        await bc.updatePost(this, this.postForm)
        this.setPostSavingStateTo(false)

        this.$notify({ message: this.$t('post_updated'), type: 'success' })
        this.$parent.closeModal()
        this.resetPostForm()
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
