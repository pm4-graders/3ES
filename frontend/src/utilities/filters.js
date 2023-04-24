import moment from 'moment'

export default {
  formatDate(value) {
    return moment(value).format('DD.MM.YYYY')
  }
}
