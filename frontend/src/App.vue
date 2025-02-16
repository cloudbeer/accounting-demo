<template>
  <div class="app">
    <van-nav-bar title="个人记账" fixed />
    <div class="content">
      <HomeView />
    </div>
  </div>
</template>

<script setup lang="ts">
import HomeView from './views/HomeView.vue'
</script>

<style>
.app {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.content {
  padding-top: 46px;
}

:root {
  --van-nav-bar-background: #1989fa;
  --van-nav-bar-title-text-color: #fff;
}
</style>
