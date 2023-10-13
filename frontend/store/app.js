export const state = () => ({
  moduleSlug: '',
  title: '',
  dialogEdit: false,
  dialogSearch: false
})

export const mutations = {
  moduleSlug (state, value) {
    state.moduleSlug = value
  },
  setDialogEdit (state, value) {
    state.dialogEdit = value
  },
  setDialogSearch (state, value) {
    state.dialogSearch = value
  },
  title (state, value) {
    state.title = value
  }
}
