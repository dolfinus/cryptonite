<template>
    <section v-if="this.$route.params.id !== undefined" class="column">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{user.name}}
        </p>
      </header>
      <div class="card-content">
        <form ref="form" name="user">
          <vue-form-generator :schema="schema" :model="model" :options="formOptions"/>

          <div class="field is-grouped">
            <p v-if="isCurrentAdmin && !isNew" class="control">
              <a class="button is-danger is-outlined" @click.prevent="onDelete" :disabled="this.isEditingCurrent">
                <span class="icon is-small">
                  <i class="fa fa-times"/>
                </span>
                <span v-t="'button.delete'"/>
              </a>
            </p>
            <p class="control">
              <a class="button is-success" @click.prevent="onSave">
                <span v-t="isNew ? 'button.create' : 'button.save'"/>
                <span class="icon is-small">
                  <i class="fa fa-check"/>
                </span>
              </a>
            </p>
          </div>
        </form>
      </div>
    </div>
  </section>
  <section v-else-if="this.isCurrentAdmin" class="centered-item">
    <router-link  class="" :to="{ name: 'user', params: {id: 'new'}}">
      <header class="fa fa-user-plus new-item">
      </header>
      <p v-t="'user.new'"/>
    </router-link>
  </section>
</template>

<script>
import 'vue-form-generator/dist/vfg-core.css'
import { validators } from 'vue-form-generator'

export default {
  name: 'User',
  data () {
    return {
      formOptions: {
        validateAfterLoad: false,
        validateAfterChanged: true
      }
    }
  },
  computed: {
    model () {
      return {
        name:        this.user.name        || '',
        first_name:  this.user.first_name  || '',
        second_name: this.user.second_name || '',
        last_name:   this.user.last_name   || '',
        password:    '',
        is_admin:    this.user.is_admin
      }
    },
    id () {
      let id = this.$route.params.id
      if (id === undefined || id === 'new') {
        id = ''
      }
      return id
    },
    isNew () {
      return this.$route.params.id === 'new'
    },
    schema () {
      let result = [
        {
          type: 'input',
          inputName: 'first_name',
          inputType: 'text',
          model: 'first_name',
          label: this.$t('label.first_name'),
          validator: validators.string
        },
        {
          type: 'input',
          inputName: 'second_name',
          inputType: 'text',
          model: 'second_name',
          label: this.$t('label.second_name'),
          validator: validators.string
        },
        {
          type: 'input',
          inputName: 'last_name',
          inputType: 'text',
          model: 'last_name',
          label: this.$t('label.last_name'),
          validator: validators.string
        },
        {
          type: 'input',
          inputName: 'password',
          inputType: 'password',
          model: 'password',
          label: this.$t('label.password'),
          required: this.isNew,
          validator: validators.password
        }
      ]
      if (this.isNew) {
        result = [
          {
            type: 'input',
            inputName: 'name',
            inputType: 'text',
            model: 'name',
            label: this.$t('label.login'),
            required: true,
            validator: validators.string
          }
        ].concat(result)
      }

      if (this.isCurrentAdmin === true) {
        result = result.concat([
          {
            type: 'checkbox',
            inputName: 'is_admin',
            model: 'is_admin',
            label: this.$t('label.is_admin'),
            default: false
          }
        ])
      }

      return {
        fields: result
      }
    },
    user () {
      return this.$store.getters.getUserData
    },
    currentUser () {
      return this.$store.getters.getCurrentUser
    },
    isCurrentAdmin () {
      return this.$store.getters.isCurrentAdmin
    },
    isEditingCurrent () {
      return this.id === this.currentUser.name
    },
    isLoading () {
      return this.$store.getters.getUserLoading
    }
  },
  watch: {
    '$store' (to, from) {
      this.reloadMenu()
    },
    '$route' (to, from) {
      this.reloadCurrent()
    }
  },
  methods: {
    onSave: function () {
      const formData = new FormData(this.$refs.form)
      var data = {}
      for (var [key, value] of formData.entries()) {
        if (value === 'on' || value === 'off') {
          value = (value === 'on')
        }
        data[key] = value
      }
      let reload = this.reloadMenu
      let refresh = this.reloadCurrent
      this.$store.dispatch('saveUser', [this.id, data]).then(this.$store.dispatch('fetchCurrentUser')).then(reload).then(refresh)
    },
    redirect: function () {
      this.$router.push({name: 'user', params: {id: undefined}})
    },
    onDelete: function () {
      let reload = this.reloadMenu
      let redirect = this.redirect
      this.$store.dispatch('deleteUser', this.id).then(reload).then(redirect)
    },
    reloadMenu: function () {
      this.$store.dispatch('fetchUsers')
    },
    reloadCurrent: function () {
      this.$store.dispatch('fetchUser', this.id)
    }
  },
  mounted () {
    if (this.currentUser === undefined || this.currentUser === null || this.currentUser === {}) {
      this.$router.push({name: 'login'})
    }
    this.reloadMenu()
    this.reloadCurrent()
  }
}
</script>

<style lang='sass' scoped>
</style>
