<template>
    <section v-if="this.isCurrentAdmin && this.$route.params.id !== undefined" class="column">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{test.name}}
        </p>
      </header>
      <div class="card-content">
        <form ref="form" name="test_edit">
          <vue-form-generator :schema="schema" :model="model" :options="formOptions"/>
          <div class="field is-grouped">
            <p class="control" v-if="!isNew" >
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
        </form>
      </div>
    </div>
  </section>
  <section v-else-if="this.isCurrentAdmin" class="centered-item">
    <router-link  class="" :to="{ name: 'test_edit', params: {id: 'new'}}">
      <header class="fa fa-calendar-plus new-item">
      </header>
      <p v-t="'test_edit.new'"/>
    </router-link>
  </section>
</template>

<script>
import { validators } from 'vue-form-generator'

export default {
  name: 'TestEdit',
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
      let config = {
        name:         this.test.name         || '',
        category:     this.test.category     || '',
        max_duration: this.test.max_duration || 60,
        not_before:  (this.test.not_before ? this.test.not_before : null),
        not_after:   (this.test.not_after  ? this.test.not_after  : null)
      }
      if (this.test.items !== undefined && this.test.items !== null) {
        this.test.items.forEach((item, index) => {
          config['item' + index] = item.content || ''
        })
      }
      return config
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
          inputName: 'category',
          inputType: 'text',
          model: 'category',
          label: this.$t('label.category'),
          validator: validators.string
        },
        {
          type: 'input',
          inputName: 'max_duration',
          inputType: 'number',
          model: 'max_duration',
          label: this.$t('label.max_duration'),
          validator: validators.integer
        },
        {
          type: 'input',
          inputName: 'not_before',
          inputType: 'date',
          model: 'not_before',
          label: this.$t('label.not_before'),
          validator: validators.date
        },
        {
          type: 'input',
          inputName: 'not_after',
          inputType: 'date',
          model: 'not_after',
          label: this.$t('label.not_after'),
          validator: validators.date
        }
      ]
      if (this.isNew) {
        result = [
          {
            type: 'input',
            inputName: 'name',
            inputType: 'text',
            model: 'name',
            label: this.$t('label.name'),
            placeholder: this.$t('placeholder.test_name'),
            required: true,
            validator: validators.string
          }
        ].concat(result)
      }

      if (this.test.items !== undefined && this.test.items !== null) {
        this.test.items.forEach((item, index) => {
          result.push({
            type: 'md-editor',
            inputName:'md_editor_' + index,
            model: 'item' + index,
            required: true,
            label: '#' + (index + 1),
            id: index
          })
        })
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
    test () {
      return this.$store.getters.getTestEdit
    },
    isLoading () {
      return this.$store.getters.getTestEditLoading
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
    addButtons: function () {
      let labels = this.$el.querySelectorAll('.field-md-editor > label')
      if (labels.length === 0) return
      labels.forEach((label, index) => {
        label.querySelectorAll('a').forEach((a) => a.remove())
        let plus_button  = document.createElement('a')
        let minus_button = document.createElement('a')

        let plus  = document.createElement('i')
        let minus = document.createElement('i')

        plus.className  = 'fa fa-plus add-item'
        minus.className = 'fa fa-trash remove-item'

        plus_button.appendChild(plus)
        minus_button.appendChild(minus)

        plus_button.editor_id  = index
        minus_button.editor_id = index

        plus_button.iteminsertAfter = this.insertAfter
        minus_button.itemRemove = this.removeItem

        plus_button.addEventListener('click', function () {
          this.iteminsertAfter(this.editor_id)
        })
        minus_button.addEventListener('click', function () {
          this.itemRemove(this.editor_id)
        })

        if (labels.length !== 1) label.appendChild(minus_button)
        label.appendChild(plus_button)
      })
    },
    onSave: function () {
      const formData = new FormData(this.$refs.form)
      var data = {}
      var items = []
      var format = /content_(\d+)/i
      for (var [key, value] of formData.entries()) {
        let matches = key.match(format)
        console.log(key, matches)
        if (matches !== null) {
          items.push({
            content: value
          })
        } else {
          data[key] = value
        }
      }
      if (items.length > 0) {
        data.items = items
      }
      let reload = this.reloadMenu
      let refresh = this.reloadCurrent
      this.$store.dispatch('saveTest', [this.id, data]).then(reload).then(refresh)
    },
    onDelete: function () {
      let reload = this.reloadMenu
      let redirect = this.redirect
      this.$store.dispatch('deleteTest', this.id).then(reload).then(redirect)
    },
    reloadMenu: function () {
      this.$store.dispatch('fetchTestsEdit')
    },
    reloadCurrent: function () {
      if (this.$route.params.id === 'new') {
        this.$store.dispatch('addTestEditItem', [0, ''])
      } else {
        this.$store.dispatch('fetchTestEdit', this.id)
      }
    },
    redirect: function () {
      this.$router.push({name: 'test_edit', params: {id: undefined}})
    },
    insertAfter: function (id) {
      this.$store.dispatch('addTestEditItem', [id, ''])
    },
    removeItem: function (id) {
      this.$store.dispatch('removeTestEditItem', id)
    }
  },
  mounted () {
    this.reloadMenu()
    this.reloadCurrent()
  },
  updated () {
    this.addButtons()
  }
}
</script>

<style lang='css' scoped>
</style>
