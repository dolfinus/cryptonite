<template>
  <section class="login">
    <div class="level login-logo only-mobile">
      <div class="level-item has-text-centered">
          <img src="../assets/img/logo.svg">
      </div>
    </div>
    <div class="level login-logo only-desktop">
      <div class="level-item has-text-centered">
          <img src="../assets/img/logo.svg">
      </div>
    </div>
    <div class="level">
      <div class="level-item">
          <form ref="form" name="login" autocomplete="on">
            <vue-form-generator :schema="schema" :model="model" :options="formOptions"/>
          </form>
      </div>
    </div>
    <div class="level">
      <p class="level-item has-text-centered control">
        <a class="button is-success" @click.prevent="onLogin">
          <span v-t="'button.sign_in'"/>
        </a>
      </p>
    </div>
  </section>
</template>

<script>
import { validators } from 'vue-form-generator'

export default {
  name: 'Login',
  data () {
    return {
      model: {
        username: '',
        password: ''
      },
      schema: {
        fields: [
          {
            type: 'input',
            inputName: 'username',
            inputType: 'text',
            model: 'username',
            label: this.$t('label.login'),
            placeholder: this.$t('placeholder.login'),
            required: true,
            validator: validators.username
          },
          {
            type: 'input',
            inputName: 'password',
            inputType: 'password',
            model: 'password',
            label: this.$t('label.password'),
            placeholder: this.$t('placeholder.password'),
            required: true,
            validator: validators.password
          }
        ]
      },
      formOptions: {
        validateAfterLoad: false,
        validateAfterChanged: true
      }
    }
  },
  computed: {
    token () {
      return this.$store.getters.getToken
    }
  },
  watch: {
    token (to, from) {
      if (from === undefined || from === null) {
        if (to !== undefined && to !== null) {
          this.$router.push({name: 'main'})
        }
      }
    }
  },
  methods: {
    onLogin: function () {
      const formData = new FormData(this.$refs.form)
      var auth = {}
      for (var [key, value] of formData.entries()) {
        auth[key] = value
      }
      this.$store.dispatch('logoutUser').then(
        this.$store.dispatch('loginUser', auth)
      )
    }
  },
  mounted () {
    this.$store.dispatch('logoutUser')
  }
}
</script>

<style lang="sass" scoped>

.login-logo.only-desktop
  margin-top: 120px
  margin-bottom: 30px

.login-logo.only-mobile
  margin-top: 2em!important

.login-logo 
  img
    height: 200px

fieldset
  border: none
  width: 20em

</style>
