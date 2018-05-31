String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1)
}

export default {
  methods: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },
    base64: function (str) {
      return window.btoa(unescape(encodeURIComponent(str)))
    },
    html2excel: function (html, name) {
      let prefix = 'data:application/vnd.ms-excel;base64,'
      let content = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>' + (name || 'Worksheet') + '</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>'+ html +'</table></body></html>'
      return prefix + this.base64(content)
    }
  }
}
