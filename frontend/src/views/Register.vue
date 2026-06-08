
<template>
  <div class="container">

    <h1>Register</h1>

    <select v-model="role">
      <option value="STUDENT">Student</option>
      <option value="COMPANY">Company</option>
    </select>

    <br><br>

    <input v-model="email" placeholder="Email">

    <br><br>

    <input
      v-model="password"
      type="password"
      placeholder="Password"
    >

    <br><br>

    <div v-if="role === 'STUDENT'">

      <input v-model="name" placeholder="Name">

      <br><br>

      <input
        v-model="register_number"
        placeholder="Register Number"
      >

      <br><br>

      <input
        v-model="branch"
        placeholder="Branch"
      >

      <br><br>

      <input
        v-model="cgpa"
        placeholder="CGPA"
      >

      <br><br>

      <input
        v-model="year"
        placeholder="Year"
      >

      <br><br>

      <input
        v-model="phone"
        placeholder="Phone"
      >

    </div>

    <div v-if="role === 'COMPANY'">

      <input
        v-model="company_name"
        placeholder="Company Name"
      >

      <br><br>

      <input
        v-model="industry"
        placeholder="Industry"
      >

      <br><br>

      <input
        v-model="location"
        placeholder="Location"
      >

      <br><br>

      <input
        v-model="website"
        placeholder="Website"
      >

      <br><br>

      <input
        v-model="hr_contact"
        placeholder="HR Contact"
      >

    </div>

    <br><br>

    <button @click="register">
      Register
    </button>

  </div>
</template>

<script>
import api from "../services/api";

export default {

  data() {
    return {

      role: "STUDENT",

      email: "",
      password: "",

      name: "",
      register_number: "",
      branch: "",
      cgpa: "",
      year: "",
      phone: "",

      company_name: "",
      industry: "",
      location: "",
      website: "",
      hr_contact: ""
    };
  },

  methods: {

    async register() {

      try {

        if(this.role === "STUDENT") {

          await api.post(
            "/auth/register/student",
            {
              email: this.email,
              password: this.password,
              name: this.name,
              register_number: this.register_number,
              branch: this.branch,
              cgpa: this.cgpa,
              year: this.year,
              phone: this.phone
            }
          );
        }

        else {

          await api.post(
            "/auth/register/company",
            {
              email: this.email,
              password: this.password,
              company_name: this.company_name,
              industry: this.industry,
              location: this.location,
              website: this.website,
              hr_contact: this.hr_contact
            }
          );
        }

        alert("Registration Successful");

        this.$router.push("/");

      } catch(error) {

        alert("Registration Failed");
      }
    }
  }
};
</script>

<style>
.container{
  width:400px;
  margin:auto;
  padding:20px;
}

input,select{
  width:100%;
  padding:10px;
}
</style>