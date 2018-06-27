<template>
    <section v-if="this.$route.params.id !== undefined" class="column">
    <div class="card">
      <div class="card-content">
        <form ref="form" name="module">
          <div class="content columns">
            <vue-form-generator class="field column" :schema.sync="schemaInit" :model.sync="modelInit" :options.sync="formOptions"/>
          </div>
          <div class="content columns">
            <vue-form-generator class="field column" :schema.sync="schemaLeft" :model.sync="modelLeft" :options.sync="formOptions"/>
            <vue-form-generator class="field column" :schema.sync="schemaRight" :model.sync="modelRight" :options.sync="formOptions"/>
          </div>
          <div class="content columns">
            <div class="field column">
              <p class="control">
                <a class="button is-success" @click.prevent="runAction('left')">
                  <span>{{$t('button.'+allMethods[this.$props.type][0])}}</span>
                </a>
              </p>
            </div>
            <div class="field column">
              <p class="control">
                <a class="button is-success" @click.prevent="runAction('right')">
                  <span>{{$t('button.'+allMethods[this.$props.type][1])}}</span>
                </a>
              </p>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>
  <empty v-else/>
</template>

<script>
import { validators } from 'vue-form-generator'
import Empty from './Empty'

export default {
  name: 'Module',
  props: ['type'],
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
    allMethods () {
      return {
        'cipher': ['encrypt', 'decrypt'],
        'ds':     ['sign',      'check']
      }
    },
    modelInit () {
      let method = 'init'
      return this.getModel(this.getField(method), method)
    },
    modelLeft () {
      let type   = this.allMethods[this.$props.type]
      let method = type[0]
      let field  = this.getField(method)
      return this.getModel(field.params, method)
    },
    modelRight () {
      let type   = this.allMethods[this.$props.type]
      let method = type[1]
      let field  = this.getField(method)
      return this.getModel(field.params, method)
    },
    schemaInit () {
      let method = 'init'
      return this.getSchema(this.getField(method), method)
    },
    schemaLeft () {
      let type   = this.allMethods[this.$props.type]
      let method = type[0]
      let field  = this.getField(method)
      return this.getSchema(field.params, method, field.format)
    },
    schemaRight () {
      let type   = this.allMethods[this.$props.type]
      let method = type[1]
      let field  = this.getField(method)
      return this.getSchema(field.params, method, field.format)
    },
    valueLeft () {
      let type   = this.allMethods[this.$props.type]
      let method = type[0]
      let field  = this.getField(method)
      return this.getValue(field.value)
    },
    valueRight () {
      let type   = this.allMethods[this.$props.type]
      let method = type[1]
      let field  = this.getField(method)
      return this.getValue(field.value)
    },
    fields () {
      return this.$store.getters.getModuleFields(this.$props.type, this.$route.params.id)
    },
    isLoading () {
      return this.$store.getters.getModuleLoading(this.$props.type)
    },
    str_array_pattern () {
      let pattern = '^[a-zа-я\\s,[\\]]*$'
      if (this.$refs.form) {
        let input = this.$refs.form.alphabet_init
        let alphabet = 'en'
        if (input) {
          alphabet = input.value
          if (alphabet === 'en') {
            pattern = '^[a-z\\s,[\\]]*$'
          }
          if (alphabet === 'en25') {
            pattern = '^[abcdefghiklmnopqrstuvwxyz\\s,[\\]]*$'
          }
          if (alphabet === 'ru') {
            pattern = '^[абвгдежзийклмнопрстуфхцчшщъыьэюя\\s,[\\]]*$'
          }
          if (alphabet === 'ru33') {
            pattern = '^[а-я\\s,[\\]]*$'
          }
        }
      }
      return RegExp(pattern, 'iu')
    },
    int_array_pattern () {
      return /^[\d\s,[\]]*$/iu
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.params.id !== undefined) {
        this.reload()
      }
    }
  },
  methods: {
    getValue: function (field) {
      if (field) {
        return field.value || field.default || ''
      }
      return ''
    },
    getField: function (name) {
      return this.$store.getters.getModuleField(this.$props.type, this.$route.params.id, name)
    },
    getModel: function (fields, side) {
      let config = {}
      if (fields === undefined || fields === null) {
        fields = []
      }
      fields.forEach((field) => {
        let name = field.name+'_'+side
        config[name] = this.getValue(field.value)
        if (field.name === 'alphabet' && config[name] === '') config[name] = 'en'
      })
      if (side !== 'init') {
        config['content_'+side] = this.getValue(this.getField(side))
      }
      return config
    },
    getSchema: function (fields, side, content) {
      let config = []
      if (fields === undefined || fields === null) {
        fields = []
      }
      console.log(fields)
      fields.forEach( (field) => {
        let item = {
          type:      'input',
          name:      field.name,
          inputName: field.name + '_' + side,
          inputType: 'text',
          model:     field.name + '_' + side,
          label:     (field.name.length > 1 ? this.$t('label.'+field.name) : field.name.capitalize())
        }
        if (field.required) {
          item.selectOptions = {
            hideNoneSelectedText: true
          }
          item.required  = true
          item.validator = [validators.required]
        }
        if (field.type === 'textarea') {
          item.type = 'textArea'
          item.validator = [validators.alpha]
        } else if (field.type === 'str') {
          item.inputType = 'text'
          item.validator = [validators.alpha]
        } else if (field.type === 'int' || field.type === 'prime') {
          item.inputType = 'number'
          item.validator = [validators.integer]
        } else if (field.type === 'regexp') {
          item.inputType = 'text'
          item.pattern   = RegExp(field.expr, 'iu')
          item.validator = [validators.regexp]
        } else if (field.type === 'select') {
          item.type = 'select'
          item.values = field.values
          if (!Array.isArray(field.values)) {
            item.values = Object.keys(field.values).map((key) => {
              return {
                id: key,
                name: (key.length > 1 ? this.$t('label.' + key) : key)
              }
            })
          }
          console.log(item)
        } else if (field.type === 'alphabet') {
          item.type = 'select'
          item.values = function () {
            return [
              { id: 'en',   name: this.$t('alphabet.en') },
              { id: 'en25', name: this.$t('alphabet.en25') },
              { id: 'ru',   name: this.$t('alphabet.ru') },
              { id: 'ru33', name: this.$t('alphabet.ru33') }
            ]
          }
          item.selectOptions = {
            hideNoneSelectedText: true
          }
          item.required  = true
          item.validator = [validators.required]
        }
        config.push(item)
      })
      if (content !== undefined) {
        let textarea = {
          type:      'textArea',
          inputName: 'content' + '_' + side,
          model:     'content' + '_' + side,
          label:     this.$t('label.content')
        }
        if (content === 'str') {
          textarea.pattern = this.str_array_pattern
        } else if (content === 'int') {
          textarea.pattern = this.int_array_pattern
        }
        textarea.validator = [validators.regexp]
        config.push(textarea)
      }
      return {
        fields: config
      }
    },
    reload: function () {
      let type   = this.allMethods[this.$props.type]
      if ((!this.fields[type[0]] || !this.fields[type[1]]) && this.$route.params.id !== undefined) { // eslint-disable-line eqeqeq
        this.$store.dispatch('fetch' + this.$props.type.capitalize(), this.$route.params.id).then(
          this.$forceUpdate()
        )
      }
    },
    runAction: function (side) {
      const formData = new FormData(this.$refs.form)
      var data = {}
      let i = side === 'left' ? 0 : 1
      let method = this.allMethods[this.$props.type][i]
      let fields = this.getField(method)
      for (var [key, value] of formData.entries()) {
        let [name, type] = key.split('_')
        if (name === 'content' && type === method) {
          let format = fields.format
          if (format === 'int') {
            data[key] = this.clear_upper(value).split(/\s/)
          } else {
            data[key] = this.clear_upper(value)
          }
        } else if (type === 'init' || type === method) {
          data[key] = name === 'alphabet' ? value : value.toUpperCase()
        }
      }
      console.log(data)
      data.action = method
      this.$store.dispatch('moduleSend', [this.$route.params.id, data]).then(
        // this.$forceUpdate()
      )
    },
    clear_upper: function (str) {
      return str.replace(/,/g, ' ').replace(/\s+/g, ' ').replace(/\[/g, '').replace(/\]/g, '').trim().toUpperCase()
    }
  },
  mounted () {
    this.reload()
  }
}
</script>

<style lang="sass" scoped>


</style>
