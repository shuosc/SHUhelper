/* eslint-disable */
export default {
  logEvent(category, action, label, sessionId = null) {
    dataLayer.push({
      appEventCategory: category,
      appEventAction: action,
      appEventLabel: label
    })
    dataLayer.push({
      event: 'appEvent'
    })
  },
  logPage(path, name, sessionId = null) {
    dataLayer.push({
      screenPath: path,
      screenName: name
    })
    dataLayer.push({
      event: 'appScreenView'
    })
  },
  loginUser(id) {
    window.uid = id
  }
}
