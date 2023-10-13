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
          @click="getTeacher(item)"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
        <v-btn
          v-if="item.status === 'PENDING'"
          class="mr-2"
          depressed
          icon
          @click="resendLink(item)"
        >
          <v-icon>mdi-email-fast</v-icon>
        </v-btn>
      </template>
    </v-data-table>
    <v-dialog
      v-model="dialogEdit"
      max-width="600px"
      :fullscreen="$vuetify.breakpoint.smAndDown"
      scrollable
    >
      <v-form ref="form" @submit.prevent="saveTeacher">
        <v-card flat :tile="$vuetify.breakpoint.smAndDown">
          <v-card-title class="primary white--text">
            {{ form._id ? 'Formulario editar profesor' :
              'Formulario crear profesor' }}
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
                Información del profesor
              </v-col>
              <v-col cols="12" md="6">
                <text-field
                  v-model="form.name"
                  label="Nombre"
                  :rules="generalRules"
                />
              </v-col>
              <v-col cols="12" md="6">
                <text-field
                  v-model="form.lastname"
                  label="Apellido"
                  :rules="generalRules"
                />
              </v-col>
              <v-col cols="12" md="6">
                <text-field
                  v-model="form.document"
                  label="Cédula"
                  :rules="generalRules"
                />
              </v-col>
              <v-col cols="12" md="6">
                <text-field
                  v-model="form.username"
                  label="Usuario"
                  :rules="generalRules"
                />
              </v-col>
              <v-col cols="12" md="12">
                <text-field
                  v-model="form.email"
                  label="Correo"
                  :rules="generalRules"
                />
              </v-col>
              <v-col cols="12" md="12">
                <text-field-password
                  v-model="form.password"
                  label="Contraseña"
                  :rules="passwordEmptyRules"
                />
              </v-col>
              <v-col cols="12" md="12">
                <v-file-input
                  v-model="photo"
                  filled
                  dense
                  prepend-inner-icon="mdi-paperclip"
                  :prepend-icon="null"
                  label="Foto"
                  hide-details="auto"
                />
              </v-col>
            </v-row>
            <v-row v-if="form._id" dense>
              <v-col cols="12">
                <v-select
                  v-model="form.status"
                  label="Estado"
                  filled
                  dense
                  hide-details="auto"
                  :items="userStatus"
                  item-value="value"
                  item-text="text"
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
  </v-container>
</template>

<script>
import generalRules from '~/mixins/form-rules/general-rules'
import passwordEmptyRules from '~/mixins/form-rules/passwordsEmpty'
import { resetPasswordUrl, teacherUrl } from '~/mixins/routes'

export default {
  mixins: [generalRules, passwordEmptyRules],

  data () {
    return {
      options: {},
      total: -1,
      items: [],
      form: {
        _id: '',
        name: '',
        lastname: '',
        document: '',
        username: '',
        email: '',
        password: '',
        status: ''
      },
      photo: null
    }
  },

  head () {
    return { title: 'Teachers' }
  },

  computed: {
    headers () {
      return [
        { text: 'Profesor', value: 'fullname' },
        { text: 'Usuario', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Estado', value: 'status' },
        { text: 'Opciones', value: 'options' }
      ]
    },
    userStatus () {
      return [
        {
          text: 'Activo',
          value: 'ACTIVE'
        },
        {
          text: 'Pendiente de activación',
          value: 'PENDING',
          disabled: true
        },
        {
          text: 'Inactivo',
          value: 'INACTIVE'
        }
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
        const data = await this.$axios.$get(teacherUrl)
        this.items = data.items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async saveTeacher () {
      try {
        if (!this.$refs.form.validate()) { return }
        let message
        if (this.form._id) {
          ({ message } = await this.$axios.$patch(
            `${teacherUrl}${this.form._id}`, this.form))
        } else {
          ({ message } = await this.$axios.$post(teacherUrl, this.form))
        }

        this.getData()
        this.dialogEdit = false
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async getTeacher (item) {
      try {
        const teacher = await this.$axios.$get(`${teacherUrl}${item._id}`)
        this.form = teacher
        this.dialogEdit = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async resendLink (item) {
      try {
        const { message } = await this.$axios.$post(resetPasswordUrl,
          { email: item.email })
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}
</script>
