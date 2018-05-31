export default {
  getToken: (state) => {
    return state.current_user.token
  },
  getCurrentUser: (state) => {
    return state.current_user
  },
  isLoggedIn: (state) => {
    return state.current_user !== undefined && state.current_user !== null && state.current_user !== {} && state.current_user.token !== undefined && state.current_user.token !== null
  },
  isCurrentAdmin: (state) => {
    return state.current_user.is_admin === true
  },

  getNavbarMenu: (state) => {
    return state.menu.mobileMenu
  },
  getNavbarModules: (state) => {
    return state.menu.dropdownModules
  },
  getNavbarTests: (state) => {
    return state.menu.dropdownTests
  },
  getNavbarUser: (state) => {
    return state.menu.dropdownUser
  },

  getMenuContent: (state) => (type) => {
    return state[type].categories
  },
  getMenuLoading: (state) => (type) => {
    return state[type].is_loading
  },
  getMenuVisible: (state) => (type) => {
    if (type === 'users' && state.current_user.is_admin !== true) {
      return false
    }
    if (!state[type].categories || state[type].categories.length === 0) {
      return false
    }
    return true
  },

  getModuleFields: (state) => (type, id) => {
    if (!state[type].data[id]) {
      return {}
    }
    return state[type].data[id].fields
  },
  getModuleField: (state) => (type, id, name) => {
    if (!state[type].data[id]) {
      return {}
    }
    if (!state[type].data[id].fields[name]) {
      return {}
    }
    return state[type].data[id].fields[name]
  },
  getModuleLoading: (state) => (type) => {
    return state[type].is_loading
  },

  getUserData: (state) => {
    return state.user
  },
  getUserLoading: (state) => {
    return state.user.is_loading
  },

  getTestEdit: (state) => {
    return state.test_edit
  },
  getTestEditLoading: (state) => {
    return state.test_edit.is_loading
  },

  getTestsRun: (state) => {
    return state.tests_run
  },
  getTestRun: (state) => {
    return state.test_run
  },
  getTestRunLoading: (state) => {
    return state.test_run.is_loading
  },

  getTestResult: (state) => {
    return state.test_result
  },
  getTestResultLoading: (state) => {
    return state.test_result.is_loading
  },

  getTestResults: (state) => {
    return state.test_results
  },
  getTestResultsLoading: (state) => {
    return state.test_results.is_loading
  },

  getInstruments: (state) => {
    return state.instruments
  },
  getInstrumentsLoading: (state) => {
    return state.instruments.is_loading
  }
}
