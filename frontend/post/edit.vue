<template lang="pug">
  post-form(isEditForm="true", @updatePost="updatePost(data)")
</template>

<script>
import PostForm from './__parts/form.vue'
import bc from '../blockchains'

export default {
  methods: {

    async updatePost (data) {
      try {
        await bc.updatePost(this, data)
        this.$notify({ message: this.$t('post_updated'), type: 'success' })
        this.$parent.closeModal()
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
