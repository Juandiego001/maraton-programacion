<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options" :disable-sort="true")
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

  v-row(dense)
    v-col(cols="12" md="12")
      .primary--text Respuestas del juez
    v-col(v-for="(response, index) in responses" :key="`response${index}`")
      v-chip.white--text(:color="response.color")
        | {{ `${response.code}: ${response.description}` }}

  //- Diálogo de creación/edición
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
              v-select(v-model="form.contestid" label="Competencia" filled
              :items="contests" item-text="full_contest" item-value="_id"
              hide-details="auto" :rules="generalRules")
            v-col(cols="12" md="12")
              v-select(v-model="form.challengeid" label="Reto" filled
              :items="challenges" item-text="name" item-value="_id"
              hide-details="auto" :rules="generalRules"
              :disabled="!challenges.length")
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
              v-select(v-model="form.topicsid" label="Temática"
              filled :items="topics" item-text="title" item-value="_id"
              hide-details="auto" multiple dense small-chips
              :disabled="!topics.length")
            v-col(cols="12" md="12")
              v-select(v-model="form.structuresid" label="Estructura de datos"
              filled :items="structures" item-text="title"
              item-value="_id" hide-details="auto" multiple dense small-chips)
            v-col(cols="12" md="12")
              text-field(v-model="form.link" label="Enlace"
              :rules="fileLinkRules")
            v-col(cols="12" md="12")
              v-select(v-model="form.responseid" label="Respuesta del juez"
              filled :items="responses" item-text="description" item-value="_id"
              hide-details="auto" dense)
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

  //- Diálogo de búsqueda
  v-dialog(v-model="dialogSearch" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(@submit.prevent="doSearch")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title.primary.white--text Búsqueda de soluciones
          v-spacer
          v-btn.primary(fab small depressed @click="dialogSearch=false")
            v-icon mdi-close
        v-card-text.mt-3
          v-row(dense)
            v-col(cols="12" md="12")
              v-select(v-model="search.contestid" label="Competencia" filled
              :items="contests" item-text="full_contest" item-value="_id"
              hide-details="auto" clearable)
            v-col(cols="12" md="12")
              v-select(v-model="search.challengeid" label="Reto" filled
              :items="challenges" item-text="title" item-value="_id"
              hide-details="auto" clearable)
            v-col(cols="12" md="12")
              v-select(v-model="search.languageid" label="Lenguaje" filled
              :items="languages" item-text="name" item-value="_id"
              hide-details="auto" clearable)
        v-card-actions
          v-spacer
          v-btn(depressed @click="clearSearch") Limpiar valores
          v-btn(color="primary" depressed type="submit") Buscar
</template>

<script>
import generalRules from '../../mixins/form-rules/general-rules'
import fileLinkRules from '../../mixins/form-rules/file-link'
import {
  solutionUrl, contestUrl, challengeUrl, sourceUrl, topicUrl,
  languageUrl, structureUrl, responseUrl
}
  from '../../mixins/routes'

export default {
  mixins: [generalRules, fileLinkRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      sources: [],
      contests: [],
      challenges: [],
      topics: [],
      structures: [],
      languages: [],
      responses: [],
      file: null,
      form: {
        _id: '',
        contestid: '',
        challengeid: '',
        sourceid: '',
        topicid: [],
        structureid: [],
        link: '',
        responseid: '',
        description: ''
      },
      search: {
        contestid: '',
        challengeid: '',
        languageid: ''
      }
    }
  },

  head () {
    return { title: 'Solutions' }
  },

  computed: {
    headers () {
      return [
        { text: 'Competencia', value: 'full_contest' },
        { text: 'Reto', value: 'full_challenge' },
        { text: 'Archivo fuente asociado', value: 'full_source' },
        { text: 'Respuesta', value: 'full_response' },
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
          topicsid: [],
          structuresid: [],
          link: '',
          description: '',
          responseid: '',
          error: ''
        }
      } else {
        this.getContests()
        this.getStructures()
        this.$refs.form && this.$refs.form.resetValidation()
      }
    },
    dialogSearch (value) {
      if (value) {
        this.getContests()
        this.getChallenges()
        this.getLanguages()
      }
    },
    'form.contestid' (value) {
      if (value) {
        this.getChallenges(value)
        this.sources = []
      }
    },
    'form.challengeid' (value) {
      if (value) {
        this.getSources(value)
        this.getTopics(value)
      }
    },
    'search.contestid' (value) {
      if (value) {
        this.getChallenges(value)
        this.sources = []
      }
    }
  },

  beforeMount () {
    this.moduleSlug = 'Soluciones'
    this.canViewPage()
  },

  methods: {
    async getData () {
      try {
        this.items = (await this.$axios.$get(solutionUrl)).items
        this.getResponses()
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    getFormData () {
      const formData = new FormData()

      for (const key of Object.keys(this.form)) {
        if (this.form[key] != null &&
          !(['topicsid', 'structuresid'].includes(key))) {
          formData.append(key, this.form[key])
        }
      }

      if (this.form.topicsid) {
        for (const topicid of this.form.topicsid) {
          formData.append('topicsid', topicid)
        }
      }

      if (this.form.structuresid) {
        for (const structureid of this.form.structuresid) {
          formData.append('structuresid', structureid)
        }
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
    async getContests () {
      try {
        this.contests = (await this.$axios.$get(contestUrl)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getChallenges (value) {
      try {
        if (value) {
          this.challenges = (await this.$axios.$get(
            `${challengeUrl}contest/${value}`)).items
        } else {
          this.challenges = (await this.$axios.$get(challengeUrl)).items
        }
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
    async getTopics (challengeid) {
      try {
        this.topics = (await this.$axios.$get(
          `${topicUrl}challenge/${challengeid}`)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getStructures () {
      try {
        this.structures = (await this.$axios.$get(structureUrl)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getResponses () {
      try {
        this.responses = (await this.$axios.$get(responseUrl)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getLanguages () {
      try {
        this.languages = (await this.$axios.$get(languageUrl)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async doSearch () {
      try {
        let query = ''
        for (const key of Object.keys(this.search)) {
          if (this.search[key]) {
            query += `${key}=${this.search[key]}&`
          }
        }
        this.items = (await this.$axios.$get(
          `${solutionUrl}?${query}`)).items
        this.dialogSearch = false
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    clearSearch () {
      this.search = {}
      this.doSearch()
    }
  }
}
</script>
