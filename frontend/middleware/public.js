export default async function ({ redirect, $axios, app }) {
  try {
    const me = await $axios.$get('/api/account/profile')
    if (me.username) {
      app.router.push('/')
    }
  } catch (err) {
  }
}
