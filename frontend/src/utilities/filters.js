import moment from 'moment'

export default {
  formatDate(value) {
    return moment(value).format('DD.MM.YYYY')
  },
  formatDatetime(value) {
    return moment(value).format('DD.MM.YYYY HH:mm')
  }
}
