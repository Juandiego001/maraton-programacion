export default {
  computed: {
    fileLinkRules () {
      return [
        v => !!this.form.real_name || !!this.file || !!this.form.link ||
          'Debe agregar un archivo o un link'
      ]
    }
  }
}
