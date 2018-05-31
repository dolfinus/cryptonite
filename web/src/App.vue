<template>
<div>
    <nav>
        <router-view name="navbar"></router-view>
        <router-view name="subnavbar"></router-view>
    </nav>
    <section class="section columns">
      <router-view name="menu"></router-view>
      <transition name="fade">
        <router-view name="main" class="column"></router-view>
      </transition>
    </section>
</div>
</template>

<script>

export default {
  name: '',
  computed: {
    isLoading () {
      return this.$store.state.isLoading
    }
  }
}
</script>

<style lang="sass">
@media print
  html, body
    display: none

@media (max-width: 1024px)
  .only-desktop
    display: none!important

@media (min-width: 1024px)
  .only-mobile
    display: none!important

.navbar-item
  padding: 0

.section
  padding-top: 1.5em!important
  padding-bottom: 1.5em!important

.quill-editor
  width: 100%
  height: 100%
  .ql-editor
    height: 100%!important
    max-height: 61vh!important
    overflow-y: scroll!important
    ul
      > li:contains(input[type=checkbox])
        &::before
          content: ''
fieldset
  border: none!important
ul.card-content
  padding-top: 0.3em!important
  padding-bottom: 0.3em!important
.add-item, .remove-item
  float: right
.add-item 
  color: green
.remove-item
  color: red
  padding-left: 0.3em

.centered-item
  text-align: center!important
  margin-top: auto!important
  margin-bottom: auto!important
  margin-left: auto!important
  margin-right: auto!important
.new-item
  color: green

input[disabled=disabled]
  background-color: #eee!important
input[readonly=readonly]
  color: #999!important
.actions a:nth-child(1)
  display: none

.is-max-width
  width: 100%
.vue-form-generator .form-group.disabled > label
  font-style: normal!important

.navbar-dropdown a.navbar-item
  padding-right: 2em!important

.navbar-burger
  margin-left: 0!important
  float: right!important

  .navbar-link
    padding: 1em!important

    width: 2.5em!important
    height: 2.5em!important
.navbar
  .breadcrumb
    margin-top: 0!important
    margin-bottom: 0!important

</style>
