<template>
    <section v-if="this.$route.params.id !== undefined">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{test.name}}
        </p>
      </header>
      <div class="card-content">
        <datatable :rows="results" :columns="columns" :title="$t('label.results')" printable="false"/>
      </div>
    </div>
  </section>
  <empty v-else/>
</template>

<script>
import DataTable from 'vue-materialize-datatable'
import Empty from '../components/Empty'

export default {
  name: 'TestRun',
  components: {
    datatable: DataTable,
    empty: Empty
  },
  data () {
    return {
    }
  },
  computed: {
    columns () {
      let result = [
        {label: this.$t('label.user_name'), field: 'fio',         clickable: false, html: true},
        {label: this.$t('label.begin'),     field: 'begin',       clickable: false, html: true},
        {label: this.$t('label.end'),       field: 'end',         clickable: false, html: true}
      ]
      for (var i = 0; i < this.test.items_count; ++i) {
        result.push({label: 'N'+(i+1), field: 'result_'+i, clickable: false, html: true})
      }
      result = result.concat([
        {label: this.$t('label.answers_count'), field: 'score',       clickable: false, html: true},
        {label: this.$t('label.percent'),       field: 'percent',     clickable: false, html: true},
        {label: this.$t('label.score'),         field: 'mark',        clickable: false, html: true},
        {label: this.$t('label.finished'),      field: 'is_finished', clickable: false, html: true}
      ])
      return result
    },
    currentUser () {
      return this.$store.getters.getCurrentUser
    },
    isCurrentAdmin () {
      return this.$store.getters.isCurrentAdmin
    },
    results () {
      return this.test.results
    },
    test () {
      return this.$store.getters.getTestResults
    },
    isLoading () {
      return this.$store.getters.getTestResultsLoading
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
      this.$store.dispatch('fetchTestsResults')
    },
    reloadCurrent: function () {
      this.$store.dispatch('fetchTestResults', this.$route.params.id || '')
    }
  },
  beforeMount () {
    if (!this.isCurrentAdmin) {
      this.$router.push({name: 'test_result', params: {id: this.$route.params.i}})
    }
    this.reloadMenu()
    this.reloadCurrent()
  }
}
</script>

<style lang='css' scoped>
</style>
