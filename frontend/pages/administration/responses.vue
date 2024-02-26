<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options" :search="search" :disable-sort="true")
    template(#item.status="{ item }")
      | {{  item.status ? 'Activo' : 'Inactivo'  }}
    template(#item.options="{ item }")
      v-btn(class="mr-2" color="success" depressed icon
      @click="getResponse(item)")
        v-icon mdi-pencil-outline

  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveResponse")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ formTitle }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close

        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información de la respuesta del juez
            v-col(cols="12" md="12")
              text-field(v-model="form.code" label="Código"
              :rules="generalRules")
            v-col(cols="12" md="12")
              //- Color
              v-menu(ref="menu" v-model="menu" :close-on-content-click="true"
              transition="scale-transition" offset-y min-width="auto")
                template(v-slot:activator="{ on, attrs }")
                  v-text-field(v-model="form.color" readonly v-bind="attrs"
                  label="Color" v-on="on" prepend-inner-icon="mdi-palette"
                  :color="form.color" filled hide-details="auto")
                v-color-picker(v-model="form.color" hide-canvas hide-inputs
                hide-sliders show-swatches swatches-max-height="100"
                :swatches="swatches")
            v-col(cols="12" md="12")
              v-textarea(v-model="form.description" label="Descripción"
              filled depressed auto-grow hide-details="auto")

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
import { responseUrl } from '../../mixins/routes'

export default {
  mixins: [generalRules],

  data () {
    return {
      menu: false,
      options: {},
      total: -1,
      items: [],
      search: '',
      form: {
        _id: '',
        code: '',
        description: '',
        color: '#F94144'
      }
    }
  },

  head () {
    return { title: "Judge's Responses" }
  },

  computed: {
    headers () {
      return [
        { text: 'Código', align: 'center', width: 6, value: 'code' },
        { text: 'Color', align: 'center', width: 12, value: 'color' },
        {
          text: 'Descripción', align: 'center', width: 12, value: 'description'
        },
        { text: 'Estado', align: 'center', width: 6, value: 'status' },
        { text: 'Opciones', align: 'center', width: 6, value: 'options' }
      ]
    },
    formTitle () {
      return this.form._id
        ? 'Editar respuesta del juez'
        : 'Crear respuesta del juez'
    },
    swatches: {
      get () {
        return [
          ['#F94144', '#F3722C'],
          ['#F8961E', '#F9844A'],
          ['#F9C74F', '#43AA8B'],
          ['#4D908E', '#577590'],
          ['#90BE6D', '#277DA1']
        ]
      }
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
    this.moduleSlug = 'Respuestas'
    this.canViewPage()
  },

  methods: {
    async getData () {
      try {
        const data = await this.$axios.$get(responseUrl)
        this.items = data.items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveResponse () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
              `${responseUrl}${this.form._id}`, this.form))
        } else {
          ({ message } = await this.$axios.$post(responseUrl, this.form))
        }

        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getResponse (item) {
      try {
        this.form = (await this.$axios.$get(`${responseUrl}${item._id}`))
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
