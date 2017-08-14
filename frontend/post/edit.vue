<template lang="pug">
  post-form(isEditForm="true", @updatePost="updatePost(data)")
</template>

<script>
import PostForm from './__parts/form.vue'
import bc from '../blockchains'
import { mapMutations } from 'vuex'

export default {
  methods: {
    ...mapMutations('resetPostForm'),

    async updatePost (data) {
      try {
        await bc.updatePost(this, data)
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
