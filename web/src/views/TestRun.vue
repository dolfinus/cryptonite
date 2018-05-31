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
          <div class="field is-grouped">
            <p class="control">
              <router-link tag="a" v-if="this.test.is_finished" class="navbar-item" :to="{ name: 'test_result', params: {id: this.$route.params.id}}">
              <a class="button is-info">
                <span v-t="'button.results'"/>
                <span class="icon is-small">
                  <i class="fas fa-redo"></i>
                </span>
              </a>
              </router-link>
              <a v-if="!this.test.is_finished && this.test.begin" class="button is-warning" @click.prevent="onRun">
                <span v-t="'button.continue'"/>
                <span class="icon is-small">
                  <i class="fa fa-play"></i>
                </span>
              </a>
              <a v-else-if="!this.test.is_finished" class="button is-success" @click.prevent="onRun">
                <span v-t="'button.run'"/>
                <span class="icon is-small">
                  <i class="fa fa-play"></i>
                </span>
              </a>
            </p>
          </div>
        </form>
      </div>
    </div>
  </section>
  <empty v-else-if="isEmpty" :content="$t('placeholder.no_tests')"/>
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
        max_duration: this.test.max_duration,
        begin:       (this.test.begin ? this.test.begin : null),
        end:         (this.test.end   ? this.test.end   : null),
        items_count:  this.test.items_count,
        state:       (this.test.is_finished ? this.$t('label.finished') : (this.test.begin ? this.$t('label.running') : this.$t('label.not_started')))
      }
      return config
    },
    schema () {
      let result = [
        {
          type: 'input',
          model: 'state',
          inputName: 'state',
          inputType: 'text',
          label: this.$t('label.state'),
          disabled: true,
          readonly: true
        },
        {
          type: 'input',
          inputName: 'items_count',
          inputType: 'text',
          model: 'items_count',
          label: this.$t('label.questions_count'),
          disabled: true,
          readonly: true
        },
        {
          type: 'input',
          inputName: 'max_duration',
          inputType: 'number',
          model: 'max_duration',
          label: this.$t('label.max_duration'),
          disabled: true,
          readonly: true
        },
        {
          type: 'input',
          inputName: 'begin',
          inputType: 'text',
          model: 'begin',
          label: this.$t('label.begin'),
          disabled: true,
          readonly: true
        },
        {
          type: 'input',
          inputName: 'end',
          inputType: 'text',
          model: 'end',
          label: this.$t('label.end'),
          disabled: true,
          readonly: true
        }
      ]

      return {
        fields: result
      }
    },
    tests () {
      return this.$store.getters.getTestsRun
    },
    test () {
      return this.$store.getters.getTestRun
    },
    isLoading () {
      return this.$store.getters.getTestRunLoading
    },
    isEmpty () {
      return !this.$store.getters.getMenuVisible('tests_run')
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
    onRun: function () {
      this.$router.push({name: 'test_item_run', params: {id: this.$route.params.id, item: this.test.last_item || 1}})
    },
    reloadMenu: function () {
      this.$store.dispatch('fetchTestsRun')
    },
    reloadCurrent: function () {
      this.$store.dispatch('fetchTestRun', this.$route.params.id || '')
    }
  },
  beforeMount () {
    this.reloadMenu()
    this.reloadCurrent()
  }
}
</script>

<style lang='css' scoped>
</style>
