<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options" :search="search" :disable-sort="true")
    template(#item.file_link="{ item }")
      .text-truncate {{ item.real_name ? item.real_name : item.link }}
    template(#item.options="{ item }")
      v-btn(color="success" depressed icon @click="getMaterial(item)")
        v-icon mdi-pencil-outline
      v-btn(v-if="item.real_name" color="primary"
      :href="`${downloadUrl}/${item.file_url}`" target="_blank" icon)
        v-icon mdi-download-outline
      v-btn(v-if="item.link" color="primary" :href="item.link" target="_blank"
      icon)
        v-icon mdi-link
      v-btn(color="error" icon @click="showConfirmDelete(item)")
        v-icon mdi-trash-can-outline
    template(#item.status="{ item }")
      | {{ item.status ? 'Activo' : 'Inactivo' }}

  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveMaterial")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ formTitle }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close

        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información del material
            v-col(v-if="form.real_name" cols="12" md="6")
              v-text-field(v-model="form.real_name" label="Nombre del archivo"
              filled dense readonly hide-details="auto")
            v-col(v-if="form.username" cols="12" md="6")
              v-text-field(v-model="form.username" label="Creado por"
              filled dense readonly hide-details="auto")
            v-col(cols="12" md="12")
              v-file-input(v-model="file" filled dense
              :label="form.real_name ? 'Subir otro archivo' : 'Subir archivo'"
              hide-details="auto" :rules="fileLinkRules")
            v-col(cols="12" md="12")
              text-field(v-model="form.link" label="Enlace"
              :rules="fileLinkRules")
            v-col(cols="12" md="12")
              v-textarea(v-model="form.description" filled depressed
              label="Descripción" hide-details="auto")

          v-row(v-if="form._id" dense)
            v-col(cols="12")
              v-checkbox(v-model="form.status" label="Activo"
              hide-details="auto")
            v-col(class="text-caption" cols="12" md="6")
              | ID: {{ form._id }}
            v-col(class="text-caption text-md-right" cols="12" md="6")
              | Modificado por: {{ form.updated_by }}
              | {{ $moment(form.updated_at) }}

        v-card-actions
          v-spacer
          v-btn(color="primary" depressed type="submit") Guardar

  v-dialog(v-model="confirmDelete" max-width="500px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-card(flat :tile="$vuetify.breakpoint.smAndDown")
      v-card-title.error.white--text
        | Confirmar eliminación
        v-spacer
        v-btn.white--text(icon @click="confirmDelete=false")
          v-icon mdi-close
      v-card-text.mt-3 ¿Seguro que desea eliminar el material?
      v-card-actions
        v-spacer
        v-btn.error(@click="deleteFile") Confirmar

  dialog-search(v-model="dialogSearch" :doSearch="doSearch")
</template>

<script>
import fileLinkRules from '~/mixins/form-rules/file-link'
import { materialUrl } from '~/mixins/routes'

export default {
  mixins: [fileLinkRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      search: '',
      file: null,
      confirmDelete: false,
      form: {
        _id: '',
        real_name: '',
        file_url: '',
        link: '',
        username: '',
        description: ''
      }
    }
  },

  head () {
    return { title: 'Materials' }
  },

  computed: {
    headers () {
      return [
        { text: 'Archivo/enlace', value: 'file_link' },
        { text: 'Estado', value: 'status' },
        { text: 'Opciones', align: 'center', value: 'options' }
      ]
    },
    formTitle () {
      return this.form._id ? 'Editar material' : 'Crear material'
    },
    downloadUrl () {
      return `${materialUrl}download`
    }
  },

  watch: {
    options: { handler () { this.getData() } },
    dialogEdit (value) {
      if (!value) {
        this.$refs.form.reset()
        this.form._id = ''
        this.file = null
      } else {
        this.$refs.form && this.$refs.form.resetValidation()
      }
    },
    confirmDelete (value) {
      if (!value) {
        this.form._id = ''
      }
    }
  },

  beforeMount () {
    this.moduleSlug = 'Materiales'
    this.canViewPage()
  },

  methods: {
    async getData () {
      try {
        this.items = (await this.$axios.$get(materialUrl)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    getFormData () {
      const formData = new FormData()
      for (const key of Object.keys(this.form)) {
        if (this.form[key] != null) { formData.append(key, this.form[key]) }
      }
      if (this.file) { formData.append('file', this.file) }
      return formData
    },
    async saveMaterial () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
            `${materialUrl}${this.form._id}`, this.getFormData()))
        } else {
          ({ message } = await this.$axios.$post(materialUrl,
            this.getFormData()))
        }
        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getMaterial (item) {
      try {
        this.form = (await this.$axios.$get(`${materialUrl}${item._id}`))
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    showConfirmDelete (item) {
      this.form._id = item._id
      this.confirmDelete = true
    },
    async deleteFile () {
      try {
        const { message } = await this.$axios.$delete(
          `${materialUrl}${this.form._id}`)
        this.getData()
        this.confirmDelete = false
        this.showSnackbar(message)
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
