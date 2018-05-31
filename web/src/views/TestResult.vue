<template>
    <section v-if="this.$route.params.id !== undefined">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{test.name}}
        </p>
      </header>
      <div class="card-content">
        <form ref="form" name="test_edit">
          <vue-form-generator :schema="schema" :model="model" :options="formOptions"/>
        </form>
      </div>
    </div>
  </section>
  <empty v-else-if="isEmpty" :content="$t('placeholder.empty_result')"/>
  <empty v-else/>
</template>

<script>
import Empty from '../components/Empty'

export default {
  name: 'TestRun',
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
      let config = {
        name:         this.test.name,
        max_duration: this.test.max_duration,
        begin:       (this.test.begin      ? this.test.begin      : null),
        end:         (this.test.end        ? this.test.end        : null),
        score:       this.test.mark + ' (' + this.test.percent + '%)',
        state:       (this.test.is_finished ? this.$t('label.finished') : this.$t('label.over'))
      }
      if (this.test.answers !== undefined && this.test.answers !== null) {
        this.test.answers.forEach((answer, index) => {
          config['item' + index] = answer.answer || ''
        })
      }
      return config
    },
    schema () {
      let result = [
        {
          type: 'input',
          inputName: 'name',
          inputType: 'text',
          model: 'name',
          label: this.$t('label.name'),
          readonly: true
        },
        {
          type: 'input',
          inputName: 'max_duration',
          inputType: 'number',
          model: 'max_duration',
          label: this.$t('label.max_duration'),
          readonly: true
        },
        {
          type: 'input',
          model: 'state',
          inputName: 'state',
          inputType: 'text',
          label: this.$t('label.state'),
          readonly: true
        },
        {
          type: 'input',
          inputName: 'begin',
          inputType: 'text',
          model: 'begin',
          label: this.$t('label.begin'),
          readonly: true
        },
        {
          type: 'input',
          inputName: 'end',
          inputType: 'text',
          model: 'end',
          label: this.$t('label.end'),
          readonly: true
        },
        {
          type: 'input',
          inputName: 'score',
          inputType: 'text',
          model: 'score',
          label: this.$t('label.score'),
          readonly: true
        }
      ]

      if (this.test.answers !== undefined && this.test.answers !== null) {
        this.test.answers.forEach((answer, index) => {
          result.push({
            type: 'md-editor',
            inputName:'md_editor_' + index,
            model: 'item' + index,
            label: '#' + (index + 1) + ': ' + (answer.result ? '✓' : '✗'),
            id: index,
            options: {
              placeholder: this.$t('placeholder.skipped_answer')
            },
            disabled: true,
            readonly: true
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
      return this.$store.getters.getTestResult
    },
    isLoading () {
      return this.$store.getters.getTestResultLoading
    },
    isEmpty () {
      return !this.$store.getters.getMenuVisible('tests_result')
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
    reloadMenu: function () {
      this.$store.dispatch('fetchTestsResult')
    },
    reloadCurrent: function () {
      this.$store.dispatch('fetchTestResult', this.$route.params.id || '')
    }
  },
  beforeMount () {
    if (this.isCurrentAdmin) {
      this.$router.push({name: 'test_results', params: {id: this.$route.params.i}})
    }
    this.reloadMenu()
    this.reloadCurrent()
  }
}
</script>

<style lang='css' scoped>
</style>
