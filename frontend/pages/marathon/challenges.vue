<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options" :search="search")
    template(#item.status="{ item }")
      | {{  item.status ? 'Activo' : 'Inactivo'  }}
    template(#item.options="{ item }")
      v-btn(class="mr-2" color="success" depressed icon
      @click="getChallenge(item)")
        v-icon mdi-pencil-outline

  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveTopic")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ formTitle }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close

        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información del reto
            v-col(cols="12" md="6")
              text-field(v-model="form.title" label="Título"
              :rules="generalRules")
            v-col(cols="12" md="6")
              text-field(v-model="form.name" label="Nombre archivo fuente")
            v-col(cols="12" md="12")
              v-select(v-model="form.languagesid" dense :items="languages"
              label="Lenguajes aceptados" filled multiple chips
              :rules="generalRules" item-text="name" item-value="_id"
              hide-details="auto")
            v-col(cols="12" md="6")
              v-select(v-model="form.contestid" dense :items="contests"
              label="Competencia" filled :rules="generalRules"
              item-text="full_contest" item-value="_id" hide-details="auto")
            v-col(cols="12" md="6")
              v-select(v-model="form.difficultyid" label="Dificultad" dense
              :items="difficulties" filled item-text="name" item-value="_id"
              hide-details="auto")
            v-col(cols="12" md="12")
              v-select(v-model="form.topicsid" dense :items="topics"
              label="Temáticas" filled multiple chips :rules="[]"
              item-text="title" item-value="_id" hide-details="auto")

          v-row(v-if="form._id" dense)
            v-col(v-if="form._id" cols="12")
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
import generalRules from '~/mixins/form-rules/general-rules'
import { topicUrl, difficultyUrl, contestUrl, challengeUrl, languageUrl }
  from '~/mixins/routes'

export default {
  mixins: [generalRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      search: '',
      contests: [],
      topics: [],
      languages: [],
      difficulties: [],
      form: {
        _id: '',
        title: '',
        source: ''
      }
    }
  },

  head () {
    return { title: 'Challenges' }
  },

  computed: {
    headers () {
      return [
        { text: 'Reto', align: 'center', width: 6, value: 'title' },
        { text: 'Competencia', align: 'center', width: 12, value: 'contest.full_contest' },
        { text: 'Estado', align: 'center', width: 6, value: 'status' },
        { text: 'Opciones', align: 'center', width: 6, value: 'options' }
      ]
    },
    formTitle () {
      return this.form._id ? 'Editar reto' : 'Crear reto'
    }
  },

  watch: {
    options: { handler () { this.getData() } },
    dialogEdit (value) {
      if (!value) {
        this.$refs.form.reset()
        this.form = {
          _id: '',
          title: '',
          source: ''
        }
      } else {
        this.getContests()
        this.getTopics()
        this.getDifficulties()
        this.getLanguages()
        this.$refs.form && this.$refs.form.resetValidation()
      }
    }
  },

  beforeMount () {
    this.moduleSlug = 'Retos'
    this.canViewPage()
  },

  methods: {
    async getData () {
      try {
        const data = await this.$axios.$get(challengeUrl)
        this.items = data.items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveTopic () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
              `${challengeUrl}${this.form._id}`, this.form))
        } else {
          ({ message } = await this.$axios.$post(challengeUrl, this.form))
        }

        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getChallenge (item) {
      try {
        this.form = (await this.$axios.$get(`${challengeUrl}${item._id}`))
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
    async getTopics () {
      try {
        this.topics = (await this.$axios.$get(topicUrl)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getDifficulties () {
      try {
        this.difficulties = (await this.$axios.$get(difficultyUrl)).items
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
    doSearch (value) {
      this.search = value
      this.dialogSearch = false
    }
  }
}
</script>
