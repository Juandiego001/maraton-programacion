export default {
  computed: {
    numberRules () {
      return [
        v => !!v || 'El campo es requerido',
        v => !/,/g.test(v) || 'El número debe ser un entero',
        v => !/-/g.test(v) || 'El número debe ser un entero positivo',
        v => !/[^0-9]/g.test(v) || 'El número no debe contener, ' +
          ' letras signos de puntuación ni caracteres especiales'
      ]
    }
  }
}
