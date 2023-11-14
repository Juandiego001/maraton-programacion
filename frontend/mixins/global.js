import { mapMutations } from 'vuex'

export default {
  computed: {
    allowSearchIcon () {
      return ['Publicaciones', 'Actividades',
        'Carpetas', 'Perfiles', 'Administradores', 'Profesores', 'Acudientes',
        'Estudiantes']
    },
    allowCreateIcon () {
      return ['Publicaciones', 'Actividades', 'Comentarios',
        'Carpetas', 'Administradores', 'Profesores', 'Acudientes',
        'Estudiantes']
    },
    dialogEdit: {
      get () { return this.$store.state.app.dialogEdit },
      ...mapMutations({ set: 'app/setDialogEdit' })
    },
    dialogSearch: {
      get () { return this.$store.state.app.dialogSearch },
      ...mapMutations({ set: 'app/setDialogSearch' })
    },
    moduleSlug: {
      get () { return this.$store.state.app.moduleSlug },
      ...mapMutations({ set: 'app/moduleSlug' })
    },
    canSearch () {
      return this.$ability.can('read', this.moduleSlug)
    },
    canCreate () {
      return this.$ability.can('create', this.moduleSlug)
    }
  },

  methods: {
    ...mapMutations({
      showSnackbar: 'snackbar/show'
    }),
    canViewPage () {
      if (!this.$ability.can('read', this.moduleSlug)) {
        this.$router.push('/')
      }
    }
  }
}
