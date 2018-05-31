import Vue from 'vue'
import Router from 'vue-router'

import Navbar from './components/Navbar'
import Menu from './components/Menu'
import Empty from './components/Empty'

import Login from './views/Login'
import Article from './views/Article'

import Module from './components/Module'
import Instrument from './views/Instrument'

import TestEdit from './views/TestEdit'
import TestRun from './views/TestRun'
import TestRunItem from './views/TestRunItem'
import TestResult from './views/TestResult'
import TestResults from './views/TestResults'

import User from './views/User'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      components: {
        main: Login
      }
    },
    {
      path: '/',
      name: 'main',
      components: {
        navbar: Navbar,
        main: ''
      }
    },
    {
      path: '/ciphers',
      name: 'ciphers',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: Module
      },
      props: {
        menu: {type: 'ciphers', one_item: 'cipher', preload: true, category_translate: true, item_translate: true},
        main: {type: 'cipher'}
      },
      children: [{
        name: 'cipher',
        path: ':id'
      }]
    },
    {
      path: '/eds',
      name: 'eds',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: Module
      },
      props: {
        menu: {type: 'eds', one_item: 'ds', preload: true, category_translate: true, item_translate: true},
        main: {type: 'ds'}
      },
      children: [{
        name: 'ds',
        path: ':id'
      }]
    },
    {
      path: '/instruments',
      name: 'instruments',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: Instrument
      },
      props: {
        menu: {type: 'instruments', one_item: 'instrument'}
      },
      children: [{
        name: 'instrument',
        path: ':id'
      }]
    },
    {
      path: '/articles',
      name: 'articles',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: Article
      },
      props: {
        menu: {type: 'articles', one_item: 'article'}
      },
      children: [{
        name: 'article',
        path: ':id'
      }]
    },
    {
      path: '/users',
      name: 'users',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: User
      },
      props: {
        menu: {type: 'users', one_item: 'user', category_translate: true}
      },
      children: [{
        name: 'user',
        path: ':id'
      }]
    },
    {
      path: '/tests/edit',
      name: 'tests_edit',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: TestEdit
      },
      props: {
        menu: {type: 'tests_edit', one_item: 'test_edit'}
      },
      children: [{
        name: 'test_edit',
        path: ':id'
      }]
    },
    {
      path: '/tests/run',
      name: 'tests_run',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: TestRun
      },
      props: {
        menu: {type: 'tests_run', one_item: 'test_run'}
      },
      children: [{
        name: 'test_run',
        path: ':id'
      }]
    },
    {
      path: '/tests/run/:id/:item',
      name: 'test_item_run',
      components: {
        navbar: Navbar,
        main: TestRunItem
      }
    },
    {
      path: '/tests/result',
      name: 'tests_result',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: TestResult
      },
      props: {
        menu: {type: 'tests_result', one_item: 'test_result', category_translate: true}
      },
      children: [{
        name: 'test_result',
        path: ':id'
      }]
    },
    {
      path: '/tests/results',
      name: 'tests_results',
      components: {
        navbar: Navbar,
        menu: Menu,
        main: TestResults
      },
      props: {
        menu: {type: 'tests_results', one_item: 'test_results'}
      },
      children: [{
        name: 'test_results',
        path: ':id'
      }]
    }
  ]
})
