<template>
  <div id="app">
    <el-menu mode="horizontal">
      <el-menu-item index="1">
        <router-link to="/eve">测评结果</router-link>
      </el-menu-item>
      <el-menu-item index="2">
        <router-link to="/human">人工评测</router-link>
      </el-menu-item>
      <el-menu-item index="3">
        <router-link to="/add">问题管理</router-link>
      </el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>
