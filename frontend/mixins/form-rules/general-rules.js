export default {
  computed: {
    generalRules () {
      return [v => !!v || 'El campo es requerido']
    }
  }
}
