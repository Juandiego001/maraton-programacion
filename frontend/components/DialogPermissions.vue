<template>
  <v-dialog
    :value="dialog"
    max-width="700px"
    :fullscreen="$vuetify.breakpoint.smAndDown"
    scrollable
    @input="ev => $emit('input', ev)"
  >
    <v-card flat :tile="$vuetify.breakpoint.smAndDown">
      <v-card-title class="primary--text">
        Permisos
        <v-spacer />
        <v-btn fab small depressed @click="$emit('input', false)">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-card-text>
          <v-data-table
            :headers="headers"
            dense
            :items="items"
            :items-per-page="15"
            :server-items-length="total"
            :options.sync="options"
            :footer-props="{itemsPerPageOptions:[5,10,15,20]}"
          >
            <template #top>
              <v-text-field
                v-model="search"
                placeholder="Buscar"
                append-icon="mdi-magnify"
                filled
                dense
                hide-details
              />
            </template>
            <template #[`item.read`]="{item}">
              <div class="d-flex justify-center">
                <v-checkbox
                  v-model="item.read"
                  hide-details
                  dense
                  :disabled="isDisabled(item, 'read')"
                  @change="ev => updtatePermissions(item)"
                />
              </div>
            </template>
            <template #[`item.create`]="{item}">
              <div class="d-flex justify-center">
                <v-checkbox
                  v-model="item.create"
                  hide-details
                  dense
                  :disabled="isDisabled(item, 'create')"
                  @change="ev => updtatePermissions(item)"
                />
              </div>
            </template>
            <template #[`item.update`]="{item}">
              <div class="d-flex justify-center">
                <v-checkbox
                  v-model="item.update"
                  hide-details
                  dense
                  :disabled="isDisabled(item, 'update')"
                  @change="ev => updtatePermissions(item)"
                />
              </div>
            </template>
            <template #[`item.delete`]="{item}">
              <div class="d-flex justify-center">
                <v-checkbox
                  v-model="item.delete"
                  hide-details
                  dense
                  :disabled="isDisabled(item, 'delete')"
                  @change="ev => updtatePermissions(item)"
                />
              </div>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card-title>
    </v-card>
  </v-dialog>
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
    profileid: {
      type: String,
      default: ''
    }
  },

  data () {
    return {
      items: [],
      options: {},
      total: 0,
      search: ''
    }
  },

  computed: {
    headers () {
      return [
        { text: 'Módulo', value: 'module.name' },
        { text: 'Leer', value: 'read', align: 'center' },
        { text: 'Crear', value: 'create', align: 'center' },
        { text: 'Editar', value: 'update', align: 'center' }
      ]
    }
  },

  watch: {
    options: { handler () { this.getData() }, deep: true },
    dialog (value) {
      if (value) {
        this.getData()
      } else {
        this.options.page = 1
        this.permissions = []
      }
    },
    search () {
      this.options.page = 1
      this.getData()
    }
  },

  methods: {
    isDisabled (item, action) {
      const slugs = ['config-modules', 'config-cities', 'config-logs']
      const slugsPemissionDelete = ['project-job-changes', 'project-jobs', 'project-projects']
      const slugsPermissions = ['config-groups', 'config-permissions']
      const disabled = (item.group.code === 'admin_company' &&
        slugsPermissions.includes(item.module.slug)) ||
        (slugs.includes(item.module.slug) && action !== 'read') ||
        (!slugsPemissionDelete.includes(item.module.slug) &&
        action === 'delete')
      return disabled
    },
    async getData () {
      try {
        this.items = (await this.$axios.$get(
          `${permissionUrl}${this.profileid}`)).items
      } catch (err) {
        this.showSnackbar(err)
      }
    },
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
