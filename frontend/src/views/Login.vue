<template>
  <div class="container">

    <h1>Placement Portal</h1>

    <input
      v-model="email"
      placeholder="Email"
    />

    <input
      v-model="password"
      type="password"
      placeholder="Password"
    />

    <button @click="login">
      Login
    </button>
    <p>
      New User?
      <router-link to="/register">
        Register Here
      </router-link>
    </p>

  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },

  methods: {
    async login() {

      try {

        const response = await api.post(
          "/auth/login",
          {
            email: this.email,
            password: this.password
          }
        );

        localStorage.setItem(
          "token",
          response.data.access_token
        );

        localStorage.setItem(
          "role",
          response.data.role
        );

        if (
          response.data.role === "ADMIN"
        ) {
          this.$router.push("/admin");
        }

        else if (
          response.data.role === "COMPANY"
        ) {
          this.$router.push("/company");
        }

        else {
          this.$router.push("/student");
        }

      } catch {

        alert("Login Failed");

      }
    }
  }
};
</script>

<style>
.container{
  width:300px;
  margin:100px auto;
}

input{
  width:100%;
  margin-bottom:10px;
  padding:10px;
}

button{
  padding:10px;
  width:100%;
}
</style>