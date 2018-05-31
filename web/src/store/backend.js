import axios from 'axios'

let port = ''

if (process.env.NODE_ENV !== 'production') {
  port = ':5000'
}

const current_domain = window.location.protocol+'//'+window.location.host.split(':')[0]+port

let $backend = axios.create({
  baseURL: current_domain+'/api/',
  timeout: 10000,
  headers: {'Content-Type': 'application/json'}
})

export default {
  setToken (token) {
    $backend.defaults.headers['Authorization'] = 'Bearer ' + token
  },
  loginUser (auth) {
    return $backend.get(`users/${auth['username'] || ''}`, {auth: auth})
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchCiphers (raw) {
    let params = {params: {'categorized': true, 'categories': ['stream', 'block', 'transition']}}
    if (raw) {
      params = {}
    }
    return $backend.get(`ciphers`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchCipher (id) {
    return $backend.get(`ciphers/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchEds (raw) {
    let params = {params: {'categorized': true, 'categories': ['stream', 'block', 'transition']}}
    if (raw) {
      params = {}
    }
    return $backend.get(`eds`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchDs (id) {
    return $backend.get(`eds/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  moduleSend (id, data) {
    return $backend.post(`modules/${id}`, data)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchArticles (raw) {
    let params = {params: {'categorized': true}}
    if (raw) {
      params = {}
    }
    return $backend.get(`articles`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchArticle (id) {
    return $backend.get(`articles/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  saveArticle (id, data) {
    let method = $backend.post
    if (id !== undefined && id !== '') {
      method = $backend.put
    }
    return method(`articles/${id}`, data)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  deleteArticle (id) {
    return $backend.delete(`articles/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchUsers (raw) {
    let params = {params: {'categorized': true}}
    if (raw) {
      params = {}
    }
    return $backend.get(`users`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchUser (id) {
    return $backend.get(`users/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  saveUser (id, data) {
    let method = $backend.post
    if (id !== undefined && id !== '') {
      method = $backend.put
    }
    return method(`users/${id}`, data)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  deleteUser (id) {
    return $backend.delete(`users/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestsEdit (raw) {
    let params = {params: {'categorized': true}}
    if (raw) {
      params = {}
    }
    return $backend.get(`tests/edit`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestEdit (id) {
    return $backend.get(`tests/edit/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  saveTest (id, data) {
    let method = $backend.post
    if (id !== undefined && id !== '') {
      method = $backend.put
    }
    return method(`tests/edit/${id}`, data)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  deleteTest (id) {
    return $backend.delete(`tests/edit/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestsRun (raw) {
    let params = {params: {'categorized': true}}
    if (raw) {
      params = {}
    }
    return $backend.get(`tests/run`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestRun (id) {
    return $backend.get(`tests/run/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestItemRun (test, item) {
    return $backend.get(`tests/run/${test}/${item}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  saveTestItemResult (test, item, data) {
    return $backend.post(`tests/run/${test}/${item}`, data)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestsResult (raw) {
    let params = {params: {'categorized': true}}
    if (raw) {
      params = {}
    }
    return $backend.get(`tests/result`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestResult (id) {
    return $backend.get(`tests/result/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestsResults (raw) {
    let params = {params: {'categorized': true}}
    if (raw) {
      params = {}
    }
    return $backend.get(`tests/results`, params)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  },
  fetchTestResults (id) {
    return $backend.get(`tests/results/${id}`)
      .then(response => ({'data': response.data, 'error': response.error, 'token': response.headers['token']}))
  }
}
