/* eslint-disable */
export default {
  logEvent(category, action, label, sessionId) {
    dataLayer.push({
      appEventCategory: category,
      appEventAction: action,
      appEventLabel: label,
      sessionId: sessionId
    })
    dataLayer.push({
      event: 'appEvent'
    })
  },
  logPage(path, name, sessionId) {
    dataLayer.push({
      screenPath: path,
      screenName: name,
      sessionId: sessionId
    })
    dataLayer.push({
      event: 'appScreenView'
    })
  },
  loginUser(id) {
    ga('set', 'userId', id);
  }
}
