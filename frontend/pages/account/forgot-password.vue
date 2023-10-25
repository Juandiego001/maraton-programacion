<template lang="pug">
v-row(class="fill-height my-0 mx-0 white")
  v-col(cols="12" md="6" class="px-0 py-0")
    v-img(cover class="fill-height" src="/coding.jpg" alt="Logo de fundación")
  v-col(cols="12" md="6")
    v-row(class="fill-height" align="center")
      v-col
        h1(class="primary--text text-center mb-3") Maratón UAO
        p(class="headline text-center") Recuperación de contraseña
        v-form(ref="form" class="text-center"
        @submit.prevent="recoverPassword")
          v-row(justify="center" align="center")
            v-col(cols="12" md="8" sm="8")
              text-field(v-model="email" label="Correo"
              :rules="[generalRules]")
          v-row(justify="center" align="center")
            v-col(cols="12" md="8")
              v-btn.white.primary--text.me-3( @click="login") Regresar
              v-btn(class="primary" type="submit") Recuperar contraseña
</template>

<script>
import generalRules from '../../mixins/form-rules/generalRules'
import { resetPasswordUrl } from '../../mixins/routes'

export default {
  name: 'IndexPage',
  mixins: [generalRules],
  layout: 'auth',

  data () {
    return {
      email: ''
    }
  },

  methods: {
    login () {
      this.$router.push('/account/login')
    },
    async recoverPassword () {
      try {
        if (!this.$refs.form.validate()) { return }
        const { message } = await this.$axios.$post(resetPasswordUrl,
          { email: this.email })
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}

</script>

<style scoped>
</style>
