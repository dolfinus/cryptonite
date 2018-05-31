import backend from './backend'
import Cookies from 'js-cookie'

export default {

  async loginUser (context, auth) {
    backend.setToken('')
    let response = await backend.loginUser(auth)
    Object.assign(response.data, {'token': response.token})
    context.commit('setCurrentUser', response.data)
  },

  logoutUser (context) {
    Object.keys(Cookies.get()).forEach((cookie) => Cookies.remove(cookie))
    context.commit('resetState', {})
    backend.setToken('')
  },

  async fetchCurrentUser (context) {
    let response = await backend.fetchUser(context.getters.getCurrentUser.name)
    Object.assign(response.data, {'token': response.token})
    context.commit('setCurrentUser', response.data)
  },

  toggleNavbarMenu (context) {
    context.commit('setNavbarMenu', !context.getters.getNavbarMenu)
  },

  setNavbarMenu (context, value) {
    context.commit('setNavbarMenu', value)
  },

  toggleNavbarModules (context) {
    context.commit('setNavbarModules', !context.getters.getNavbarModules)
  },

  setNavbarModules (context, value) {
    context.commit('setNavbarModules', value)
  },

  toggleNavbarTests (context) {
    context.commit('setNavbarTests', !context.getters.getNavbarTests)
  },

  setNavbarTests (context, value) {
    context.commit('setNavbarTests', value)
  },

  toggleNavbarUser (context) {
    context.commit('setNavbarUser', !context.getters.getNavbarUser)
  },

  setNavbarUser (context, value) {
    context.commit('setNavbarUser', value)
  },

  async fetchCiphers (context, preload) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setCiphersLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchCiphers()
    context.commit('setCiphers', response.data)
    context.commit('setCurrentToken', response.token)
    if (preload) {
      let response = await backend.fetchCiphers(true)
      for (let i in response.data) {
        let item = response.data[i]
        context.dispatch('fetchCipher', item)
      }
    }
  },

  async fetchCipher (context, id) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setCipherLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchCipher(id)
    context.commit('setCipher', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchEds (context, preload) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setEdsLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchEds()
    context.commit('setEds', response.data)
    context.commit('setCurrentToken', response.token)
    if (preload) {
      let response = await backend.fetchEds(true)
      for (let i in response.data) {
        let item = response.data[i]
        context.dispatch('fetchDs', item)
      }
    }
  },

  async fetchDs (context, id) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchDs(id)
    context.commit('setDs', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async moduleSend (context, data) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    let dat    = data[1]
    let method = dat.action
    let params = {}
    Object.keys(dat).forEach((key) => {
      let value = dat[key]
      let [name, type] = key.split('_')
      if (type === 'init' || type === method || type === '' || type === undefined) {
        params[name] = dat[key]
      }
    })
    backend.setToken(context.getters.getToken)
    let response = await backend.moduleSend(data[0], params)
    context.commit('setModuleResult', [data, response.data])
    context.commit('setCurrentToken', response.token)
  },

  fetchInstruments (context) {
    context.commit('setInstruments', context.getters.getInstruments.categories)
  },

  async fetchArticles (context) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setArticlesLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchArticles()
    context.commit('setArticles', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchArticle (context, id) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setArticleLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchArticle(id)
    context.commit('setArticle', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async saveArticle (context, data) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    backend.setToken(context.getters.getToken)
    let response = await backend.saveArticle(data[0], data[1])
    context.commit('setCurrentToken', response.token)
    context.dispatch('fetchArticles')
  },

  async deleteArticle (context, id) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    backend.setToken(context.getters.getToken)
    let response = await backend.deleteArticle(id)
    context.commit('setCurrentToken', response.token)
    context.dispatch('fetchArticles')
  },

  async fetchUsers (context) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    context.commit('setUsersLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchUsers()
    context.commit('setUsers', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchUser (context, id) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    if (!context.getters.isCurrentAdmin && context.getters.getCurrentUser.name !== id) {
      return
    }
    context.commit('setUserLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchUser(id)
    context.commit('setUser', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async saveUser (context, data) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    if (!context.getters.isCurrentAdmin && context.getters.getCurrentUser.name !== data[0]) {
      return
    }
    backend.setToken(context.getters.getToken)
    let response = await backend.saveUser(data[0], data[1])
    context.commit('setCurrentToken', response.token)
    context.dispatch('fetchUsers')
  },

  async deleteUser (context, id) {
    if (!context.getters.isCurrentAdmin || context.getters.getCurrentUser.name === id) {
      return
    }
    backend.setToken(context.getters.getToken)
    let response = await backend.deleteUser(id)
    context.commit('setCurrentToken', response.token)
    context.dispatch('fetchUsers')
  },

  async fetchTestsEdit (context) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    context.commit('setTestsEditLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestsEdit()
    context.commit('setTestsEdit', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchTestEdit (context, id) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    context.commit('setTestEditLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestEdit(id)
    context.commit('setTestEdit', response.data)
    context.commit('setCurrentToken', response.token)
  },

  addTestEditItem (context, data) {
    let id      = data[0]
    let content = data[1]
    context.commit('addTestEditItem', id, content)
  },

  removeTestEditItem (context, id) {
    context.commit('removeTestEditItem', id)
  },

  async saveTest (context, data) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    backend.setToken(context.getters.getToken)
    let response = await backend.saveTest(data[0], data[1])
    context.commit('setCurrentToken', response.token)
    context.dispatch('fetchTestsEdit')
  },

  async deleteTest (context, id) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    backend.setToken(context.getters.getToken)
    let response = await backend.deleteTest(id)
    context.commit('setCurrentToken', response.token)
    context.dispatch('fetchTestsEdit')
  },

  async fetchTestsRun (context) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setTestsRunLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestsRun()
    context.commit('setTestsRun', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchTestRun (context, id) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setTestRunLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestRun(id)
    context.commit('setTestRun', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchTestItemRun (context, data) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setTestRunLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestItemRun(data[0], data[1])
    context.commit('setTestRunItem', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async saveTestItemResult (context, data) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    let reload = this.fetchTestRun
    backend.setToken(context.getters.getToken)
    let response = await backend.saveTestItemResult(data[0], data[1], data[2])
    context.commit('setCurrentToken', response.token)
  },

  async fetchTestsResult (context) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setTestsResultLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestsResult()
    context.commit('setTestsResult', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchTestResult (context, id) {
    if (!(context.getters.isLoggedIn)) {
      return
    }
    context.commit('setTestResultLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestResult(id)
    context.commit('setTestResult', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchTestsResults (context) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    context.commit('setTestsResultsLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestsResults()
    context.commit('setTestsResults', response.data)
    context.commit('setCurrentToken', response.token)
  },

  async fetchTestResults (context, id) {
    if (!(context.getters.isCurrentAdmin)) {
      return
    }
    context.commit('setTestResultsLoading', true)
    backend.setToken(context.getters.getToken)
    let response = await backend.fetchTestResults(id)
    context.commit('setTestResults', response.data)
    context.commit('setCurrentToken', response.token)
  }
}
