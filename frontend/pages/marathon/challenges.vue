<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options" :disable-sort="true")
    template(#item.status="{ item }")
      | {{  item.status ? 'Activo' : 'Inactivo'  }}
    template(#item.options="{ item }")
      v-btn(class="mr-2" color="success" depressed icon
      @click="getChallenge(item)")
        v-icon mdi-pencil-outline
      v-btn(v-if="item.contest_url" color="primary"
      :href="`${contestDownloadUrl}/${item.contest_url}`" target="_blank" icon)
        v-icon mdi-file-download
      v-btn(v-if="item.contest_link" color="primary" :href="item.contest_link"
      target="_blank" icon)
        v-icon mdi-link

  //- Diálogo de edición
  v-dialog(v-model="dialogEditChallenge" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="formEdit" @submit.prevent="saveChallenges")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ formTitle }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEditChallenge=false")
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

  //- Diálogo de creación múltiple
  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveChallenges")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ formTitle }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close

        v-card-text.mt-3
          v-select(v-model="form.contestid" dense :items="contests"
          label="Competencia" filled :rules="generalRules"
          item-text="full_contest" item-value="_id" hide-details="auto")
          v-tabs.mt-3.mb-5(v-model="tab" center-active light)
            v-tab(v-for="(challenge, index) in challenges"
            :key="`tab${index}`")
              | {{ challenge.title ? challenge.title : 'Reto #' + (index + 1) }}
          v-tabs-items(v-model="tab")
            v-tab-item(v-for="(challenge, index) in challenges"
            :key="`challenge${index}`")
              v-card
                v-card-text
                  v-row(dense)
                    v-col(class="primary--text" cols="12" md="12")
                      | Información del reto
                    v-col(cols="12" md="6")
                      text-field(v-model="challenge.title"
                      label="Título" :rules="generalRules")
                    v-col(cols="12" md="6")
                      text-field(v-model="challenge.name"
                      label="Nombre archivo fuente")
                    v-col(cols="12" md="12")
                      v-select(v-model="challenge.languagesid" dense
                      :items="languages" label="Lenguajes aceptados" filled
                      multiple small-chips :rules="generalRules"
                      item-text="name" item-value="_id" hide-details="auto")
                    v-col(cols="12" md="12")
                      v-select(v-model="challenge.difficultyid"
                      label="Dificultad" dense :items="difficulties" filled
                      item-text="name" item-value="_id" hide-details="auto")
                    v-col(cols="12" md="12")
                      v-select(v-model="challenge.topicsid" dense
                      :items="topics" label="Temáticas" filled multiple
                      small-chips :rules="[]" item-text="title" item-value="_id"
                      hide-details="auto")

        v-card-actions
          v-spacer
          v-btn(@click="addChallenge") Agregar otro reto
          v-btn(color="primary" type="submit") Guardar

  //- Diálogo de búsqueda
  v-dialog(v-model="dialogSearch" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(@submit.prevent="doSearch")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title.primary.white--text Búsqueda de retos
          v-spacer
          v-btn.primary(fab small depressed @click="dialogSearch=false")
            v-icon mdi-close
        v-card-text.mt-3
          v-row(dense)
            v-col(cols="12" md="6")
              v-text-field(v-model="search.title" label="Título" filled
              hide-details="auto" dense)
            v-col(cols="12" md="6")
              v-select(v-model="search.contestid" dense :items="contests"
              label="Competencia" filled item-text="full_contest"
              item-value="_id" hide-details="auto")
            v-col(cols="12" md="6")
              v-select(v-model="search.difficultyid" label="Dificultad" dense
              :items="difficulties" filled item-text="name" item-value="_id"
              hide-details="auto")
            v-col(cols="12" md="6")
              v-select(v-model="search.topicsid" dense :items="topics"
              label="Temáticas" filled multiple chips :rules="[]"
              item-text="title" item-value="_id" hide-details="auto")
        v-card-actions
          v-spacer
          v-btn(depressed @click="clearSearch") Limpiar valores
          v-btn(color="primary" depressed type="submit") Buscar
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
      dialogEditChallenge: false,
      items: [],
      languages: [],
      contests: [],
      topics: [],
      difficulties: [],
      tab: 0,
      form: {
        _id: '',
        title: '',
        source: ''
      },
      search: {
        title: '',
        contestid: '',
        difficultyid: '',
        topicsid: ''
      },
      challenges: [
        {
          title: 'Reto #1',
          source: ''
        }
      ]
    }
  },

  head () {
    return { title: 'Challenges' }
  },

  computed: {
    headers () {
      return [
        { text: 'Reto', align: 'center', width: 6, value: 'title' },
        {
          text: 'Competencia',
          align: 'center',
          width: 12,
          value: 'full_contest'
        },
        { text: 'Estado', align: 'center', width: 6, value: 'status' },
        { text: 'Opciones', align: 'center', width: 6, value: 'options' }
      ]
    },
    formTitle () {
      return this.form._id ? 'Editar reto' : 'Crear reto'
    },
    contestDownloadUrl () {
      return `${contestUrl}download`
    }
  },

  watch: {
    options: { handler () { this.getData() } },
    dialogEditChallenge (value) {
      if (!value) {
        this.$refs.formEdit.reset()
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
        this.$refs.formEdit && this.$refs.formEdit.resetValidation()
      }
    },
    dialogEdit (value) {
      if (!value) {
        this.$refs.form.reset()
        this.challenges = [
          {
            title: 'Reto #1',
            source: ''
          }
        ]
      } else {
        this.getContests()
        this.getTopics()
        this.getDifficulties()
        this.getLanguages()
        this.$refs.form && this.$refs.form.resetValidation()
      }
    },
    dialogSearch (value) {
      if (value) {
        this.getContests()
        this.getTopics()
        this.getDifficulties()
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
        this.items = (await this.$axios.$get(challengeUrl)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveChallenges () {
      try {
        if ((this.$refs.form && !this.$refs.form.validate()) ||
        (this.$refs.formEdit && !this.$refs.formEdit.validate())) { return }

        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
              `${challengeUrl}${this.form._id}`, this.form))
        } else {
          ({ message } = await this.$axios.$post(challengeUrl,
            { challenges: this.challenges, contestid: this.form.contestid }))
        }

        this.getData()
        this.dialogEdit = false
        this.dialogEditChallenge = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getChallenge (item) {
      try {
        this.form = (await this.$axios.$get(`${challengeUrl}${item._id}`))
        this.dialogEditChallenge = true
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
    addChallenge () {
      const challengeCopy = this.$clone(this.challenges)
      challengeCopy.push(
        {
          title: `Reto #${this.challenges.length + 1}`,
          source: ''
        })
      this.challenges = challengeCopy
    },
    async doSearch () {
      try {
        let query = ''
        if (this.search.title) {
          query += `title=${this.search.title}&`
        }
        if (this.search.contestid) {
          query += `contestid=${this.search.contestid}&`
        }
        if (this.search.difficultyid) {
          query += `difficultyid=${this.search.difficultyid}&`
        }
        if (Array.isArray(this.search.topicsid) &&
          this.search.topicsid.length > 0) {
          query += `topicsid=${this.search.topicsid}`
        }

        this.items = (await this.$axios.$get(
          `${challengeUrl}?${query}`)).items
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
