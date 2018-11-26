import http from '../http'
export default {
  getPosts: function() {
    http.get()
    return [
      {
        id: '123123',
        tittle: '',
        descrption: '',
        longtitude: '',
        latitude: '',
        location: ''
      }
    ]
  },
  addNewPost: function(post) {},
  modifyPost: function(payload) {}
}
