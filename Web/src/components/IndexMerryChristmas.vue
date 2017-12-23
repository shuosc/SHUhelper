<template>
    <div class="content">
        <p>
            <span class="a">M</span>
            <span class="b">e</span>
            <span class="c">r</span>
            <span class="d">r</span>
            <span class="e">y</span>
            <span class="f">&nbsp;</span>
            <span class="g">C</span>
            <span class="h">h</span>
            <span class="i">r</span>
            <span class="j">i</span>
            <span class="k">s</span>
            <span class="l">t</span>
            <span class="m">m</span>
            <span class="n">a</span>
            <span class="o">s</span>
        </p>
    </div>
</template>

<script>
export default {}
</script>

<style scoped>
.content {
  /* background: url(http://www.localnomad.com/de/blog/wp-content/uploads/2012/12/Christmas-tree.jpg); */
  background-size: cover;
  background-position: center;
  width: 100%;
  margin: 20px auto;
}

p {
  background: rgba(100, 100, 100, 0.3);
  padding: 10px 15px;
  /* margin-top: 45vh; */
  border: 1px solid #555;
  border-radius: 8px;
  text-align: center;
  font: bold 175% 'Mountains of Christmas', sans-serif;
}

span.a {
  color: orange;
  -webkit-animation: colorOne 1s infinite;
}
span.b {
  color: green;
  -webkit-animation: colorTwo 1s infinite;
}
span.c {
  color: chocolate;
  -webkit-animation: colorThree 1s infinite;
}
span.d {
  color: lightblue;
  -webkit-animation: colorFour 1s infinite;
}
span.e {
  color: darkgreen;
  -webkit-animation: colorFive 1s infinite;
}
span.g {
  color: orange;
  -webkit-animation: colorOne 1s infinite;
}
span.h {
  color: green;
  -webkit-animation: colorTwo 1s infinite;
}
span.i {
  color: chocolate;
  -webkit-animation: colorThree 1s infinite;
}
span.j {
  color: lightblue;
  -webkit-animation: colorFour 1s infinite;
}
span.k {
  color: darkgreen;
  -webkit-animation: colorFive 1s infinite;
}
span.l {
  color: orange;
  -webkit-animation: colorOne 1s infinite;
}
span.m {
  color: green;
  -webkit-animation: colorTwo 1s infinite;
}
span.n {
  color: chocolate;
  -webkit-animation: colorThree 1s infinite;
}
span.o {
  color: lightblue;
  -webkit-animation: colorFour 1s infinite;
}
span.p {
  color: darkgreen;
  -webkit-animation: colorFive 1s infinite;
}

@-webkit-keyframes colorOne {
  from {
    color: orange;
  }
  to {
    color: green;
  }
}
@-webkit-keyframes colorTwo {
  from {
    color: green;
  }
  to {
    color: chocolate;
  }
}
@-webkit-keyframes colorThree {
  from {
    color: chocolate;
  }
  to {
    color: lightblue;
  }
}
@-webkit-keyframes colorFour {
  from {
    color: lightblue;
  }
  to {
    color: darkgreen;
  }
}
@-webkit-keyframes colorFive {
  from {
    color: darkgreen;
  }
  to {
    color: orange;
  }
}

</style>
