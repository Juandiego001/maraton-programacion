<template lang="pug">
v-text-field(:value="data" :label="label" filled dense type="text"
hide-details="auto" :placeholder="placeholder" :readonly="readonly"
:rules="rules" @input="ev => $emit('input', ev)")
</template>

<script>
export default {

  model: {
    prop: 'data',
    event: 'input'
  },

  props: {
    data: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: false
    },
    rules: {
      type: Array,
      default: new Array(0)
    }
  },

  data () {
    return {
    }
  }
}
</script>
