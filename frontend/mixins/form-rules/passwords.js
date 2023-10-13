export default {
  computed: {
    passwordRules () {
      const rules = [
        v => /[A-Z]/.test(v) || 'Se requieren mayúsculas',
        v => /[a-z]/.test(v) || 'Se requireren minúsculas',
        v => /[^a-zA-Z\d]/.test(v) || 'Se requieren caracteres especiales',
        v => /\d/.test(v) || 'Agregar un número',
        v => (v && v.length >= 8) || 'Contraseña débil',
        v => (v && v.length <= 24) ||
          'Su contraseña ha excedido el límite de caracteres'
      ]
      if (this.form.new_password) {
        const rule = v => v === this.form.new_password ||
          'Las contraseñas no coinciden'
        rules.push(rule)
      }
      return rules
    }
  }
}
