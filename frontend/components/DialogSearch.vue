<template lang="pug">
v-dialog(:value="dialog" max-width="600px" @input="ev => $emit('input', ev)"
:fullscreen="$vuetify.breakpoint.smAndDown" scrollable)
  v-form(@submit.prevent="doSearch(search)")
    v-card(flat :tile="$vuetify.breakpoint.smAndDown")
      v-card-title.primary.white--text Búsqueda general
        v-spacer
        v-btn.primary(fab small depressed @click="dialogSearch=false")
          v-icon mdi-close
      v-card-text.mt-3
        v-row
          v-col(cols="12")
            v-text-field(prepend-icon="mdi-magnify" label="Buscar"
            filled single-line hide-details v-model="search" autofocus dense
            clearable @click:clear="resetSearch")
      v-card-actions
        v-spacer
        v-btn(color="primary" depressed type="submit") Buscar
</template>
<script>
export default {
  name: 'SearchPage',

  model: {
    prop: 'dialog',
    event: 'input'
  },
  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    doSearch: {
      type: Function,
      default: null
    }
  },
  data () {
    return {
      search: ''
    }
  },

  methods: {
    resetSearch () {
      this.search = ''
      this.doSearch()
    }
  }
}
</script>
