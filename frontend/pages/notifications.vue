<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options")

    template(#item.options="{ item }")
      v-btn(class="mr-2" color="success" depressed icon
      @click="getUser(item)")
        v-icon mdi-pencil-outline
      v-btn(v-if="item.status === 'PENDING'" class="mr-2" color="primary"
      icon @click="resendLink(item)")
        v-icon mdi-email-fast-outline

  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveUser")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ form._id ? 'Editar usuario' : 'Crear usuario' }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close

        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información del usuario
            v-col(cols="12" md="6")
              text-field(v-model="form.name" label="Nombre completo"
              :rules="generalRules")
            v-col(cols="12" md="6")
              text-field(v-model="form.username" label="Usuario"
              :rules="generalRules")
            v-col(cols="12" md="12")
              text-field(v-model="form.email" label="Correo"
              :rules="generalRules")
            v-col(cols="12" md="12")
              text-field-password(v-model="form.password" label="Contraseña"
                :rules="passwordEmptyRules")

          v-row(v-if="form._id" dense)
            v-col(cols="12")
              v-select(v-model="form.status" label="Estado" filled dense
              hide-details="auto" :items="userStatus" item-value="value"
              item-text="text")
            v-col(class="text-caption" cols="12" md="6")
              | ID: {{ form._id }}
            v-col(class="text-caption text-md-right" cols="12" md="6")
              | Modificado por: {{ form.updated_by }}
              | {{ $moment(form.updated_at) }}

        v-card-actions
          v-spacer
          v-btn(color="primary" depressed type="submit") Guardar
</template>

<script>
import passwordsEmptyRules from '~/mixins/form-rules/passwords-empty'
import generalRules from '~/mixins/form-rules/general-rules'
import { userUrl } from '~/mixins/routes'

export default {
  mixins: [generalRules, passwordsEmptyRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      form: {
        _id: '',
        name: '',
        username: '',
        email: '',
        password: ''
      },
      photo: null
    }
  },

  head () {
    return { title: 'Users' }
  },

  computed: {
    headers () {
      return [
        { text: 'Nombre completo', value: 'name' },
        { text: 'Usuario', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Estado', value: 'status' },
        { text: 'Opciones', value: 'options' }
      ]
    },
    userStatus () {
      return [
        {
          text: 'Activo',
          value: 'ACTIVE'
        },
        {
          text: 'Pendiente de activación',
          value: 'PENDING',
          disabled: true
        },
        {
          text: 'Inactivo',
          value: 'INACTIVE'
        }
      ]
    }
  },

  watch: {
    options: { handler () { this.getData() } },
    dialogEdit (value) {
      if (!value) {
        this.$refs.form.reset()
        this.form._id = ''
      } else {
        this.$refs.form && this.$refs.form.resetValidation()
      }
    }
  },

  beforeMount () {
    this.moduleSlug = 'Notificaciones'
    this.canViewPage()
  },

  methods: {
    async getData () {
      try {
        const data = await this.$axios.$get(userUrl)
        this.items = data.items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveUser () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
            `${userUrl}${this.form._id}`, this.form))
        } else {
          ({ message } = await this.$axios.$post(userUrl, this.form))
        }

        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getUser (item) {
      try {
        this.form = (await this.$axios.$get(`${userUrl}${item._id}`))
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}
</script>
