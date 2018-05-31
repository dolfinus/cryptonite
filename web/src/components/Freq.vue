<template>
    <section class="column">
    <div class="card">
      <div class="card-content">
        <chart ref="chart" type="bar" :data.sync="dataChart" :options.sync="chartOptions">
        </chart>
        <form ref="form" name="freq">
          <div class="content columns">
            <div class="field column">
              <p class="control">
                <textarea class="textarea" v-model.trim="input_text"></textarea>
              </p>
              <a class="button is-success is-outlined" :href.sync="xlsx" :download.sync="filename">
                <span class="icon is-small">
                  <i class="fa fa-download"></i>
                </span>
                <span v-t="'button.download'"></span>
              </a>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import Chart from 'vue-bulma-chartjs'
import 'chartjs-plugin-zoom'

var ColorHash = require('color-hash')
const colorHash = new ColorHash()

export default {
  name: 'Freq',
  props: ['count'],
  components: {
    chart: Chart
  },
  data () {
    return {
      input_text: '',
      chartOptions: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        legend: {
          display: false
        },
        height: 300,
        pan: {
          enabled: true,
          mode: 'xy'
        },
        zoom: {
          enabled: true,
          mode: 'x'
        },
        title: this.title
      },
      formOptions: {
        validateAfterLoad: false,
        validateAfterChanged: true
      },
      chart : null
    }
  },
  computed: {
    dataChart () {
      let config = {
        labels: this.labels,
        datasets: [{
          data: this.columns,
          backgroundColor: this.colored(this.labels)
        }]
      }
      return config
    },
    filename () {
      if (this.$props.count === '1') {
        return 'chars.xslx'
      }
      if (this.$props.count === '2') {
        return 'bigrams.xslx'
      }
      if (this.$props.count === '3') {
        return 'trigrams.xslx'
      }
      return 'unknown.xslx'
    },
    title () {
      let config = {display: true, text: ''}
      if (this.$props.count === '1') {
        config.text = this.$t('instruments.monogram')
      } else if (this.$props.count === '2') {
        config.text = this.$t('instruments.bigram')
      } else if (this.$props.count === '3') {
        config.text = this.$t('instruments.trigram')
      } else {
        config.display = false
      }
      return config
    },
    labels () {
      return Array.from(Object.keys(this.json).sort())
    },
    columns () {
      let json   = this.json
      let labels = this.labels
      return Array.from(labels.map((char) => json[char] ))
    },
    json () {
      let text    = this.input_text
      let letters = {}
      let count   = +this.$props.count
      for (let i = 0; i < text.length - (count - 1); ++i) {
        let char = text[i]
        if (count > 1) {
          char += text[i+1]
          if (count > 2) {
            char += text[i+2]
          }
        }
        if (!letters[char]) {
          letters[char] = 0
        }
        letters[char] += 1
      }
      return letters
    },
    xlsx () {
      let html = '<tr><th>Char</th><th>Freq</th></tr>'
      for (let i = 0; i < this.labels.length; ++i) {
        let char  = this.labels[i]
        let value = this.columns[i]
        html += '<tr><td>'+char+'</td><td>'+value+'</td></tr>'
      }
      html += '<tr><td>Total</td><td>'+this.columns.reduce((prev, next) => prev + next, 0)+'</td></tr>'
      return this.html2excel(html, 'Bigram')
    },
    chrt () {
      return this.input_text
    }
  },
  watch: {
    '$route' (to, from) {
      this.reload()
    },
    chrt (to, from) {
      this.reload()
    }
  },
  methods: {
    reload () {
      this.$nextTick(() => {
        if (this.$refs.chart) {
          this.$refs.chart.resetChart()
        }
      })
    },
    colored (arr) {
      return arr.map((char) => { return colorHash.hex(char) })
    }
  },
  mounted () {
    this.reload()
  }
}
</script>

<style lang="sass" scoped>


</style>
