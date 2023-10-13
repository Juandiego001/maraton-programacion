<template lang="pug">
v-text-field(filled dense :label="label" hide-details="auto"
:type="showPassword ? 'text' : 'password'" :rules="rules"
:autocomplete="autocomplete" @input="ev => $emit('input', ev)")
  template(#append)
    v-btn(icon @click="showPassword=!showPassword")
      v-icon {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
</template>

<script>
export default {

  model: {
    prop: 'data',
    event: 'input'
  },

  props: {
    data: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: 'Contraseña'
    },
    rules: {
      type: Array,
      default: new Array(0)
    },
    autocomplete: {
      type: String,
      default: 'password'
    }
  },

  data () {
    return {
      showPassword: false
    }
  }
}
</script>
