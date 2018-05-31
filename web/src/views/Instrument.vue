<template>
  <freq v-if      ="this.$route.params.id === 'monogram'" count="1"/>
  <freq v-else-if ="this.$route.params.id === 'bigram'  " count="2"/>
  <freq v-else-if ="this.$route.params.id === 'trigram' "s count="3"/>
  <empty v-else/>
</template>

<script>
import 'vue-form-generator/dist/vfg-core.css'
import Freq from '../components/Freq'
import Empty from '../components/Empty'

export default {
  name: 'Instruments',
  components: {
    freq: Freq,
    empty: Empty
  },
  data () {
    return {
    }
  }
}
</script>

<style lang='css' scoped>
</style>
