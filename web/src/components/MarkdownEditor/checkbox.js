let _, checkboxReplace

_ = require('underscore')

checkboxReplace = function (md, options, Token) {
  'use strict'
  var arrayReplaceAt, createTokens, defaults, lastCheckboxId, lastRadioId, lastParentId, pattern, splitTextToken, prevType, alreadyChecked, incParent
  arrayReplaceAt = md.utils.arrayReplaceAt
  lastCheckboxId = 0
  lastRadioId = 0
  lastParentId = 0
  alreadyChecked = false
  prevType = 'radio'
  defaults = {
    divWrap: false,
    divClass: 'checkbox',
    checkboxNamePrefix: 'checkbox',
    radioNamePrefix: 'radio'
  }
  options = _.extend(defaults, options)
  pattern = /(\[|\()(X|\s|_|-|\*)(\]|\))\s(.*)/i
  createTokens = function (checked, type, label, Token) {
    var checkboxId, radioId, parentId, checkboxPrefixedId, radioPrefixedId, parentPrefixedId, nodes, token
    nodes = []

    /**
     * <div class='checkbox'>
     */
    if (options.divWrap) {
      token = new Token('checkbox_open', 'div', 1)
      token.attrs = [['class', options.divClass]]
      nodes.push(token)
    }

    token = new Token('contenteditable_open', 'span', 1)
    token.attrs = [['contenteditable', 'false']]
    nodes.push(token)
    /**
     * <input type='checkbox' id='checkbox{n}' checked='true'>
     */
    checkboxId = lastCheckboxId
    radioId = lastRadioId
    parentId = lastParentId
    checkboxPrefixedId = options.checkboxNamePrefix + checkboxId
    radioPrefixedId = options.radioNamePrefix + radioId
    parentPrefixedId = options.radioNamePrefix + parentId
    token = new Token('checkbox_input', 'input', 0)
    token.attrs = [['type', type]]
    if (type === 'checkbox') {
      lastCheckboxId += 1
      token.attrs.push(['name', checkboxPrefixedId])
      token.attrs.push(['id', checkboxPrefixedId])
    }
    if (type === 'radio') {
      lastRadioId += 1
      token.attrs.push(['name', parentPrefixedId])
      token.attrs.push(['id', radioPrefixedId])
      token.attrs.push(['value', radioId])
    }
    if (checked === true) {
      token.attrs.push(['checked', 'true'])
    }
    nodes.push(token)

    token = new Token('contenteditable_close', 'span', -1)
    nodes.push(token)

    /**
     * <label for='checkbox{n}'>
     */
    token = new Token('label_open', 'label', 1)
    token.attrs = []
    if (type === 'checkbox') {
      token.attrs.push(['for', checkboxPrefixedId])
    }
    if (type === 'radio') {
      token.attrs.push(['for', radioPrefixedId])
    }
    nodes.push(token)

    /**
     * content of label tag
     */
    token = new Token('text', '', 0)
    token.content = label
    nodes.push(token)

    /**
     * closing tags
     */
    nodes.push(new Token('label_close', 'label', -1))
    if (options.divWrap) {
      nodes.push(new Token('checkbox_close', 'div', -1))
    }
    return nodes
  }
  splitTextToken = function (original, Token) {
    var checked, label, matches, text, bracket, type, value
    text = original.content
    matches = text.match(pattern)
    if (matches === null) {
      return original
    }
    type      = 'checkbox'
    checked   = false
    incParent = false
    bracket   = matches[1]
    value     = matches[2]
    label     = matches[4]
    if (bracket === '(') {
      type = 'radio'
      if (prevType !== type) incParent = true
    }
    if (value === 'X' || value === 'x' || value === '*') {
      checked = true
    }
    if (type === 'radio' && !incParent && checked && alreadyChecked) {
      incParent = true
    }
  
    if (incParent) lastParentId += 1

    if (type === 'radio' && checked) {
      alreadyChecked = checked
    } else if (type === 'checkbox') {
      alreadyChecked = false
    }
    prevType = type
    return createTokens(checked, type, label, Token)
  }
  return function (state) {
    var blockTokens, i, j, l, token, tokens
    blockTokens = state.tokens
    j = 0
    l = blockTokens.length
    while (j < l) {
      if (blockTokens[j].type !== 'inline') {
        j++
        continue
      }
      tokens = blockTokens[j].children
      i = tokens.length - 1
      while (i >= 0) {
        token = tokens[i]
        blockTokens[j].children = tokens = arrayReplaceAt(tokens, i, splitTextToken(token, state.Token))
        i--
      }
      j++
    }
  }
}

module.exports = function (md, options) {
  'use strict'
  md.core.ruler.push('checkbox', checkboxReplace(md, options))
}
