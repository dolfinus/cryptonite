<template>
    <section class="column">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{test.name}}
        </p>
      </header>
      <div class="card-content">
        <form ref="form" name="test_run">
          <vue-form-generator :schema="schema" :model="model" :options="formOptions"/>
          <div class="field is-grouped">
            <span class="control">{{this.time}}</span>
            <span class="control">{{this.end}}</span>
          </div>
          <div class="field is-grouped">
            <p class="control">
              <a class="button is-danger is-outlined" @click.prevent="onEnd">
                <span class="icon is-small">
                  <i class="fa fa-times"></i>
                </span>
                <span v-t="'button.close'"/>
              </a>
            </p>
            <p class="control">
              <a class="button is-warning" @click.prevent="onSkip">
                <span class="icon is-small">
                  <i class="fa fa-step-forward"></i>
                </span>
                <span v-t="'button.skip'"/>
              </a>
            </p>
            <p class="control">
              <a class="button is-success" @click.prevent="onSave">
                <span v-t="'button.next'"/>
                <span class="icon is-small">
                  <i class="fa fa-check"></i>
                </span>
              </a>
            </p>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script>

const time_format = 'HH:mm:ss'

export default {
  name: 'TestRunItem',
  props: ['id', 'item'],
  data () {
    return {
      now: this.$moment(),
      formOptions: {
        validateAfterLoad: false,
        validateAfterChanged: true
      }
    }
  },
  computed: {
    model () {
      let config = {
        item_no: this.$route.params.item,
        name:    this.test.name,
        content: this.test.item ? this.test.item.content : ''
      }
      return config
    },
    schema () {
      let result = [{
        type: 'md-editor',
        inputName:'md_editor',
        model: 'content',
        required: true,
        label: '#' + (this.$route.params.item),
        disabled: true,
        id: 0
      }]
      return {
        fields: result
      }
    },
    test () {
      return this.$store.getters.getTestRun
    },
    isLoading () {
      return this.$store.getters.getTestRunLoading
    },
    time () {
      return this.$t('label.current', {time: this.$moment.duration(this.begin_time).format(time_format)})
    },
    end () {
      let end   = this.end_time
      let now   = this.now
      if (end !== null) {
        return this.$t('label.to_end', {time: this.$moment.duration(end.diff(now)).format(time_format)})
      }
    },
    begin_time () {
      let begin     = this.$moment(this.test.begin)
      let now       = this.now
      return now.diff(begin)
    },
    end_time () {
      if (!this.test.begin) {
        return null
      }
      if (!this.test.max_duration || !this.test.not_after) {
        return null
      }
      let begin     = this.$moment(this.test.begin)
      let now       = this.now

      let end, not_after
      if (this.test.not_after) {
        not_after = this.$moment(this.test.not_after)
      } else {
        not_after = now
      }
      if (this.test.max_duration) {
        end       = begin.add(this.test.max_duration, 'minutes')
      } else {
        end       = now
      }
      if (not_after.diff(end) > 0) {
        return end
      } else {
        return not_after
      }
    }
  },
  watch: {
    '$store' (to, from) {
      this.reload()
    },
    '$route' (to, from) {
      this.reload()
    }
  },
  methods: {
    onSave: function () {
      console.log(0)
      const formData = new FormData(this.$refs.form)
      var data = {}
      var items = []
      var format = /content_(\d+)/i
      for (var [key, value] of formData.entries()) {
        let matches = key.match(format)
        if (matches !== null) {
          data.answer = value
        } else {
          data[key] = value
        }
      }
      let reload = this.reload
      let redirect_next   = this.redirectNext
      let redirect_result = this.redirectResult
      this.$store.dispatch('saveTestItemResult', [this.$route.params.id, this.$route.params.item, data]).then(redirect_result).then(redirect_next).then(reload)
    },
    onSkip: function () {
      let reload = this.reload
      let redirect_next   = this.redirectNext
      let redirect_result = this.redirectResult
      redirect_result().then(redirect_next).then(reload)
    },
    onEnd: function () {
      let redirect = this.redirectResult
      this.$store.dispatch('saveTestItemResult', [this.$route.params.id, this.test.items_count, {}]).then(redirect)
    },
    redirectLast: function () {
      console.log(1, this.test.last_item)
      if (!this.test.is_finished && (this.test.last_item || 1) <= this.test.items_count) {
        this.$router.push({name: 'test_item_run', params: {id: this.$route.params.id, item: this.test.last_item || 1}})
      } else {
        this.$router.push({name: 'test_result', params: {id: this.$route.params.id}})
      }
    },
    redirectNext: function () {
      console.log(2, +this.$route.params.item + 1)
      if ((+this.$route.params.item) > this.test.items_count || (+this.test.last_item) > this.test.items_count || this.test.is_finished) {
        this.$router.push({name: 'test_result', params: {id: this.$route.params.id}})
      } else {
        this.$router.push({name: 'test_item_run', params: {id: this.$route.params.id, item: +this.$route.params.item + 1}})
      }
    },
    redirectResult: function () {
      console.log(3, this.test.items_count, this.test.last_item, this.test.is_finished)
      if ((+this.$route.params.item) > this.test.items_count || (+this.test.last_item) > this.test.items_count || this.test.is_finished) {
        this.$router.push({name: 'test_result', params: {id: this.$route.params.id}})
      }
    },
    reloadItem: function () {
      console.log(4)
      if (!this.test.is_finished) {
        this.$store.dispatch('fetchTestItemRun', [this.$route.params.id, this.$route.params.item])
        window.setInterval(() => {
          this.now = this.$moment()
        }, 1000)
      }
    },
    reload: function () {
      console.log(5)
      let redirect_last   = this.redirectLast
      let redirect_result = this.redirectResult
      let reload_item     = this.reloadItem
      this.$store.dispatch('fetchTestRun', this.$route.params.id).then(redirect_result).then(redirect_last).then(reload_item)
    }
  },
  mounted () {
    if (this.$route.params.item === undefined) {
      this.$router.push({name: 'test_run', params: {id: this.$route.params.id}})
    } else {
      this.reload()
    }
  }
}
</script>

<style lang='css' scoped>
</style>
