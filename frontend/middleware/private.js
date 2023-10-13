// import { AbilityBuilder, Ability } from '@casl/ability'

export default async function ({ redirect, $axios, $ability, app, store }) {
  try {
    const epoch = Math.floor(Date.now() / 1000)
    const oldEpoch = store.state.session.epoch

    if (epoch - oldEpoch > 10) {
      const user = await $axios.$get('/api/account/profile')
      if (!user.username) {
        redirect('/account/login/')
      }
      store.commit('session/updateSession', { epoch, ...user })
      $ability.update(user.abilities)
    }
  } catch (err) {
    redirect('/account/login/')
  }
}
