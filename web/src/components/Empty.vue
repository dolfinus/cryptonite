<template>
  <section class="centered-item">
    <span class="">
      {{content || $t('placeholder.not_selected')}}
    </span>
  </section>
</template>

<script>

export default {
  name: 'Empty',
  props: ['content'],
  data () {
    return {
    }
  }
}
</script>

<style lang='sass' scoped>
</style>
