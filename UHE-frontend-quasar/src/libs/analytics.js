/* eslint-disable */
export default {
  logEvent(category, action, label, sessionId = 'UA-111372547-1') {
    dataLayer.push({
      appEventCategory: category,
      appEventAction: action,
      appEventLabel: label,
      sessionId: sessionId
    })
    dataLayer.push({ event: 'appEvent' })
  },
  logPage(path, name, sessionId = 'UA-111372547-1') {
    dataLayer.push({
      screenPath: path,
      screenName: name,
      sessionId: sessionId
    })
    dataLayer.push({ event: 'appScreenView' })
  }
}
