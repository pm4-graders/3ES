import { createServer, Model } from 'miragejs'
import moment from 'moment'
import _ from 'lodash'

export function makeServer({ environment = 'development' } = {}) {
  let server = createServer({
    environment,

    models: {
      result: Model
    },

    seeds(server) {
      server.db.loadData({
        results: [
          { title: 'Dunkirk', date: moment().format(), id: _.random(1000) },
          { title: 'Dunkirk', date: moment().format(), id: _.random(1000) },
          { title: 'Dunkirk', date: moment().format(), id: _.random(1000) },
          { title: 'Dunkirk', date: moment().format(), id: _.random(1000) }
        ]
      })
    },

    routes() {
      this.namespace = 'api'

      this.get(
        '/results',
        (schema) => {
          return schema.db.results
        },
        { timing: 1000 }
      )
      this.post('/upload', (schema) => {
        schema.db.results.insert({ title: 'peeeter', date: moment().format(), id: _.random(1000) })
        return {
          success: true
        }
          , { timing: 1000 }
      })
    }
  })

  const dbData = localStorage.getItem('db')

  if (dbData) {
    // https://miragejs.com/api/classes/db/#load-data
    server.db.loadData(JSON.parse(dbData))
  }
  // https://miragejs.com/api/classes/server/#pretender
  server.pretender.handledRequest = function(verb) {
    if (verb.toLowerCase() !== 'get' && verb.toLowerCase() !== 'head') {
      localStorage.setItem('db', JSON.stringify(server.db.dump()))
    }
  }
  return server
}
