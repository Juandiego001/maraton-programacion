export default {
  computed: {
    passwordEmptyRules () {
      return [
        v => (!v || /[A-Z]/.test(v)) || 'Se requieren mayúsculas',
        v => (!v || /[a-z]/.test(v)) || 'Se requireren minúsculas',
        v => (!v || /[^a-zA-Z\d]/.test(v)) ||
          'Se requieren caracteres especiales',
        v => (!v || /\d/.test(v)) || 'Agregar un número',
        v => (!v || v.length >= 8) || 'Contraseña débil',
        v => (!v || v.length <= 24) ||
          'Su contraseña ha excedido el límite de caracteres'
      ]
    }
  }
}
