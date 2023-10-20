<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options")
    template(#item.options="{ item }")
      v-btn.success--text(icon @click="getRole(item)")
        v-icon mdi-pencil
      v-btn(icon @click="getPermissions(item)")
        v-icon.primary--text mdi-shield-account-variant-outline

  v-dialog(v-model="dialogEdit" max-width="600px" scrollable
  :fullscreen="$vuetify.breakpoint.smAndDown")
    v-form(ref="form" @submit.prevent="saveRole")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ form._id ? 'Editar rol' : 'Crear rol' }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close
        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información del rol
            v-col(cols="12" md="12")
              text-field(v-model="form.name" label="Nombre"
              :rules="generalRules" maxlength="100")
          v-row(v-if="form._id" dense)
            v-col(class="text-caption" cols="12" md="6")
              | ID: {{ form._id }}
            v-col(class="text-caption text-md-right" cols="12" md="6")
              | Modificado por: {{ form.updated_by }}
              |  {{ $moment(form.updated_at) }}
        v-card-actions
          v-spacer
          v-btn(color="primary" depressed type="submit") Guardar
  dialog-permissions(v-model="dialogPermissions" :profileid="profileid")
</template>

<script>
import { roleUrl } from '~/mixins/routes'
import generalRules from '~/mixins/form-rules/general-rules'

export default {
  name: 'PermissionsPage',
  mixins: [generalRules],
  layout: 'default',

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      form: {
        name: ''
      },
      profileid: '',
      dialogPermissions: false
    }
  },

  computed: {
    headers () {
      return [
        { text: 'Rol', value: 'name' },
        { text: 'Estado', value: 'status' },
        { text: 'Opciones', value: 'options' }
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

  methods: {
    async getData () {
      try {
        const data = await this.$axios.$get(roleUrl)
        this.items = data.items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getRole (item) {
      try {
        const data = await this.$axios.$get(`${roleUrl}${item._id}`)
        this.form = data
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveRole () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(`${roleUrl}${this.form._id}`,
            this.form))
        } else {
          ({ message } = await this.$axios.$post(roleUrl, this.form))
        }
        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    getPermissions (item) {
      this.profileid = item._id
      this.dialogPermissions = true
    }
  }
}
</script>
