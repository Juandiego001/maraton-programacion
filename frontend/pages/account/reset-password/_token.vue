<template lang="pug">
v-row(class="fill-height my-0 mx-0 white")
  v-col(cols="12" md="6" class="px-0 py-0")
    v-img(cover class="fill-height" src="/coding.jpg" alt="Logo de fundación")
  v-col(cols="12" md="6" class="text-center")
    v-row(class="fill-height" align="center")
      v-col(cols="12" md="12")
        h1(class="primary--text text-center mb-3") Maratón UAO
        p(class="headline text-center") Reestablecer contraseña
      v-col(cols="12" md="12")
        v-form(ref="form" class="text-center" @submit.prevent="resetPassword")
          v-row(justify="center" align="center")
            v-col(class="pb-0" cols="12" md="8" sm="8")
              text-field-password(v-model="form.new_password" label="Contraseña"
              :rules="passwordRules")
            v-col(cols="12" md="8" sm="8")
              text-field-password(v-model="confirm_password"
              label="Confirmar contraseña" :rules="passwordRules")
            v-col(cols="12" md="12")
              v-btn(color="primary" type="submit" depressed) Guardar
</template>
<script>
import { resetPasswordUrl } from '~/mixins/routes'
import passwordRules from '~/mixins/form-rules/passwords'

export default {
  name: 'ResetPage',
  mixins: [passwordRules],
  layout: 'auth',

  data () {
    return {
      form: {
        new_password: ''
      },
      confirm_password: ''
    }
  },

  head () {
    return { title: 'Reestablecer contraseña' }
  },

  methods: {
    async resetPassword () {
      try {
        this.$refs.form.validate()
        if (!this.$refs.form.validate()) { return }
        const { message } = await this.$axios.$patch(
          `${resetPasswordUrl}/${this.$route.params.token}`, this.form)
        this.showSnackbar(message)
        this.$router.push('/account/login')
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}
</script>
