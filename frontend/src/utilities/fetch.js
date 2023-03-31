import Type from 'union-type'

function T() {
  return true
}
const appUrl = import.meta.env.VITE_API_URL
const Request = Type({
  Nil: [],
  Prepared: { params: T },
  Fetching: [],
  Failed: { errorMsg: String },
  Success: { data: T }
})
const Webresource = Type({
  Nil: [],
  Loading: [],
  Failed: { request: Request.Failed },
  Loaded: { entries: T }
})

Webresource.e = {
  Nil: 'Nil'
}

const requestToWebresource = (request, resource) =>
  Request.case(
    {
      Failed: (request) => Webresource.FailedOf({ request }),
      Success: (entries) => {
        return Webresource.LoadedOf({ entries: entries })
      }
    },
    request
  )

Webresource.prototype.comp = function (...comp) {
  for (let c of comp) {
    if (this._name === c) {
      return true
    }
  }
  return false
}
Request.prototype.comp = function (...comp) {
  for (let c of comp) {
    if (this._name === c) {
      return true
    }
  }
  return false
}

const get = async (route, request = { value: Request.Nil }, options = {}) => {
  request.value = Request.Fetching

  options.method = 'GET'
  try {
    let res = await fetch(`${appUrl}${route}`, options)
    let data = await res.json()
    request.value = Request.SuccessOf({ data })
  } catch (e) {
    request.value = Request.FailedOf({ errorMsg: e.message })
  }
  return request.value
}

const post = async (route, request = { value: Request.Nil }, options = {}) => {
  options.method = 'POST'
  //options.body = JSON.stringify(data)
  let formdata = new FormData()
  for (let key in request.value.params) {
    formdata.append(key, request.value.params[key])
  }
  options.body = formdata
  request.value = Request.Fetching
  try {
    let res = await fetch(`${appUrl}${route}`, options)
    let data = await res.json()
    request.value = Request.SuccessOf({ data })
  } catch (e) {
    console.log(e)
    request.value = Request.FailedOf({ errorMsg: e.message})
  }
  return request.value
}

export { get, post, Webresource, Request, requestToWebresource }
