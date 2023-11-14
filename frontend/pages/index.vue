<template lang="pug">
v-container
  v-row
    v-col(cols="2")
      v-card(nuxt :to="'/administration/roles'" hover)
        v-card-title.primary.white--text
          div
            span Roles
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-shield-account-variant-outline
    v-col(cols="2")
      v-card(nuxt :to="'/administration/users'" hover)
        v-card-title.primary.white--text
          div
            span Usuarios
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-account
    v-col(cols="2")
      v-card(nuxt :to="'/administration/topics'" hover)
        v-card-title.primary.white--text
          div
            span Temáticas
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-tag-multiple-outline
    v-col(cols="2")
      v-card(nuxt :to="'/administration/structures'" hover)
        v-card-title.primary.white--text
          div
            span Estructuras
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-lan
    v-col(cols="2")
      v-card(nuxt :to="'/administration/languages'" hover)
        v-card-title.primary.white--text
          div
            span Lenguajes
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-codepen
    v-col(cols="3")
      v-card(nuxt :to="'/administration/notifications'" hover)
        v-card-title.primary.white--text
          div
            span Notificaciones
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-bell-outline
    v-col(cols="3")
      v-card(nuxt :to="'/marathon/contests'" hover)
        v-card-title.primary.white--text
          div
            span Competencias
            p.caption Maratón
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-medal-outline
    v-col(cols="2")
      v-card(nuxt :to="'/marathon/challenges'" hover)
        v-card-title.persian.white--text
          div
            span Retos
            p.caption Maratón
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.persian--text mdi-text-box-outline
    v-col(cols="2")
      v-card(nuxt :to="'/marathon/solutions'" hover)
        v-card-title.saffron.white--text
          div
            span Soluciones
            p.caption Maratón
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.saffron--text mdi-code-tags
    v-col(cols="2")
      v-card(nuxt :to="'/marathon/materials'" hover)
        v-card-title.burnt.white--text
          div
            span Materiales
            p.caption Maratón
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.burnt--text mdi-book
</template>

<script>
export default {
  name: 'IndexPage',
  data () {
    return {
      user: '',
      password: '',
      count: 0
    }
  },

  methods: {
    login () {
    }
  }
}

</script>

<style scoped>
</style>
