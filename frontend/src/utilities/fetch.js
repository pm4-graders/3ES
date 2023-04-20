import Type from 'union-type'

function T() {
  return true
}
const appUrl = import.meta.env.VITE_API_URL

// Defining a type for HTTP request status
const Request = Type({
  Nil: [], // Request hasn't been made yet
  Prepared: { params: T }, // Request parameters have been prepared
  Fetching: [], // Request is being fetched
  Failed: { errorMsg: String }, // Request failed
  Success: { data: T } // Request was successful
})

// Defining a type for web resources
const Webresource = Type({
  Nil: [], // Web resource doesn't exist
  Loading: [], // Web resource is being loaded
  Failed: { request: Request.Failed }, // Failed to load web resource
  Loaded: { entries: T } // Web resource was successfully loaded
})

Webresource.e = {
  Nil: 'Nil'
}

// Converting a Request type to a Webresource type
const requestToWebresource = (request) =>
  Request.case(
    {
      Failed: (request) => Webresource.FailedOf({ request }),
      Success: (entries) => {
        return Webresource.LoadedOf({ entries: entries })
      }
    },
    request
  )

// Adding a comp method to the Webresource type prototype
Webresource.prototype.comp = function (...comp) {
  for (let c of comp) {
    if (this._name === c) {
      return true
    }
  }
  return false
}

// Adding a comp method to the Request type prototype
Request.prototype.comp = function (...comp) {
  for (let c of comp) {
    if (this._name === c) {
      return true
    }
  }
  return false
}

// An asynchronous function for making a GET request to the API
const get = async (route, request = { value: Request.Nil }, options = {}) => {
  request.value = Request.Fetching

  options.method = 'GET'
  try {
    let res = await fetch(`${appUrl}${route}`, options)
    let data = await res.json()
    if (data.success) {

      request.value = Request.SuccessOf({ data: data.exams })
      return request.value
    }
    request.value = Request.FailedOf({errorMsg: "API Fehler"});
  } catch (e) {
    request.value = Request.FailedOf({ errorMsg: e.message })
  }
  return request.value
}

// An asynchronous function for making a POST request to the API
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
    request.value = Request.FailedOf({ errorMsg: e.message })
  }
  return request.value
}

export { get, post, Webresource, Request, requestToWebresource }
