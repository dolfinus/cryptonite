import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Cookies from 'js-cookie'
import createLogger from 'vuex/dist/logger'

import actions from './actions'
import getters from './getters'
import mutations from './mutations'

Vue.use(Vuex)

let secure = window.location.protocol === 'https:'

let initial_state = {
  current_user: {
    name: '',
    first_name: '',
    second_name: '',
    last_name: '',
    is_admin: false,
    token: null
  },
  menu: {
    mobileMenu:      false,
    dropdownModules: false,
    dropdownTests:   false,
    dropdownUser:    false
  },
  ciphers: {
    is_loading: true,
    categories: []
  },
  cipher: {
    is_loading: true,
    data: {
      atbash: {
        id: 'atbash',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      bellaso: {
        id: 'bellaso',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      caesar: {
        id: 'caesar',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      elliptic: {
        id: 'elliptic',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      enigma: {
        id: 'enigma',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      polibiy: {
        id: 'polibiy',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      rsa: {
        id: 'rsa',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      tritemius: {
        id: 'tritemius',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      viginer: {
        id: 'viginer',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      },
      viginer2: {
        id: 'viginer',
        fields: {
          init: [],
          encrypt: {
            format: 'str',
            params: [],
            value: ''
          },
          decrypt: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      }
    }
  },
  eds: {
    is_loading: true,
    categories: []
  },
  ds: {
    is_loading: true,
    data: {
      elliptic: {
        id: 'elliptic',
        fields: {
          init: [],
          sign: {
            format: 'str',
            params: [],
            value: ''
          },
          check: {
            format: 'str',
            params: [],
            value: ''
          }
        }
      }
    }
  },
  articles: {
    is_loading: true,
    categories: []
  },
  article: {
    is_loading: true,
    name: '',
    text: ''
  },
  users: {
    is_loading: true,
    caregories: []
  },
  user: {
    is_loading: true,
    data: null
  },
  tests_edit: {
    is_loading: true,
    categories: []
  },
  test_edit: {
    is_loading: true,
    data: null
  },
  tests_run: {
    is_loading: true,
    caregories: []
  },
  test_run: {
    is_loading: true,
    test: null,
    item: null
  },
  tests_result: {
    is_loading: true,
    caregories: []
  },
  test_result: {
    is_loading: true
  },
  tests_results: {
    is_loading: true,
    caregories: []
  },
  test_results: {
    is_loading: true
  },
  instruments: {
    is_loading: false,
    categories: [{
      id: 'freq',
      items: [
        {id: 'monogram'},
        {id: 'bigram'},
        {id: 'trigram'}
      ]
    }]
  }
}

let plugins = [createPersistedState({
  storage: {
    getItem: key => Cookies.get(key),
    setItem: (key, value) => Cookies.set(key, value, { expires: 7, secure: secure }),
    removeItem: key => Cookies.remove(key)
  }
})]

if (process.env.NODE_ENV !== 'production') {
  plugins = plugins.concat([createLogger()])
}

let store = new Vuex.Store({

  plugins: plugins,
  strict: process.env.NODE_ENV !== 'production',
  mutations,
  actions,
  getters,
  state: Object.assign(initial_state, {})
})

export default store
export { store, initial_state }
