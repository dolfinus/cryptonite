<template>
    <section v-if="this.$route.params.id !== undefined">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{article.name}}
        </p>
      </header>
      <div class="card-content">
        <form ref="form" name="article">
          <vue-form-generator :schema="schema" :model="model" :options="formOptions"/>
          <template v-if="isCurrentAdmin">
            <div class="field is-grouped">
              <p class="control" v-if="!isNew">
                <a class="button is-danger is-outlined" @click.prevent="onDelete">
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
          </template>
        </form>
      </div>
    </div>
  </section>
  <section v-else-if="this.isCurrentAdmin" class="centered-item">
    <router-link  class="" :to="{ name: 'article', params: {id: 'new'}}">
      <header class="fa fa-plus new-item">
      </header>
      <p v-t="'article.new'"/>
    </router-link>
  </section>
  <empty v-else/>
</template>

<script>
import Empty from '../components/Empty'
import { validators } from 'vue-form-generator'

export default {
  name: 'Article',
  components: {
    empty: Empty
  },
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
        name:     this.article.name     || '',
        category: this.article.category || '',
        content:  this.article.text     || ''
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
          type: 'md-editor',
          model: 'content',
          required: true
        }
      ]
      if (!this.isCurrentAdmin) {
        result[0].disabled = true
        result[0].readonly = true
      } else {
        result = [{
          type: 'input',
          inputName: 'category',
          inputType: 'text',
          model: 'category',
          label: this.$t('label.category'),
          validator: validators.string
        }].concat(result)
      }
      if (this.id === '') {
        result = [
          {
            type: 'input',
            inputName: 'name',
            inputType: 'text',
            model: 'name',
            label: this.$t('label.title'),
            placeholder: this.$t('placeholder.title'),
            required: true,
            validator: validators.string
          }
        ].concat(result)
      }

      return {
        fields: result
      }
    },
    currentUser () {
      return this.$store.getters.getCurrentUser
    },
    isCurrentAdmin () {
      return this.$store.getters.isCurrentAdmin
    },
    article () {
      return this.$store.state.article
    },
    isLoading () {
      return this.$store.state.article.is_loading
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
        data[key] = value
      }
      let reload = this.reloadMenu
      let refresh = this.reloadCurrent
      this.$store.dispatch('saveArticle', [this.id, data]).then(reload).then(refresh)
    },
    onDelete: function () {
      let reload = this.reloadMenu
      let redirect = this.redirect
      this.$store.dispatch('deleteArticle', this.id).then(reload).then(redirect)
    },
    reloadMenu: function () {
      this.$store.dispatch('fetchArticles')
    },
    reloadCurrent: function () {
      this.$store.dispatch('fetchArticle', this.id)
    },
    redirect: function () {
      this.$router.push({name: 'article', params: {id: undefined}})
    }
  },
  mounted () {
    this.reloadMenu()
    this.reloadCurrent()
  }
}
</script>

<style lang='css' scoped>
</style>
