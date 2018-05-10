<template lang="pug">
  div
    div.row.justify-center(style="margin-top: 5px;")
      div.card.col-10
        div.row.main-info
          div.col-2.avatar-wrapper
            img.avatar(src="/static/avatar.jpg")
          div.col-9.info-wrapper
            p.title kastnerorz
            p.subtitle 2018-5-7
        hr.horizontal-separator
        div.contact-info
          p.subtitle Phone
          p.title 1810178956


        
          
          //- div.media
          //-   div.media-left
          //-     img.image.is-48x48.is-rounded(src="")
          //-   div.media-content
          //-     p.title.is-4 招领人
          //-     p.subtitle.is-6 2018-5-7
          //- div.content
          //-   p.subtitle.is-6 Phone
          //-   p.title 18101978956
          //-   hr(style="margin: 0")
          //-   p.subtitle.is-6 Email
          //-   p.title kastnerorz@gmail.com
          //-   p.subtitle.is-6 QQ
          //-   p.title 1171399571
    //- div.row.justify-center(style="margin-top: 5px;")
    //-   div.card.col-11


    

    div(style="position:fixed;bottom:0;width:100vw;background-color:#ccc;height:3rem;display:flex;justify-content:space-around;padding:1rem;box-sizing:border-box;")
      div(style="flex:1;display:flex;")
        div(style="flex:1;") 收藏
        div(style="flex:1;") share
      div(style="flex:1;text-align:right;") 18800000000
</template>
<script>
export default { }
</script>
<style scoped>

.card {
  background-color: white;
  /* padding: 11px 16px 11px 16px; */
  box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
  border-radius: 8px;
  margin: 0 0 10px 0;
}
.avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
}

.main-info {
  padding: 11px 16px 0 16px;
}

.contact-info {
  padding: 11px 0 11px 16px;  
}
.info-wrapper {
  padding: 0 0 0 10px;
}

.title {
  font-weight: bold;
  padding-top: 3px;
  font-size: 16px;
}

.subtitle {
  padding-top: 3px;
  color: grey;
  font-size: 14px
}

.horizontal-separator {
  border: 1px solid grey;
}
</style>
