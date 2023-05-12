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
  Failed: { errorMsgList: Array }, // Request failed
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
const get = async (route, request = null, options = {}, entriesKey = 'entries') => {
  if (!request) {
    request = { value: Request.Nil }
  }
  request.value = Request.Fetching

  options.method = 'GET'
  try {
    let res = await fetch(`${appUrl}${route}`, options)
    let data = await res.json()
    if (data.success) {
      request.value = Request.SuccessOf({ data: data[entriesKey] })
      return request.value
    }
    request.value = Request.FailedOf({ errorMsgList: ['API Fehler'] })
  } catch (e) {
    request.value = Request.FailedOf({ errorMsgList: [e.message] })
  }
  return request.value
}

// An asynchronous function for making a POST request to the API
const post = async (route, request = { value: Request.Nil }, options = {}, type = 'json') => {
  options.method = 'POST'

  if (type === 'json') {
    options.body = JSON.stringify(request.value.params)
    options.headers = {
      'Content-Type': 'application/json'
    }
  } else if (type === 'multipart') {
    const formData = new FormData()
    for (const name in request.value.params) {
      console.log(name)
      console.log(request.value.params[name])
      formData.append(name, request.value.params[name])
    }
    options.body = formData
  }
  // let formdata = new FormData()
  // for (let key in request.value.params) {
  //   formdata.append(key, request.value.params[key])
  // }
  // options.body = formdata
  request.value = Request.Fetching
  try {
    let res = await fetch(`${appUrl}${route}`, options)
    let data = await res.json()
    if (!data.success) {
      request.value = Request.FailedOf({ errorMsgList: data.message })
      return request.value
    }
    request.value = Request.SuccessOf({ data })
  } catch (e) {
    request.value = Request.FailedOf({ errorMsgList: [e.message] })
  }
  return request.value
}

export { get, post, Webresource, Request, requestToWebresource }
