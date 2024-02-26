<template lang="pug">
v-container
  v-row
    v-col(v-if="canRead('Temáticas')" cols="2" sm="3" md="2")
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
    v-col(v-if="canRead('Estructuras')" cols="2" sm="4" md="2")
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
    v-col(v-if="canRead('Respuestas')" cols="2" sm="4" md="2")
      v-card(nuxt :to="'/administration/responses'" hover)
        v-card-title.primary.white--text
          div
            span Respuestas
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-message-badge
    v-col(v-if="canRead('Lenguajes')" cols="2" sm="3" md="2")
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
    v-col(v-if="canRead('Dificultades')" cols="2" sm="4" md="2")
      v-card(nuxt :to="'/administration/difficulties'" hover)
        v-card-title.primary.white--text
          div
            span Dificultades
            p.caption Administración
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-clock-fast
  v-row
    v-col(v-if="canRead('Roles')" cols="2" sm="3" md="2")
      v-card(nuxt :to="'/user/roles'" hover)
        v-card-title.primary.white--text
          div
            span Roles
            p.caption Usuario
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-shield-account-variant-outline
    v-col(v-if="canRead('Usuarios')" cols="2" sm="3" md="2")
      v-card(nuxt :to="'/user/users'" hover)
        v-card-title.primary.white--text
          div
            span Usuarios
            p.caption Usuario
        v-card-text
        v-card-actions
          v-spacer
          v-btn(icon)
            v-icon.primary--text mdi-account
  v-row
    v-col(v-if="canRead('Competencias')" cols="3" sm="4" md="3")
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
    v-col(v-if="canRead('Retos')" cols="2" sm="3" md="2")
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
    v-col(v-if="canRead('Soluciones')" cols="2" sm="3" md="2")
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
    v-col(v-if="canRead('Materiales')" cols="2" sm="3" md="2")
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
    canRead (slug) {
      return this.$ability.can('read', slug)
    }
  }
}

</script>

<style scoped>
</style>
