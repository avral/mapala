<template>
	<AddPage :forEdit="true" @close="closeModal"></AddPage>
</template>

<script>
import AddPage from './AddPage.vue'

export default {
	methods: {
		closeModal() {
			// this.$emit('close')
			this.$parent.closeModal()
		}
	},
	components: {
		AddPage
	}
}
</script>
