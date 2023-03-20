<template>
  <div class="spinner">
    <div class="bouncing-loader">
    <div />
    <div />
    <div />
    </div>
  </div>
</template>

<style scoped>
.spinner {
  /* padding-top: 100px; */
  position: fixed;
  top: 50%;
  left: 0;
  width: 100%;
  height: 100%;
}
.bouncing-loader {
  display: flex;
  justify-content: center;
}
.bouncing-loader > div {
  width: 1rem;
  height: 1rem;
  margin: 3rem 0.2rem;
  background: #2596be;
  border-radius: 50%;
  animation: bouncing-loader 0.6s infinite alternate;
}
.bouncing-loader > div:nth-child(2) {
  animation-delay: 0.2s;
}
.bouncing-loader > div:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes bouncing-loader {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0.1;
    transform: translateY(-1rem);
  }
}
</style>
