
export default {
  theme: 'snow',
  boundary: document.body, 
  modules: {
    toolbar: [
      //[{'history': 'undo'}, {'history': 'redo'}],
      [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      ['blockquote', 'code-block'],
      [{ 'list': 'ordered' }, { 'list': 'bullet' }],
      [{ 'script': 'sub' }, { 'script': 'super' }],
      [{ 'indent': '-1' }, { 'indent': '+1' }],
      [{ 'align': '' }, { 'align': 'center' }, { 'align': 'right' }, {'align': 'justify'}],
      //['formula'],
      ['link', 'image', 'video'],
      ['clean'],
      //['tasklist'],
      [{ 'table': ['newtable_1_1', 'newtable_2_2', 'newtable_3_3', 'newtable_4_4', 'newtable_5_5'] }],
      [{ 'table': 'append-row' }],
      //[{ 'table': 'remove-row' }],
      [{ 'table': 'append-col' }]
      //[{ 'table': 'remove-col' }],
      //[{ 'table': 'remove-table' }]
    ],
    //formula: true,
    history: {
      delay: 2000,
      maxStack: 500,
      userOnly: true
    },
    clipboard: {
      matchVisual: false
    },
    table: true
  },
  readOnly: false
}
