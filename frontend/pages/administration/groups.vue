<template>
  <v-container fluid>
    <v-data-table
      :headers="headers"
      :items="items"
      :server-items-length="total"
      :options.sync="options"
    >
      <!-- Bug v-slot https://stackoverflow.com/questions/61344980/v-slot-directive-doesnt-support-any-modifier -->
      <template #[`item.options`]="{ item }">
        <v-btn
          class="mr-2"
          color="success"
          depressed
          icon
          @click="getGroup(item)"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
        <v-btn
          color="primary"
          depressed
          icon
          @click="getStudents(item)"
        >
          <v-icon>
            mdi-account-school
          </v-icon>
        </v-btn>
      </template>
    </v-data-table>
    <v-dialog
      v-model="dialogEdit"
      max-width="600px"
      :fullscreen="$vuetify.breakpoint.smAndDown"
      scrollable
    >
      <v-form ref="form" @submit.prevent="saveGroup">
        <v-card flat :tile="$vuetify.breakpoint.smAndDown">
          <v-card-title class="primary white--text">
            {{ form._id ? 'Formulario editar grupo' :
              'Formulario crear grupo' }}
            <v-spacer />
            <v-btn
              class="white--text"
              icon
              @click="dialogEdit=false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text class="my-3">
            <v-row dense>
              <v-col class="primary--text" cols="12" md="12">
                Información del grupo
              </v-col>
              <v-col cols="12" md="12">
                <text-field
                  v-model="form.name"
                  label="Nombre"
                  :rules="generalRules"
                />
              </v-col>
            </v-row>
            <v-row v-if="form._id" dense>
              <v-col cols="12">
                <v-checkbox
                  v-model="form.status"
                  label="Activo"
                />
              </v-col>
              <v-col class="text-caption" cols="12" md="6">
                ID: {{ form._id }}
              </v-col>
              <v-col class="text-caption text-md-right" cols="12" md="6">
                Modificado por: {{ form.updated_by }}
                {{ $moment(form.updated_at) }}
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" depressed type="submit">
              Guardar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
    <dialog-students-group
      v-model="dialogStudents"
      :groupid="groupid"
      :items="students"
    />
  </v-container>
</template>

<script>
import generalRules from '~/mixins/form-rules/general-rules'
import { groupUrl, studentUrl } from '~/mixins/routes'

export default {
  mixins: [generalRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      dialogStudents: false,
      students: [],
      form: {
        _id: '',
        name: '',
        status: ''
      },
      groupid: ''
    }
  },

  head () {
    return { title: 'Groups' }
  },

  computed: {
    headers () {
      return [
        { text: 'Grupo', value: 'name' },
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

  beforeMount () {
  },

  methods: {
    async getData () {
      try {
        const data = await this.$axios.$get(groupUrl)
        this.items = data.items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveGroup () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
              `${groupUrl}${this.form._id}`, this.form))
        } else {
          ({ message } = await this.$axios.$post(groupUrl, this.form))
        }

        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getGroup (item) {
      try {
        const group = await this.$axios.$get(`${groupUrl}${item._id}`)
        this.form = group
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getStudents (item) {
      try {
        this.students = (await this.$axios.$get(
          `${studentUrl}group?groupid=${item._id}`)).items
        this.groupid = item._id
        this.dialogStudents = true
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}
</script>
