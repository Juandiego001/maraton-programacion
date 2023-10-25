<template lang="pug">
v-dialog(:value="dialog" max-width="600px" scrollable
:fullscreen="$vuetify.breakpoint.smAndDown" @input="ev => $emit('input', ev)")
  v-card(flat :tile="$vuetify.breakpoint.smAndDown" scrollable)
    v-card-title(class="primary white--text") Mi perfil
      v-spacer
      v-btn(fab small depressed color="primary"
      @click="$emit('input', false)")
        v-icon mdi-close
    v-card-text(class="py-3")
      v-expansion-panels(v-model="panel" flat)
        v-expansion-panel
          v-expansion-panel-header(class="primary--text px-0") Perfil
          v-expansion-panel-content
            v-form
              v-row(dense)
                v-col(cols="12" md="6")
                  text-field(:value="profile.name" label="Nombre"
                  :readonly="true" dense)
                v-col(cols="12" md="6")
                  text-field(:value="profile.lastname" label="Apellido"
                  :readonly="true" dense)
                v-col(cols="12" md="6")
                  text-field(:value="profile.username" label="Usuario"
                  :readonly="true" dense)
                v-col(cols="12" md="6")
                  text-field(:value="profile.document" label="Documento"
                  :readonly="true" dense)
                v-col(cols="12")
                  text-field(:value="profile.email" label="Correo"
                  :readonly="true" dense)

        v-expansion-panel
          v-expansion-panel-header(class="primary--text px-0")
            | Cambiar contraseña
          v-expansion-panel-content
            v-form(ref="form" @submit.prevent="changePassword")
              v-row(dense)
                v-col(cols="12")
                  text-field-password(v-model="form.current_password"
                  label="Contraseña actual" :rules="generalRules"
                  autocomplete="current_password")
                v-col(cols="12" md="6")
                  text-field-password(v-model="form.new_password"
                  label="Nueva contraseña" :rules="passwordRules"
                  autocomplete="new_password")
                v-col(cols="12" md="6")
                  text-field-password(v-model="confirmPassword"
                  label="Confirmar contraseña" :rules="passwordRules")
                v-col(cols="12")
                  v-card(flat)
                    v-card-actions
                      v-spacer
                      v-btn(color="primary" depressed type="submit")
                        | Guardar
</template>

<script>
import { changePasswordUrl } from '~/mixins/routes'
import generalRules from '~/mixins/form-rules/generalRules'
import passwordRules from '~/mixins/form-rules/passwords'

export default {
  name: 'ProfilePage',
  mixins: [generalRules, passwordRules],

  model: {
    prop: 'dialog',
    event: 'input'
  },

  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    profile: {
      type: Object,
      default: () => {}
    }
  },

  data () {
    return {
      model: 0,
      panel: [0],
      form: {
        new_password: '',
        current_password: ''
      },
      confirmPassword: ''
    }
  },

  methods: {
    async changePassword () {
      try {
        if (!this.$refs.form.validate()) { return }
        const { message } = await this.$axios.$patch(
          changePasswordUrl, this.form)
        this.$refs.form.reset()
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}

</script>
