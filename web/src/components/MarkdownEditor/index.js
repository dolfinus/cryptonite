import _Quill from 'quill'
import mdEditor from './editor.vue'

const Quill = window.Quill || _Quill
const install = (Vue, globalOptions) => {
  if (globalOptions) {
    mdEditor.props.globalOptions.default = () => globalOptions
  }
  Vue.component(mdEditor.name, mdEditor)
}

const VueMdEditor = { Quill, mdEditor, install }

export default VueMdEditor
export { Quill, mdEditor, install }
