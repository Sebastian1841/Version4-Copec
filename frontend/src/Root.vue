<template>
    <component :is="loggedIn ? 'App' : 'Login'" @authenticated="loggedIn = true" />
  </template>
  
  <script>
  import Login from './Views/Login.vue';
  import App   from './App.vue';
  
  export default {
    name: 'Root',
    components: { Login, App },
    data() {
      return { loggedIn: false };
    }
  };
  </script>