<template lang="pug">
v-app
  v-navigation-drawer(v-model="drawer" fixed app dark class="primary")
    v-row(class="py-4")
      v-col(class="text-center pb-0" cols="12" md="12")
        v-avatar
          template(v-if="session.photo")
            v-img(:src="photoUrl" alt="Avatar")
          template(v-else)
            v-icon(large) mdi-account-circle-outline
      v-col(class="white--text text-center pb-0" cols="12" md="12")
        p(class="mb-0") {{ session.name }} {{ session.lastname }}
      v-col(class="text-center pb-0" cols="6")
        v-btn(class="primary white--text" @click="showProfile") Perfil
      v-col(class="text-center" cols="6")
        v-btn(class="error white--text" @click="logout")
          v-icon(class="white--text") mdi-logout
          | Salir
    v-list
      v-list-item(link to="/")
        v-list-item-icon
          v-icon mdi-home
        v-list-item-content
          v-list-item-title Inicio
      v-list-group(
        v-for="(item, i) in appMenu"
        :key="item.text + '' + i"
        active-class="accent--text")
        template(#activator)
          v-list-item-icon
            v-icon {{ item.icon }}
          v-list-item-content
            v-list-item-title {{ item.title }}
        v-list-item(v-for="(option, j) in item.items"
        :key="option.title + '' + j" :to="option.to")
          v-list-item-icon
            v-icon(class="white--text") {{ option.icon }}
          v-list-item-title(class="white--text") {{ option.title }}
  v-app-bar(app dark class="primary")
    v-app-bar-nav-icon( @click.stop="drawer = !drawer")
    v-toolbar-title
      NuxtLink(class="white--text text-decoration-none" to="/")
      | Maratón UAO
    v-spacer
    v-btn(v-if="canSearch" icon @click="dialogSearch=true")
      v-icon mdi-magnify
    v-btn(icon)
      v-icon mdi-message-text-outline
    v-btn(icon)
      v-icon mdi-bell-outline
    v-btn(v-if="canCreate" icon @click="dialogEdit=true")
      v-icon mdi-plus
  v-main
    Nuxt

  v-snackbar(v-model="snackbar" multi-line
  :color="$store.state.snackbar.type") {{ $store.state.snackbar.text }}
    template(#action)
      v-btn(icon @click="snackbar=false")
        v-icon mdi-close

  dialog-profile(v-model="dialogProfile" :profile="profile")
</template>

<script>
import { mapMutations } from 'vuex'
import menu from './menu'
import { photoUrl, accountProfileUrl, logoutUrl } from '~/mixins/routes'

export default {
  name: 'DefaultLayout',
  middleware: 'private',
  data () {
    return {
      dialogProfile: false,
      profile: {},
      drawer: false,
      appMenu: []
    }
  },

  computed: {
    session () { return { ...this.$store.state.session } },
    snackbar: {
      get () { return this.$store.state.snackbar.snackbar },
      ...mapMutations({ set: 'snackbar/snackbar' })
    },
    photoUrl () { return `${photoUrl}/${this.session.photoUrl}` }
  },

  beforeMount () {
    this.getMenu()
  },

  methods: {
    getMenu () {
      try {
        const options = []
        for (const option of this.$clone(menu)) {
          option.e = this.session.epoch
          option.items = option.items.filter(subitem =>
            this.$ability.can('read', subitem.title))
          if (option.items.length) { options.push(option) }
        }
        this.appMenu = options
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async showProfile () {
      try {
        const data = await this.$axios.$get(accountProfileUrl)
        this.profile = data
        this.dialogProfile = true
      } catch (err) {
        this.showSnackbar(err)
      }
    },
    async logout () {
      try {
        const { message } = await this.$axios.$get(logoutUrl)
        this.showSnackbar(message)
        this.$router.push('/account/login')
      } catch (err) {
        this.showSnackbar(err)
      }
    }
  }
}
</script>

<style>
html { overflow-y: auto !important }
</style>
