<template>
  <div class="quill-editor">
    <slot name="toolbar"></slot>
    <div ref="editor"></div>
    <textarea ref="textarea" :name="schema.id !== undefined ? 'content_' + schema.id : 'content'" class="form-control is-hidden" type="text" :value="value"></textarea>
  </div>
</template>

<script>
  // require sources
  import _Quill from 'quill'
  import defaultOptions from './options'
  // import katex from 'katex'
  import TurndownService from 'turndown'
  import MarkdownIt from 'markdown-it'
  import { abstractField } from 'vue-form-generator'
  import { gfm } from './td'
  import { TableCell, TableRow, Table, Contain } from 'quill-table'
  import TableModule from './table'
  import { InputBlot, typeAttribute, checkedAttribute, contenteditableAttribute, nameAttribute, valueAttribute } from './input'

  _Quill.register(typeAttribute)
  _Quill.register(checkedAttribute)
  _Quill.register(contenteditableAttribute)
  _Quill.register(nameAttribute)
  _Quill.register(valueAttribute)
  _Quill.register(InputBlot)
  _Quill.register(TableCell)
  _Quill.register(TableRow)
  _Quill.register(Table)
  _Quill.register(Contain)
  _Quill.register('modules/table', TableModule)

  let empty_handler = (e) => { e.preventDefault() }

  let td = new TurndownService({
    blankReplacement (content, node) {
      const types = ['IFRAME']
      if (types.indexOf(node.nodeName) !== -1) {
        return `\n\n${node.outerHTML}\n\n`
      } else {
        const output = []
        node.childNodes.forEach((child) => {
          if (types.indexOf(child.nodeName) !== -1) {
            output.push(child.outerHTML)
          }
        })
        if (output.length) {
          return '\n\n' + output.join('\n\n') + '\n\n'
        } else {
          return node.isBlock ? '\n\n' : ''
        }
      }
    }
  }).keep(['iframe', 'input']).remove(['script'])

  td.use(gfm)

  let md = new MarkdownIt()
  md.use(require('./checkbox'))
  md.set({
    html: true
  })

  const Quill = window.Quill || _Quill
  // window.katex = katex
  window.td = td
  window.md = md

  // pollfill
  if (typeof Object.assign !== 'function') {
    Object.defineProperty(Object, 'assign', {
      value (target, varArgs) {
        if (target == null) {
          throw new TypeError('Cannot convert undefined or null to object')
        }
        const to = Object(target)
        for (let index = 1; index < arguments.length; index++) {
          const nextSource = arguments[index]
          if (nextSource != null) {
            for (const nextKey in nextSource) {
              if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
                to[nextKey] = nextSource[nextKey]
              }
            }
          }
        }
        return to
      },
      writable: true,
      configurable: true
    })
  }

  function clp_clear () {
    var clipboard = window.clipboardData
    if (clipboard) {
      var content = window.clipboardData.getData('Text')
      if (content == null) {
        window.clipboardData.clearData()
      }
    }
    setTimeout(clp_clear, 1000)
  }

  // export
  export default {
    name: 'quill-editor',
    mixins: [ abstractField ],
    data () {
      return {
        _options: {},
        _content: '',
        defaultOptions
      }
    },
    props: {
      content: String,
      disabled: {
        type: Boolean,
        default: false
      },
      readonly: {
        type: Boolean,
        default: false
      },
      options: {
        type: Object,
        required: false,
        default: () => ({})
      },
      globalOptions: {
        type: Object,
        required: false,
        default: () => ({})
      }
    },
    mounted () {
      this.initialize()
    },
    beforeDestroy () {
      this.quill = null
      delete this.quill
    },
    methods: {
      // Init Quill instance
      initialize () {
        if (this.$el) {
          this._options = Object.assign({placeholder: this.$t('placeholder.content')}, this.defaultOptions, this.globalOptions, this.options, this.schema.options)

          if (this.disabled) {
            this._options.modules.toolbar = []
          }

          // Instance
          this.quill = new Quill(this.$refs.editor, this._options)
          this.quill.enable(false)

          // Disabled editor
          if (!this.disabled) {
            this.quill.enable(true)
          }

          if (this.disabled) {
            this.$refs.editor.parentNode.querySelector('.ql-toolbar').remove()
            this.$refs.editor.addEventListener('selectstart', empty_handler)
            this.$refs.editor.addEventListener('selectend',   empty_handler)
            this.$refs.editor.addEventListener('contextmenu', empty_handler)
            this.$refs.editor.addEventListener('keydown',     empty_handler)
            this.$refs.editor.addEventListener('keyup',       empty_handler)
          }

          if (this.readonly || this.schema.readonly) {
            this.$refs.editor.addEventListener('mousedown',   empty_handler)
            this.$refs.editor.addEventListener('mouseup',     empty_handler)
            this.$refs.editor.addEventListener('click',       empty_handler)
            this.$refs.editor.addEventListener('dblclick',    empty_handler)
            this.$refs.editor.addEventListener('touchstart',  empty_handler)
            this.$refs.editor.addEventListener('touchend',    empty_handler)
            this.$refs.editor.addEventListener('touchcancel', empty_handler)

            clp_clear()
          }

          if (this.value || this.content) {
            this.quill.clipboard.dangerouslyPasteHTML(md.render(this.value || this.content) + '\n')
          }

          // Mark model as touched if editor lost focus
          this.quill.on('selection-change', range => {
            if (!range) {
              this.$emit('blur', this.quill)
            } else {
              this.$emit('focus', this.quill)
            }
          })

          /*
          var toolbar = this.quill.getModule('toolbar')
          toolbar.addHandler('table', function () {
            this.quill.clipboard.in
            console.log('table')
          })
          */
          // Update model if text changes
          this.quill.on('text-change', (delta, oldDelta, source) => {
            let html = this.$refs.editor.children[0].innerHTML
            if (html === '<p><br></p>') html = ''
            if (html === '<p></p>') html = ''
            const quill = this.quill
            const text = this.quill.getText()
            let markdown = td.turndown(html)
            this.$refs.textarea.value = markdown
            let rendered = md.render(markdown).replace('<br><br>', '<br>')
            this._content = rendered
            this.$emit('input', this._content)
            this.$emit('change', { rendered, text, quill })
          })

          // Emit ready event
          this.$emit('mounted', this.quill)
        }
      }
    },
    watch: {
      // Watch content change
      value (newVal, oldVal) {
        if (this.quill) {
          if (newVal) {
            let rendered = md.render(newVal)
            if (rendered !== this._content) {
              this.quill.clipboard.dangerouslyPasteHTML(rendered + '\n')
              if (this.readonly || this.schema.readonly) {
                console.log('readonly')
                let els = this.$refs.editor.querySelectorAll('.ql-editor > *')
                for (var el of els) {
                  el.style.cursor = 'default'
                }
              }
            }
          } else if (!newVal) {
            this.quill.setText('')
          }
        }
      },
      content (newVal, oldVal) {
        if (this.quill) {
          if (newVal) {
            let rendered = md.render(newVal)
            if (rendered !== this._content) {
              this.quill.clipboard.dangerouslyPasteHTML(rendered + '\n')
            }
          } else if (!newVal) {
            this.quill.setText('')
          }
        }
      }
    }
  }
</script>

<style lang='sass' scoped>
</style>
