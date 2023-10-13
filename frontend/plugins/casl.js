import { Ability } from '@casl/ability'

// Setup casl https://casl.js.org/v6/en/package/casl-vue
export default (_, inject) => {
  inject('ability', new Ability([]))
}
