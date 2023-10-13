import Vue from 'vue'
import globalMixin from '~/mixins/global'

if (!Vue.__global_mixin__) {
  Vue.__global_mixin__ = true
  Vue.mixin(globalMixin)
}

export default (_, inject) => {
  inject('clone', obj => JSON.parse(JSON.stringify(obj)))
}
