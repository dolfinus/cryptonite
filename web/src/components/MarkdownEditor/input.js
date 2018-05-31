import Quill from 'quill'
import Parchment from 'parchment'
let Embed = Quill.import('blots/embed')

class InputBlot extends Embed {
  constructor (node) {
    super(node)
    this.contentNode.remove()
    this.leftGuard.remove()
    this.rightGuard.remove()

    if (this.domNode !== undefined) {
      this.inputNode = document.createElement('input')
      this.domNode.setAttribute('contenteditable', false)
      this.domNode.appendChild(this.inputNode)

      const checkableEventHandler = (e) => {
        if (e.target.type === 'checkbox') {
          if (e.target.checked) {
            e.target.setAttribute('checked', true)
          } else {
            e.target.removeAttribute('checked')
          }
        } else {
          if (e.target.checked) {
            let otherItems = e.target.closest('ul').querySelectorAll(`input[type=${e.target.type}][name=${e.target.name}]`)
            for (let i = 0; i < otherItems.length; ++i) {
              let radio = otherItems[i]
              radio.removeAttribute('checked')
            }
          }
          e.target.setAttribute('checked', e.target.checked)
        }
        e.target.closest('.ql-container').__quill.emitter.emit('text-change')
      }

      this.domNode.addEventListener('touchend', checkableEventHandler)
      this.domNode.addEventListener('click', checkableEventHandler)
    }
  }

  format (name, value) {
    if (name === 'checked' && (value === 'true' || value === true || value === '')) {
      this.inputNode.setAttribute(name, value)
    }
    if (name === 'type' || name === 'value' || name === 'name') {
      this.inputNode.setAttribute(name, value)
    }
  }

  static value (node) {
    let val = node.getAttribute('checked')
    return (val === 'true' || val === true || val === '')
  }

  static formats (node) {
    var children
    for (let i = 0; i < node.childNodes.length; ++i) {
      let child = node.childNodes[i]
      if (child.tagName === 'INPUT') {
        children = child
      }
    }
    return {
      type:    children.getAttribute('type'),
      name:    children.getAttribute('name'),
      value:   children.getAttribute('value'),
      checked: this.value(children)
    }
  }
}
InputBlot.blotName = 'input'
InputBlot.tagName = 'SPAN'

var typeAttribute = new Parchment.Attributor.Attribute('type', 'type', {
  scope: Parchment.Scope.INLINE_ATTRIBUTE
})
var checkedAttribute = new Parchment.Attributor.Attribute('checked', 'checked', {
  scope: Parchment.Scope.INLINE_ATTRIBUTE
})
var contenteditableAttribute = new Parchment.Attributor.Attribute('contenteditable', 'contenteditable', {
  scope: Parchment.Scope.INLINE_ATTRIBUTE
})
var nameAttribute = new Parchment.Attributor.Attribute('name', 'name', {
  scope: Parchment.Scope.INLINE_ATTRIBUTE
})
var valueAttribute = new Parchment.Attributor.Attribute('value', 'value', {
  scope: Parchment.Scope.INLINE_ATTRIBUTE
})
export default InputBlot
export { InputBlot, typeAttribute, checkedAttribute, contenteditableAttribute, nameAttribute, valueAttribute }
