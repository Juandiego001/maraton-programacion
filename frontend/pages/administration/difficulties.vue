<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options" :search="search")
    template(#item.status="{ item }")
      | {{  item.status ? 'Activo' : 'Inactivo'  }}
    template(#item.options="{ item }")
      v-btn(class="mr-2" color="success" depressed icon
      @click="getLanguage(item)")
        v-icon mdi-pencil-outline

  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveLanguage")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ formTitle }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close

        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información del dificultad
            v-col(cols="12" md="6")
              text-field(v-model="form.name" label="Nombre"
              :rules="generalRules")
            v-col(cols="12" md="6")
              v-text-field(v-model="form.value" dense filled depressed
              label="Valor" :rules="numberRules" maxlength="2")
            v-col(cols="12" md="12")
              v-textarea(v-model="form.description" label="Descripción"
              filled depressed auto-grow)

          v-row(v-if="form._id" dense)
            v-col(cols="12")
              v-checkbox(v-model="form.status" label="Activo")
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
import numberRules from '~/mixins/form-rules/numbers'
import { difficultyUrl } from '~/mixins/routes'

export default {
  mixins: [generalRules, numberRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      search: '',
      form: {
        _id: '',
        name: '',
        value: 0,
        description: ''
      }
    }
  },

  head () {
    return { title: 'Difficulties' }
  },

  computed: {
    headers () {
      return [
        { text: 'Dificultad', align: 'center', width: 6, value: 'name' },
        { text: 'Valor', align: 'center', width: 6, value: 'value' },
        { text: 'Descripción', align: 'center', width: 12, value: 'description' },
        { text: 'Estado', align: 'center', width: 6, value: 'status' },
        { text: 'Opciones', align: 'center', width: 6, value: 'options' }
      ]
    },
    formTitle () {
      return this.form._id
        ? 'Editar dificultad'
        : 'Crear dificultad'
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
    this.moduleSlug = 'Lenguajes'
    this.canViewPage()
  },

  methods: {
    async getData () {
      try {
        const data = await this.$axios.$get(difficultyUrl)
        this.items = data.items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveLanguage () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
              `${difficultyUrl}${this.form._id}`, this.form))
        } else {
          ({ message } = await this.$axios.$post(difficultyUrl, this.form))
        }

        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getLanguage (item) {
      try {
        this.form = (await this.$axios.$get(`${difficultyUrl}${item._id}`))
        this.dialogEdit = true
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
