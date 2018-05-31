<template>
  <nav class="column is-2" v-if="isShow">
    <aside class="menu card" v-for="category in categories" v-bind:key="category.id"  v-bind:class="{'is-loading': isLoading}">
      <p class="menu-label card-header card-header-title">
        {{category.title && !$props.category_translate ? category.title : $t($props.type + '.'+ category.id)}}
      </p>
      <ul class="menu-list card-content">
        <li v-for="item in category.items" v-bind:key="item.id">
        <router-link :to="item_link(item.id)" activeClass="is-active">
          {{item.name && !$props.item_translate ? item.name : $t($props.one_item + '.'+ item.id)}}
        </router-link>
        </li>
      </ul>
    </aside>
  </nav>
</template>

<script>

export default {
  name: 'Menu',
  props: ['type', 'one_item', 'preload', 'category_translate', 'item_translate'],
  data () {
    return {
    }
  },
  computed: {
    categories () {
      return this.$store.getters.getMenuContent(this.$props.type)
    },
    isLoading () {
      return this.$store.getters.getMenuLoading(this.$props.type)
    },
    isShow () {
      return this.$store.getters.getMenuVisible(this.$props.type)
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.name !== from.name && this.categories === []) {
        this.reload()
      }
    }
  },
  methods: {
    item_link (item) {
      if (this.$props.one_item) {
        return { name: this.$props.one_item, params: {id: item} }
      } else {
        return { name: item }
      }
    },
    reload: function () {
      let items = this.$props.type.split('_')
      let itemsName = ''
      items.forEach((item) => {
        itemsName += item.capitalize()
      })
      console.log(itemsName)
      console.log(this.$props.preload)
      this.$store.dispatch('fetch' + itemsName, this.$props.preload).then(
        this.$forceUpdate()
      )
    }
  },
  mounted () {
    this.reload()
  }
}
</script>

<style lang="sass" scoped>
menu-label
  padding: 0.95rem
  margin-bottom: 0
column
  padding-top: 0
</style>
