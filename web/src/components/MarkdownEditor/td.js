
import { highlightedCodeBlock, strikethrough, tables } from 'turndown-plugin-gfm'

function taskListItems (turndownService) {
  turndownService.addRule('taskListItems', {
    filter: function (node) {
      return (node.type === 'checkbox' || node.type === 'radio') && (node.parentNode.nodeName === 'LI' || node.parentNode.parentNode.nodeName === 'LI')
    },
    replacement: function (content, node) {
      if (node.type === 'checkbox') {
        return (node.checked ? '[x]' : '[ ]') + ' '
      } else if (node.type === 'radio') {
        return (node.checked ? '(*)' : '( )') + ' '
      }
    }
  })
}

let gfm = [
  highlightedCodeBlock,
  strikethrough,
  tables,
  taskListItems
]

export { gfm, highlightedCodeBlock, strikethrough, tables, taskListItems }