<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options" :search="search")
    template(#item.options="{ item }")
      v-btn(class="mr-2" color="success" depressed icon
      @click="getSolution(item)")
        v-icon mdi-pencil-outline
      v-btn(v-if="item.real_name" class="mr-2" color="primary" depressed icon
      :href="`${downloadUrl}/${item._id}`" target="_blank")
        v-icon mdi-download-outline
      v-btn(v-if="item.link" color="primary" :href="item.link" target="_blank"
      icon)
        v-icon mdi-link
    template(#item.status="{ item }")
      | {{ item.status ? 'Activo' : 'Inactivo' }}

  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveSolution")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title.primary.white--text
          | {{ formTitle }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close
        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información de la solución
            v-col(cols="12" md="12")
              v-select(v-model="form.challengeid" label="Reto" filled
              :items="challenges" item-text="full_challenge" item-value="_id"
              hide-details="auto" :rules="generalRules")
            v-col(v-if="form.real_name" cols="12" md="6")
              v-text-field(v-model="form.real_name" filled
              label="Nombre del archivo" hide-details="auto" readonly)
            v-col(cols="12" md="6")
              v-select(v-model="form.sourceid" label="Archivo fuente asociado"
              filled :items="sources" item-text="full_source" item-value="_id"
              hide-details="auto" :rules="generalRules"
              :disabled="!sources.length")
            v-col(cols="12" :md="form.real_name ? 12 : 6")
              v-file-input(v-model="file" filled
              :label="form.real_name ? 'Subir otro archivo' : 'Subir archivo'"
              hide-details="auto" :rules="fileLinkRules")
            v-col(cols="12" md="12")
              text-field(v-model="form.link" label="Enlace"
              :rules="fileLinkRules")
            v-col(cols="12" md="6")
              text-field(v-model="form.judgment_status"
              label="Respuesta del juez")
            v-col(cols="12" md="6")
              text-field(v-model="form.error" label="Error")
            v-col(cols="12" md="12")
              v-textarea(v-model="form.description" label="Descripción"
              filled rows="3" auto-grow hide-details="auto")

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

  dialog-search(v-model="dialogSearch" :doSearch="doSearch")
</template>

<script>
import generalRules from '../../mixins/form-rules/general-rules'
import fileLinkRules from '../../mixins/form-rules/file-link'
import { solutionUrl, sourceUrl, challengeUrl }
  from '../../mixins/routes'

export default {
  mixins: [generalRules, fileLinkRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      search: '',
      sources: [],
      challenges: [],
      file: null,
      form: {
        _id: '',
        challengeid: '',
        sourceid: '',
        link: '',
        description: '',
        judgment_status: '',
        error: ''
      }
    }
  },

  head () {
    return { title: 'Solutions' }
  },

  computed: {
    headers () {
      return [
        { text: 'Archivo', value: 'real_name' },
        { text: 'Archivo fuente asociado', value: 'full_source' },
        { text: 'Reto', value: 'full_challenge' },
        { text: 'Hecho por', value: 'username' },
        { text: 'Opciones', value: 'options' }
      ]
    },
    formTitle () {
      return this.form._id ? 'Editar solución' : 'Crear solución'
    },
    downloadUrl () {
      return `${solutionUrl}download`
    }
  },

  watch: {
    options: { handler () { this.getData() } },
    dialogEdit (value) {
      if (!value) {
        this.form._id = ''
        this.$refs.form.reset()
        this.form = {
          _id: '',
          challengeid: '',
          sourceid: '',
          link: '',
          description: '',
          judgment_status: '',
          error: ''
        }
      } else {
        this.getChallenges()
        this.$refs.form && this.$refs.form.resetValidation()
      }
    },
    'form.challengeid' (value) {
      if (value) { this.getSources(value) }
    }
  },

  beforeMount () {
    this.moduleSlug = 'Soluciones'
    this.canViewPage()
  },

  methods: {
    async getData () {
      try {
        const data = await this.$axios.$get(solutionUrl)
        this.items = data.items
        console.log('SOLUCIONES: ', data)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    getFormData () {
      const formData = new FormData()
      for (const key of Object.keys(this.form)) {
        if (this.form[key] != null) { formData.append(key, this.form[key]) }
      }
      if (this.file) {
        formData.append('file', this.file)
      }
      return formData
    },
    async saveSolution () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        const formData = this.getFormData()
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
            `${solutionUrl}${this.form._id}`, formData))
        } else {
          ({ message } = await this.$axios.$post(solutionUrl, formData))
        }
        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getSolution (item) {
      try {
        this.form = (await this.$axios.$get(`${solutionUrl}${item._id}`))
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getSources (challengeid) {
      try {
        this.sources = (await this.$axios.$get(
        `${sourceUrl}languages/${challengeid}`)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getChallenges () {
      try {
        this.challenges = (await this.$axios.$get(challengeUrl)).items
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
