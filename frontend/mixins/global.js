import { mapMutations } from 'vuex'

export default {

  computed: {
    dialogEdit: {
      get () { return this.$store.state.app.dialogEdit },
      ...mapMutations({ set: 'app/setDialogEdit' })
    }
  },

  methods: {
    ...mapMutations({
      showSnackbar: 'snackbar/show'
    })
  }
}
