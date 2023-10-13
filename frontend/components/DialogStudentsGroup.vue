<template>
  <v-dialog
    :value="dialog"
    max-width="600px"
    scrollable
    :fullscreen="$vuetify.breakpoint.smAndDown"
    @input="ev => $emit('input', ev)"
  >
    <v-card flat :tile="$vuetify.breakpoint.smAndDown" scrollable>
      <v-card-title class="primary white--text">
        Estudiantes del grupo
        <v-spacer />
        <v-btn
          fab
          small
          depressed
          color="primary"
          @click="$emit('input', false)"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="py-3">
        <v-data-table
          :headers="headers"
          :items="items"
          :items-per-page="15"
          :server-items-length="total"
          :options.sync="options"
          :footer-props="{itemsPerPageOptions:[5,10,15,20]}"
        >
          <template #top>
            <v-row align="center" dense>
              <v-col cols="10">
                <v-text-field
                  v-model="search"
                  placeholder="Buscar"
                  append-icon="mdi-magnify"
                  filled
                  dense
                  hide-details
                  class="pb-2"
                />
              </v-col>
              <v-col class="text-center" cols="2">
                <v-btn
                  filled
                  depressed
                  icon
                  class="primary white--text"
                  @click="showAddStudent"
                >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
    <dialog-add-students-group
      v-model="dialogAddStudents"
      :groupid="groupid"
      :items="students"
    />
  </v-dialog>
</template>

<script>
import { studentUrl } from '~/mixins/routes'

export default {

  model: {
    prop: 'dialog',
    event: 'input'
  },

  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    groupid: {
      type: String,
      default: ''
    },
    items: {
      type: Array,
      default: new Array(0)
    }
  },

  data () {
    return {
      options: {},
      students: [],
      total: -1,
      search: '',
      dialogAddStudents: false
    }
  },

  computed: {
    headers () {
      return [
        { text: 'Nombre', value: 'fullname' },
        { text: 'Usuario', value: 'username' },
        { text: 'Opciones' }
      ]
    }
  },

  methods: {
    async showAddStudent () {
      try {
        this.students = (await this.$axios.$get(
            `${studentUrl}group?`)).items
        this.dialogAddStudents = true
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}
</script>
