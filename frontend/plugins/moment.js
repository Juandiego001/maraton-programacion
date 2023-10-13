export default ({ $moment }, inject) => {
  inject('moment', value => $moment(value).tz('America/Bogota')
    .format('YYYY-MM-DD HH:mm'))
}
