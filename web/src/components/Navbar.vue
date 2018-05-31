<template>
  <nav class="navbar" role="navigation" aria-label="dropdown navigation">
  
  <div class="navbar-brand">
    <router-link tag="a" class="navbar-item" :to="{ name: 'main'}">
      <img src="../assets/img/logo.svg"/>
    </router-link>
    
    <breadcrumb :list="list" class="breadcrumb centered-item only-mobile" aria-label="breadcrumbs"></breadcrumb>

    <div class="navbar-burger">
      <a class="navbar-link" @click="toggleMenu">
        <i class="fa fa-bars"/>
      </a>
    </div>
  </div>

  <div class="navbar-menu" :class="{'is-active': mobileMenu}">
    <div class="navbar-start">
      <router-link tag="a" class="navbar-item" :to="{ name: 'articles'}" v-t="'navbar.articles'"/>

      <div class="navbar-item has-dropdown" :class="{'is-active': dropdownModules}">
        <a class="navbar-link" @click="toggleModules" v-t="'navbar.modules.main'"/>

        <div class="navbar-dropdown">
          <router-link tag="a" class="navbar-item" :to="{ name: 'ciphers'}">
            <a >
              <span class="icon is-small">
                <i class="fa fa-user-secret"/>
              </span>
              <span v-t="'navbar.modules.ciphers'"/>
            </a>
          </router-link>
          <router-link tag="a" class="navbar-item" :to="{ name: 'eds'}">
            <a>
              <span class="icon is-small">
                <i class="fa fa-lock"/>
              </span>
              <span v-t="'navbar.modules.eds'"/>
            </a>
          </router-link>
          <router-link tag="a" class="navbar-item" :to="{ name: 'instruments'}">
            <a>
              <span class="icon is-small">
                <i class="fa fa-chart-bar"/>
              </span>
              <span v-t="'navbar.modules.instruments'"/>
            </a>
          </router-link>
        </div>
      </div>

      <div class="navbar-item has-dropdown" :class="{'is-active': dropdownTests}">
        <a class="navbar-link" @click="toggleTests" v-t="'navbar.test.main'"/>

        <div class="navbar-dropdown">
          <router-link tag="a" class="navbar-item" v-if="this.isCurrentAdmin" :to="{ name: 'tests_edit'}">
            <a>
              <span class="icon is-small">
                <i class="fa fa-edit"/>
              </span>
              <span v-t="'navbar.test.edit'"/>
            </a>
          </router-link>
          <router-link tag="a" class="navbar-item" :to="{ name: 'tests_run'}">
            <a>
              <span class="icon is-small">
                <i class="fa fa-play"/>
              </span>
              <span v-t="'navbar.test.run'"/>
            </a>
          </router-link>
          <router-link tag="a" class="navbar-item" :to="{ name: (this.isCurrentAdmin ? 'tests_results' : 'tests_result')}">
            <a>
              <span class="icon is-small">
                <i class="fa fa-list"/>
              </span>
              <span v-t="'navbar.test.results'"/>
            </a>
          </router-link>
        </div>
      </div>

      <router-link tag="a" class="navbar-item" v-if="this.isCurrentAdmin" :to="{ name: 'users'}" v-t="'navbar.users.main'"/>
    </div>

    <div class="navbar-end">
      <div class="navbar-item has-dropdown" :class="{'is-active': dropdownUser}">
        <a class="navbar-link only-desktop" @click="toggleUser">
          <span class="icon is-small">
            <i class="fa fa-user"/>
          </span>
          <span>{{this.currentUser.name}}</span>
        </a>

        <div class="navbar-dropdown is-right">
          <div class="navbar-item only-mobile">
            <span class="icon is-small">
              <i class="fa fa-user"/>
            </span>
            <span>{{this.currentUser.first_name}} {{this.currentUser.second_name}} {{this.currentUser.last_name}}</span>
          </div>
          <div class="navbar-item only-desktop">
            <span>{{this.currentUser.first_name}} {{this.currentUser.second_name}} {{this.currentUser.last_name}}</span>
          </div>
          <hr class="navbar-divider">
          <router-link tag="div" class='navbar-item' :to="{ name: 'user', params: {id: this.currentUser.name}}">
            <a>
              <span class="icon is-small">
                <i class="fa fa-cog"/>
              </span>
              <span v-t="'navbar.users.settings'"/>
            </a>
          </router-link>

          <hr class="navbar-divider">
          <router-link tag="div" class='navbar-item' :to="{ name: 'login'}">
              <a>
              <span class="icon is-small">
                <i class="fa fa-power-off"/>
              </span>
              <span v-t="'navbar.users.logout'"/>
            </a>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</nav>
</template>
<script>
import Breadcrumb from 'vue-bulma-breadcrumb'

export default {
  name: 'Navbar',
  components: {
    Breadcrumb
  },
  data () {
    return {}
  },
  computed: {
    currentUser () {
      return this.$store.getters.getCurrentUser
    },
    isCurrentAdmin () {
      return this.$store.getters.isCurrentAdmin
    },
    isLoggedIn () {
      return this.$store.getters.isLoggedIn
    },
    mobileMenu () {
      return this.$store.getters.getNavbarMenu
    },
    dropdownModules () {
      return this.$store.getters.getNavbarModules
    },
    dropdownTests () {
      return this.$store.getters.getNavbarTests
    },
    dropdownUser () {
      return this.$store.getters.getNavbarUser
    },
    list () {
      let path   = []
      let parent = ''
      let name   = this.$route.name
      if (name.indexOf('test') !== -1) {
        parent = 'test.'
        name = name.replace('test_', '').replace('tests_', '')
        path.push({name: this.$t('navbar.'+parent+'main'), path: '/'})
      }
      if (name.indexOf('eds') !== -1 || name.indexOf('cipher') !== -1 || name.indexOf('instrument') !== -1) {
        parent = 'modules.'
        path.push({name: this.$t('navbar.'+parent+'main'), path: '/'})
      }
      if (name.indexOf('user') !== -1) {
        path.push({name: this.$t('navbar.users.main'), path:this.$route.path})
      } else {
        path.push({name: this.$t('navbar.'+parent+name), path:this.$route.path})
      }
      return path
    }
  },
  watch: {
    '$route' (to, from) {
      this.reloadNavbar()
    }
  },
  methods: {
    reloadNavbar () {
      this.$store.dispatch('setNavbarMenu',    false)
      this.$store.dispatch('setNavbarModules', false)
      this.$store.dispatch('setNavbarTests',   false)
      this.$store.dispatch('setNavbarUser',    false)
    },
    toggleMenu () {
      this.$store.dispatch('toggleNavbarMenu')
    },
    toggleModules () {
      this.$store.dispatch('toggleNavbarModules')
    },
    toggleTests () {
      this.$store.dispatch('toggleNavbarTests')
    },
    toggleUser () {
      this.$store.dispatch('toggleNavbarUser')
    }
  },
  mounted () {
    if (!this.isLoggedIn) {
      return this.$router.push({name: 'login'})
    }
    this.reloadNavbar()
  }
}
</script>

<style lang="sass" scoped>

nav.navbar
  min-height: none
  background-color: $nav-background
  border-bottom: solid 1px #dbdbdb

.navbar-brand > .navbar-item
  padding-left: 10px

  img
    height: 15px

.navbar-link .icon
  padding-right: 0.5em
  padding-bottom: 0.1em

</style>
