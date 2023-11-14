<template lang="pug">
v-dialog(:value="dialog" max-width="700px"
:fullscreen="$vuetify.breakpoint.smAndDown" scrollable
@input="ev => $emit('input', ev)")
  v-card(flat :tile="$vuetify.breakpoint.smAndDown")
    v-card-title.primary.white--text Permisos
      v-spacer
      v-btn(color="primary" fab small depressed @click="$emit('input', false)")
        v-icon mdi-close
    v-card-text.mt-3
      v-data-table(:headers="headers" dense :items="permissions"
      :items-per-page="15" :server-items-length="total"
      :footer-props="{itemsPerPageOptions:[5, 7, 10]}")
        template(#top)
          v-text-field.mb-3(v-model="search" placeholder="Buscar"
          append-icon="mdi-magnify" filled dense hide-details)
        template(#item.read="{item}")
          div.d-flex.justify-center
            v-checkbox(v-model="item.read" hide-details dense
            @change="ev => updtatePermissions(item)")
        template(#item.create="{item}")
          div.d-flex.justify-center
            v-checkbox(v-model="item.create" hide-details dense
            @change="ev => updtatePermissions(item)")
        template(#item.update="{item}")
          div.d-flex.justify-center
            v-checkbox(v-model="item.update" hide-details dense
            @change="ev => updtatePermissions(item)")
        template(#item.delete="{item}")
          div.d-flex.justify-center
            v-checkbox(v-model="item.delete" hide-details dense
            @change="ev => updtatePermissions(item)")
</template>
<script>
import { permissionUrl } from '~/mixins/routes'

export default {
  name: 'PermissionsPage',

  model: {
    prop: 'dialog',
    event: 'input'
  },

  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    roleId: {
      type: String,
      default: ''
    },
    permissions: {
      type: Array,
      default: () => []
    },
    getRole: {
      type: Function,
      default: () => {}
    }
  },

  data () {
    return {
      total: -1,
      search: ''
    }
  },

  computed: {
    headers () {
      return [
        { text: 'Módulo', value: 'module' },
        { text: 'Leer', value: 'read', align: 'center' },
        { text: 'Crear', value: 'create', align: 'center' },
        { text: 'Editar', value: 'update', align: 'center' },
        { text: 'Eliminar', value: 'delete', align: 'center' }
      ]
    }
  },

  methods: {
    async updtatePermissions (item) {
      try {
        const { message } = await this.$axios.$patch(
            `${permissionUrl}${item._id}`, item)
        this.showSnackbar(message)
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}
</script>
