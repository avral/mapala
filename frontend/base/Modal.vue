<template>
  <div v-if="modal.show" class="pop_back" @click.self="closeModal">
    <transition
    name="custom-classes-transition"
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
    mode="out-in"
    >
      <router-view name="modal"></router-view>
  </transition>
</div>
</template>

<script>
  import { mapState } from 'vuex'
  import Auth from '../auth/Auth.vue'
  import PostView from '../post/view.vue'
  import CreatePost from '../post/create.vue'
  import EditPost from '../post/edit.vue'

  export default {
  data () {
    return {
      backTo: '/'
    }
  },
  computed: mapState([
    'modal',
    'route'
    ]),
  created() {
    this.setBackPath ()
  },
  methods:{
    /**
     * Close modal window
     *
     */
     closeModal() {
      this.setBackPath ()
      this.$store.commit('hideModal')
      this.$router.push(this.backTo)
    },
      /**
       * set redirect path
       */
       setBackPath() {
        if (this.checkModal()) {
          this.backTo = this.route.from.fullPath
        }
        return
      },
      /**
       * Check modal window
       * @return boolean
       */
       checkModal() {
        let routeFrom = this.route.from

        if (!routeFrom.meta.isModal) {
          return true
        }
        return false
      }
    },
    components: {
      Auth,
      PostView,
      CreatePost,
      EditPost
    }
  }
</script>
