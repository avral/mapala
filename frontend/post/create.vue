<template lang="pug">
  post-form(isEditForm="false", @createPost="createPost(data)")
</template>

<script>
  import PostForm from './__parts/form.vue'
  import bc from '../blockchains'
  import { mapMutations } from 'vuex'

  export default {
    methods: {
      ...mapMutations('resetPostForm'),

      async createPost (data) {
        try {
          await bc.createPost(this, data)
          this.resetPostForm()
          this.$notify({ message: this.$t('published'), type: 'success' })
        } catch (error) {
          this.$notify({ message: error, type: 'warning' })
        }
      },

      createPost () {
        if (!bc.current.key_valid) {
          this.close()
          return this.$notify({message: this.$t('add_key_err', {bc: bc.current.name}), type: 'warning'})
        }

        let err = ''

        if (!this.page.meta.location.name) err = this.$t('select_location')
        if (!this.page.body.length) err = this.$t('content_empty')
        if (!this.page.title.length) err = this.$t('title_empty')
        if (err) return this.$notify({ message: err, type: 'warning'})
        //  TODO make frontend form validation

        this.close()

        let permlink = this.$route.params.permlink ? this.$route.params.permlink : bc.getPermlink(this.page.title)
        // Divide edit/create logic
        steem.api.getContent(bc.current.blockchain_username, permlink, (err, res) => {
          if (res.id != 0 && !this.isEditPage) {
            return this.$notify({ message: this.$t('have_title'), type: 'warning'})
          } else {
            this.page.permlink = permlink
            bc.createPost(this, this.page).then(res => {
              console.log(res)
              this.page = {
                title: '',
                body: '',
                meta: {
                  images: [],
                  location: {},
                },
              },
                this.$notify({ message: this.$t('published'), type: 'success' })
              if (!this.isEditPage) {
                this.$store.commit('addPost', res.body)
              }
            }, err => {
              console.log(err)
              this.$notify({ message: err, type: 'warning'})
            })
          }
        })

      },

    },
    components: {
      PostForm
    }
  }
</script>
