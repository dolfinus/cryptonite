import { initial_state } from './index'

const date_format     = 'YYYY-MM-DD'
const datetime_format = 'DD.MM.YYYY HH:mm:SS'
const time_format     = 'HH:mm:SS'

let setMethodData = function (fields, params) {
  Object.keys(params).forEach((key) => {
    let value = params[key]
    let [name, type] = key.split('_')
    if (type === 'init') {
      fields.init.forEach(function (val, i, arr) {
        if (val.name === name) {
          arr[i].value = value
        }
      })
    } else {
      if (name === 'content') {
        fields[type].value = value
      } else if (type !== undefined) {
        fields[type].params.forEach(function (val, i, arr) {
          if (val.name === name) {
            arr[i].value = value
          }
        })
      }
    }
  })
  return fields
}

export default {
  resetState: function (state, value) {
    Object.keys(initial_state).forEach(key => { state[key] = initial_state[key] })
  },
  setCurrentUser: function (state, value) {
    state.current_user = {
      id:          value.id,
      name:        value.name,
      first_name:  value.first_name,
      second_name: value.second_name,
      last_name:   value.last_name,
      is_admin:    value.is_admin,
      token:       value.token
    }
  },
  setCurrentToken: function (state, value) {
    state.current_user.token = value
  },
  setNavbarMenu: function (state, value) {
    state.menu.mobileMenu = value
  },
  setNavbarModules: function (state, value) {
    state.menu.dropdownModules = value
  },
  setNavbarTests: function (state, value) {
    state.menu.dropdownTests = value
  },
  setNavbarUser: function (state, value) {
    state.menu.dropdownUser = value
  },
  setCiphers: function (state, value) {
    state.ciphers = {
      is_loading: false,
      categories: value
    }
  },
  setCiphersLoading: function (state, bool) {
    state.ciphers.is_loading = bool
  },
  setCipher: function (state, value) {
    state.cipher.data[value.id] = {
      is_loading: false,
      id: value.id,
      fields: {
        init: value.init,
        encrypt: Object.assign({format: 'str', params: [], 'value': ''}, value.cipher.encrypt || {}),
        decrypt: Object.assign({format: 'str', params: [], 'value': ''}, value.cipher.decrypt || {})
      }
    }
  },
  setCipherLoading: function (state, bool) {
    state.cipher.is_loading = bool
  },
  setModuleResult: function (state, data) {
    let input   = data[0]
    let content = data[1]
    let id      = input[0]
    let method  = input[1].action
    let anti    = ''
    if (method === 'encrypt') {
      anti = 'decrypt'
    } else if (method === 'decrypt') {
      anti = 'encrypt'
    } else if (method === 'sign') {
      anti = 'check'
    } else if (method === 'check') {
      anti = 'sign'
    }
    let fields = setMethodData(state.cipher.data[id].fields, input[1])

    console.log(fields[method].value)
    console.log(content)

    let from_data = fields[method].value
    let to_data   = content

    if (Array.isArray(from_data)) {
      from_data = from_data.join(', ')
    }

    if (Array.isArray(to_data)) {
      to_data = to_data.join(', ')
    }

    console.log(from_data)
    console.log(to_data)

    state.cipher.data[id].fields[method].value = from_data
    state.cipher.data[id].fields[anti].value   = to_data
  },
  setEds: function (state, value) {
    state.eds = {
      is_loading: false,
      categories: value
    }
  },
  setEdsLoading: function (state, bool) {
    state.eds.is_loading = bool
  },
  setDs: function (state, value) {
    state.ds.data[value.id] = {
      is_loading: false,
      id: value.id,
      signed: '',
      checked: '',
      fields: {
        init:  value.init,
        sign:  Object.assign({format: 'str', params: [], 'value': ''}, value.eds.sign  || {}),
        check: Object.assign({format: 'str', params: [], 'value': ''}, value.eds.check || {})
      }
    }
  },
  setDsLoading: function (state, bool) {
    state.ds.is_loading = bool
  },
  setInstruments: function (state, value) {
    state.instruments = {
      is_loading: false,
      categories: value
    }
  },
  setArticles: function (state, value) {
    state.articles = {
      is_loading: false,
      categories: value
    }
  },
  setArticlesLoading: function (state, bool) {
    state.articles.is_loading = bool
  },
  setArticle: function (state, value) {
    state.article = {
      is_loading: false,
      name:       value.name,
      category:   value.category,
      text:       value.content
    }
  },
  setArticleLoading: function (state, bool) {
    state.article.is_loading = bool
  },
  setUsers: function (state, value) {
    state.users = {
      is_loading: false,
      categories: value
    }
  },
  setUsersLoading: function (state, bool) {
    state.users.is_loading = bool
  },
  setUser: function (state, value) {
    state.user = {
      is_loading:  false,
      id:          value.id,
      name:        value.name,
      first_name:  value.first_name,
      second_name: value.second_name,
      last_name:   value.last_name,
      is_admin:    value.is_admin
    }
  },
  setUserLoading: function (state, bool) {
    state.user.is_loading = bool
  },
  setTestsEdit: function (state, value) {
    state.tests_edit = {
      is_loading: false,
      categories: value
    }
  },
  setTestsEditLoading: function (state, bool) {
    state.tests_edit.is_loading = bool
  },
  setTestEdit: function (state, value) {
    let $moment = window.moment
    state.test_edit = {
      is_loading:   false,
      id:           value.id,
      name:         value.name,
      category:     value.category,
      max_duration: value.max_duration,
      not_before:   $moment.utc(value.not_before).local().format(date_format),
      not_after:    $moment.utc(value.not_after ).local().format(date_format),
      items:        value.items
    }
  },
  addTestEditItem: function (state, id, content) {
    if (!state.test_edit.items) {
      state.test_edit.items = []
    }
    state.test_edit.items.splice(id+1, 0, {content: content})
  },
  removeTestEditItem: function (state, id) {
    if (state.test_edit.items.length > id) {
      state.test_edit.items.splice(id, 1)
    }
  },
  setTestEditLoading: function (state, bool) {
    state.test_edit.is_loading = bool
  },
  setTestsRun: function (state, value) {
    state.tests_run = {
      is_loading: false,
      categories: value
    }
  },
  setTestsRunLoading: function (state, bool) {
    state.tests_run.is_loading = bool
  },
  setTestRun: function (state, value) {
    let $moment = window.moment
    state.test_run = {
      is_loading:   false,
      id:           value.id,
      name:         value.name,
      max_duration: value.max_duration,
      not_before:   $moment.utc(value.not_before).local().format(date_format),
      not_after:    $moment.utc(value.not_after ).local().format(date_format),
      items_count:  value.items_count,
      last_item:    value.last_item,
      is_finished:  value.is_finished,
      begin:        $moment.utc(value.begin).local().format(datetime_format),
      end:          $moment.utc(value.end  ).local().format(datetime_format),
      item:         {}
    }
  },
  setTestRunLoading: function (state, bool) {
    state.test_run.is_loading = bool
  },
  setTestRunItem: function (state, value) {
    let $moment = window.moment
    state.test_run.is_loading = false
    state.test_run.item = {
      id:      value.id,
      content: value.content
    }
    if (!state.test_run.begin) {
      state.test_run.begin = $moment.utc()
    }
  },
  setTestsResult: function (state, value) {
    state.tests_result = {
      is_loading: false,
      categories: value
    }
  },
  setTestsResultLoading: function (state, bool) {
    state.tests_result.is_loading = bool
  },
  setTestResult: function (state, value) {
    let $moment = window.moment
    state.test_result = {
      is_loading:   false,
      id:           value.id,
      name:         value.name,
      max_duration: value.max_duration,
      items_count:  value.items_count,
      is_finished:  value.is_finished,
      score:        value.score,
      mark:         value.mark,
      percent:      value.percent,
      begin:        $moment.utc(value.begin).local().format(datetime_format),
      end:          $moment.utc(value.end  ).local().format(datetime_format),
      answers           : []
    }
    if (value.answers) {
      let answers = []
      value.answers.forEach((ans) => {
        let answer = {
          item_no: ans.item_no,
          time:    $moment.utc(ans.time).local().format(datetime_format),
          answer:  ans.answer,
          result:  ans.result
        }
        answers.push(answer)
      })
      state.test_result['answers'] = answers
    }
  },
  setTestResultLoading: function (state, bool) {
    state.test_result.is_loading = bool
  },
  setTestsResults: function (state, value) {
    state.tests_results = {
      is_loading: false,
      categories: value
    }
  },
  setTestsResultsLoading: function (state, bool) {
    state.tests_results.is_loading = bool
  },
  setTestResults: function (state, value) {
    let $moment = window.moment
    state.test_results = {
      is_loading:   false,
      id:           value.id,
      name:         value.name,
      items_count:  value.items_count,
      results:      []
    }
    if (value.results) {
      let results = []
      value.results.forEach((result) => {
        let res = {
          fio:          (result.user.first_name + ' ' + result.user.second_name + ' ' + result.user.last_name).trim(),
          score:        result.score,
          mark:         result.mark,
          percent:      result.percent,
          begin:        result.begin ? $moment.utc(result.begin).local().format(datetime_format) : null,
          end:          result.end   ? $moment.utc(result.end  ).local().format(datetime_format) : null,
          is_finished:  (result.is_finished ? '✓' : '✗')
        }
        if (result.answers) {
          result.answers.forEach((ans, i) => {
            res['result_'+i] = (ans.result ? '✓' : '✗')
            res['time_'+i]   = ans.time ? $moment.utc(ans.time).local().format(datetime_format) : null
            res['answer_'+i] = ans.answer
          })
          /*
          let answers = []
          result.answers.forEach((ans) => {
            let answer = {
              item_no: ans.item_no,
              time:    ans.time ? $moment.utc(ans.time).local().format(datetime_format) : null,
              answer:  ans.answer,
              result:  ans.result
            }
            answers.push(answer)
          })
          res['answers'] = answers
          */
        }
        results.push(res)
      })
      state.test_results.results = results
    }
  },
  setTestResultsLoading: function (state, bool) {
    state.test_results.is_loading = bool
  }
}
