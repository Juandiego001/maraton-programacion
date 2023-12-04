<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
    :options.sync="options" :search="search")
    template(#item.options="{ item }")
      v-btn(icon @click="getRole(item)")
        v-icon.success--text mdi-pencil-outline
      v-btn(icon @click="getPermissions(item)")
        v-icon.primary--text mdi-shield-account-variant-outline
    template(#item.status="{ item }")
      | {{ item.status ? 'Activo' : 'Inactivo' }}

  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveRole")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title.primary.white--text {{ formTitle }}
          v-spacer
          v-btn.white--text( icon @click="dialogEdit=false")
            v-icon mdi-close
        v-card-text.my-3
          v-row(dense)
            v-col.primary--text(cols="12" md="12") Información del rol
            v-col(cols="12" md="12")
              v-text-field(v-model="form.name" label="Nombre" filled dense
              required :rules="generalRules" hide-details="auto"
              maxlength="100")
          v-row(v-if="form._id" dense)
            v-col.text-caption(cols="12" md="6") ID: {{ form._id }}
            v-col.text-caption.text-md-right(cols="12" md="6")
              | Modificado por: {{ form.updated_by }}
              | {{ $moment(form.updated_at) }}
        v-card-actions
          v-spacer
          v-btn(color="primary" depressed type="submit") Guardar

  dialog-permissions(v-model="dialogPermissions" :roleId="roleId"
  :getRole="getRole" :permissions="permissions")
  dialog-search(v-model="dialogSearch" :doSearch="doSearch")
</template>

<script>
import { roleUrl, permissionUrl } from '~/mixins/routes'
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
      search: '',
      roleId: '',
      permissions: [],
      dialogPermissions: false,
      form: {
        name: ''
      }
    }
  },

  head () {
    return { title: 'Roles' }
  },

  computed: {
    headers () {
      return [
        { text: 'Rol', align: 'center', value: 'name' },
        { text: 'Estado', align: 'center', value: 'status' },
        { text: 'Opciones', align: 'center', value: 'options' }
      ]
    },
    formTitle () {
      return this.form._id ? 'Editar rol' : 'Crear rol'
    }
  },

  watch: {
    options: { handler () { this.getData() } },
    dialogEdit (value) {
      if (!value) {
        this.form._id = ''
        this.$refs.form.reset()
        this.$refs.form.resetValidation()
      } else {
        this.$refs.form && this.$refs.form.resetValidation()
      }
    }
  },

  beforeMount () {
    this.moduleSlug = 'Roles'
    this.canViewPage()
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
    async saveRole () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(`${roleUrl}${this.form._id}`,
            this.form))
        } else {
          ({ message } = await this.$axios.$post(`${roleUrl}`,
            this.form))
        }
        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getRole (item) {
      try {
        this.form = await this.$axios.$get(`${roleUrl}${item._id}`)
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getPermissions (item) {
      try {
        this.permissions = (await this.$axios.$get(
          `${permissionUrl}${item._id}`)).items
        this.dialogPermissions = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    doSearch (value) {
      this.search = value
      this.dialogSearch = false
    }
  }
}
</script>
