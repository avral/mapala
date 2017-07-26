<template>
  <div v-if="modal.show" class="pop_back" @click.self="closeModal">
    <transition 
    name="custom-classes-transition"
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
    mode="out-in"
    >
      <!-- <component v-bind:is="modal.data"></component> -->
      <router-view name="modal"></router-view>
  </transition>
</div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex'
  import Auth from '../auth/Auth.vue'
  import Page from '../page/Page.vue'
  import AddPage from '../page/AddPage.vue'
  import EditPage from '../page/EditPage.vue'

  export default {
  // props: [content],
  data() {
    return {
      backTo: '/',
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
      Page,
      AddPage,
      EditPage
    }
  }
</script>
