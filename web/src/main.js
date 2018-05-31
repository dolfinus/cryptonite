import Vue from 'vue'
import Buefy from 'buefy'
import VueFormGenerator from 'vue-form-generator'
import AsyncComputed from 'vue-async-computed'
import 'regenerator-runtime/runtime'
import VueI18n from 'vue-i18n'
import messages from './i18n'
import router from './router.js'
import store from './store'
import './filters.js'
import Mixins from './mixins.js'
import App from './App.vue'
import { mdEditor } from './components/MarkdownEditor'

import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import 'vue-form-generator/dist/vfg-core.css'
import fontawesome from '@fortawesome/fontawesome'
import solid from '@fortawesome/fontawesome-free-solid'
require('material-design-icons-iconfont/dist/material-design-icons.css')
import './assets/img/favicon-32x32.png'

const moment = require('vue-moment')
const momentDurationFormatSetup = require('moment-duration-format')

Vue.component('fieldMdEditor', mdEditor)
Vue.mixin(Mixins)
Vue.use(Buefy)
Vue.use(VueFormGenerator)
Vue.use(AsyncComputed)
Vue.use(VueI18n)
Vue.use(moment)
momentDurationFormatSetup(Vue.moment)
window.moment = Vue.moment

const i18n = new VueI18n({
  locale: 'en',
  messages
})

const vue = new Vue({
  i18n,
  el: '#vue-app',
  router,
  store,
  template: '<App/>',
  mixins: [Mixins],
  components: { App }
})
