<template>
	<create-post :forEdit="true" @close="closeModal"></create-post>
</template>

<script>
import CreatePost from './create.vue'

export default {
  methods: {
    closeModal () {
      this.$parent.closeModal()
    }
  },
  components: {
    CreatePost
  }
}
</script>
