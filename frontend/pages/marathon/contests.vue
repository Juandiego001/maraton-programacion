<template lang="pug">
v-container(fluid)
  v-data-table(:headers="headers" :items="items" :server-items-length="total"
  :options.sync="options")
    template(#item.status="{ item }")
      | {{  item.status ? 'Activo' : 'Inactivo'  }}
    template(#item.options="{ item }")
      v-btn(class="mr-2" color="success" depressed icon
      @click="getContest(item)")
        v-icon mdi-pencil-outline
      v-btn(v-if="item.real_name" color="primary"
      :href="`${downloadUrl}/${item.file_url}`" target="_blank" icon)
        v-icon mdi-download-outline
      v-btn(v-if="item.link" color="primary" :href="item.link" target="_blank"
      icon)
        v-icon mdi-link

  //- Diálogo de creación/edición
  v-dialog(v-model="dialogEdit" max-width="600px"
  :fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
    v-form(ref="form" @submit.prevent="saveTopic")
      v-card(flat :tile="$vuetify.breakpoint.smAndDown")
        v-card-title(class="primary white--text")
          | {{ form._id ? 'Editar competencia' : 'Crear competencia' }}
          v-spacer
          v-btn(class="white--text" icon @click="dialogEdit=false")
            v-icon mdi-close

        v-card-text(class="my-3")
          v-row(dense)
            v-col(class="primary--text" cols="12" md="12")
              | Información de la competencia
            v-col(cols="12" md="6")
              text-field(v-model="form.platform" label="Plataforma"
              :rules="generalRules")

            //- Fecha - Made at
            v-col(cols="12" md="6")
              v-menu(ref="menu" v-model="menu" :close-on-content-click="false"
              transition="scale-transition" offset-y min-width="auto")
                template(v-slot:activator="{ on, attrs }")
                  v-text-field(v-model="form.made_at" readonly v-bind="attrs"
                  label="Fecha de realización" v-on="on" hide-details="auto"
                  prepend-icon="mdi-calendar")
                v-date-picker(v-model="form.made_at"
                :active-picker.sync="activePicker"
                @change="saveDate")

            v-col(cols="12" md="6")
              text-field(v-model="form.name" label="Nombre")
            v-col(cols="12" md="6")
              v-file-input(v-model="file" label="Archivo"
              hide-details="auto")
            v-col(cols="12" md="12")
              text-field(v-model="form.link" label="Enlace")
            v-col(cols="12" md="6")
              v-checkbox(v-model="form.isTraining" label="Capacitación"
              hide-details="auto")
            v-col(v-if="form._id" cols="12" md="6")
              v-checkbox(v-model="form.status" label="Activo"
              hide-details="auto")
          v-row(v-if="form._id" dense)
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
        v-card-title.primary.white--text Búsqueda de competencias
          v-spacer
          v-btn.primary(fab small depressed @click="dialogSearch=false")
            v-icon mdi-close
        v-card-text.mt-3
          v-row(dense)
            v-col(cols="12" md="6")
              v-text-field(v-model="search.platform" label="Plataforma" filled
              hide-details="auto" dense clearable)
            v-col(cols="12" md="6")
              v-text-field(v-model="search.name" label="Nombre" filled
              hide-details="auto" dense clearable)
            v-col(cols="12" md="12")
              v-select(v-model="search.isTraining" label="Tipo"
              hide-details="auto" :items="typeSearchItems" filled dense)
            v-col(cols="12" md="6")
              v-menu(ref="searchMenuInitial" v-model="searchMenuInitial"
              offset-y :close-on-content-click="false"
              transition="scale-transition" min-width="auto")
                template(v-slot:activator="{ on, attrs }")
                  v-text-field(v-model="search.initial_date" readonly
                  v-bind="attrs" label="Fecha de inicial" v-on="on"
                  hide-details="auto" prepend-icon="mdi-calendar" clearable)
                v-date-picker(v-model="search.initial_date"
                :active-picker.sync="activeSearchInitialPicker"
                @change="saveSearchInitialDate")
            v-col(cols="12" md="6")
              v-menu(ref="searchMenuEnd" v-model="searchMenuEnd" offset-y
              :close-on-content-click="false" transition="scale-transition"
              min-width="auto")
                template(v-slot:activator="{ on, attrs }")
                  v-text-field(v-model="search.end_date" readonly v-bind="attrs"
                  label="Fecha de final" v-on="on" hide-details="auto"
                  prepend-icon="mdi-calendar" clearable)
                v-date-picker(v-model="search.end_date"
                :active-picker.sync="activeSearchEndPicker"
                @change="saveSearchEndDate")
        v-card-actions
          v-spacer
          v-btn(depressed @click="clearSearch") Limpiar valores
          v-btn(color="primary" depressed type="submit") Buscar
</template>

<script>
import generalRules from '../../mixins/form-rules/general-rules'
import { contestUrl } from '../../mixins/routes'

export default {
  mixins: [generalRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      activePicker: null,
      activeSearchInitialPicker: null,
      activeSearchEndPicker: null,
      menu: false,
      searchMenuInitial: false,
      searchMenuEnd: false,
      form: {
        _id: '',
        platform: '',
        made_at: '',
        name: '',
        file_url: '',
        link: '',
        isTraining: false
      },
      search: {
        platform: '',
        initial_date: '',
        end_date: '',
        name: '',
        isTraining: ''
      },
      file: null
    }
  },

  head () {
    return { title: 'Contests' }
  },

  computed: {
    headers () {
      return [
        { text: 'Plataforma', align: 'center', value: 'platform' },
        { text: 'Fecha de realización', align: 'center', value: 'made_at' },
        { text: 'Estado', align: 'center', value: 'status' },
        { text: 'Opciones', align: 'center', value: 'options' }
      ]
    },
    downloadUrl () {
      return `${contestUrl}download`
    },
    typeSearchItems () {
      return [
        { text: 'Todos', value: '' },
        { text: 'Capacitación', value: true },
        { text: 'No capacitación', value: false }
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
    },
    menu (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    searchMenuInitial (val) {
      val && setTimeout(() => (this.activeSearchInitialPicker = 'YEAR'))
    },
    searchMenuEnd (val) {
      val && setTimeout(() => (this.activeSearchEndPicker = 'YEAR'))
    }
  },

  beforeMount () {
    this.moduleSlug = 'Competencias'
    this.canViewPage()
  },

  methods: {
    getFormData () {
      const formData = new FormData()
      for (const key of Object.keys(this.form)) {
        if (this.form[key] != null) { formData.append(key, this.form[key]) }
      }
      if (this.file) { formData.append('file', this.file) }
      return formData
    },
    async getData () {
      try {
        this.items = (await this.$axios.$get(contestUrl)).items
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
              `${contestUrl}${this.form._id}`, this.getFormData()))
        } else {
          ({ message } = await this.$axios.$post(contestUrl,
            this.getFormData()))
        }

        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getContest (item) {
      try {
        this.form = (await this.$axios.$get(`${contestUrl}${item._id}`))
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    saveDate (date) {
      this.$refs.menu.save(date)
    },
    saveSearchInitialDate (date) {
      this.$refs.searchMenuInitial.save(date)
    },
    saveSearchEndDate (date) {
      this.$refs.searchMenuEnd.save(date)
    },
    async doSearch () {
      try {
        let query = ''
        for (const key of Object.keys(this.search)) {
          if (this.search[key] !== '') {
            query += `${key}=${this.search[key]}&`
          }
        }
        this.items = (await this.$axios.$get(
          `${contestUrl}?${query}`)).items
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
