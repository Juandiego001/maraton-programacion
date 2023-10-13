export const state = () => ({
  username: '',
  name: '',
  lastname: '',
  document: '',
  photo: '',
  epoch: 0
})

export const mutations = {
  photo (state, value) {
    state.photo = value
  },
  updateSession (state, { username, name, lastname, document, epoch }) {
    state.username = username
    state.name = name
    state.lastname = lastname
    state.document = document
    state.epoch = epoch
  }
}
