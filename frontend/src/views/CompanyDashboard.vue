<template>
  <div class="container">

    <h1>Company Dashboard</h1>

    <h3>Create Drive</h3>

    <input v-model="title" placeholder="Title">
    <input v-model="description" placeholder="Description">
    <input v-model="salary" placeholder="Salary">
    <input v-model="required_skills" placeholder="Skills">
    <input v-model="eligibility_branch" placeholder="Branch">
    <input v-model="minimum_cgpa" placeholder="CGPA">
    <input v-model="eligible_year" placeholder="Year">

    <br><br>

    <button @click="createDrive">
      Create Drive
    </button>

    <button @click="loadDrives">
      My Drives
    </button>

    <button @click="loadApplications">
      Applications
    </button>

    <button @click="logout">
      Logout
    </button>

    <br><br>

    <table v-if="records.length > 0">

      <thead>
        <tr>

          <th
            v-for="key in headers"
            :key="key"
          >
            {{ key }}
          </th>

          <th
            v-if="currentView==='applications'"
          >
            Actions
          </th>

        </tr>
      </thead>

      <tbody>

        <tr
          v-for="record in records"
          :key="record.id"
        >

          <td
            v-for="key in headers"
            :key="key"
          >
            {{ record[key] }}
          </td>

          <td
            v-if="currentView==='applications'"
          >

            <button
              @click="shortlist(record.application_id)"
            >
              Shortlist
            </button>

            <button
              @click="reject(record.application_id)"
            >
              Reject
            </button>

            <button
              @click="select(record.application_id)"
            >
              Select
            </button>

          </td>

        </tr>

      </tbody>

    </table>

  </div>
</template>

<script>
import api from "../services/api";

export default {

  data() {
    return {

      title: "",
      description: "",
      salary: "",
      required_skills: "",
      eligibility_branch: "",
      minimum_cgpa: "",
      eligible_year: "",

      records: [],
      headers: [],
      currentView: ""
    };
  },

  methods: {

    async createDrive() {

      const token =
        localStorage.getItem("token");

      try {

        await api.post(
          "/company/drives",
          {
            title: this.title,
            description: this.description,
            salary: this.salary,
            required_skills: this.required_skills,
            eligibility_branch:
              this.eligibility_branch,
            minimum_cgpa:
              this.minimum_cgpa,
            eligible_year:
              this.eligible_year
          },
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        );

        alert(
          "Drive Created"
        );

      } catch(error) {

        alert(
          error.response.data.error
        );
      }
    },

    async loadDrives() {

      const token =
        localStorage.getItem("token");

      const response =
        await api.get(
          "/company/drives",
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        );

      this.records =
        response.data;

      this.currentView =
        "drives";

      if(this.records.length > 0){

        this.headers =
          Object.keys(
            this.records[0]
          );
      }
    },

    async loadApplications() {

      const token =
        localStorage.getItem("token");

      const response =
        await api.get(
          "/company/applications",
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        );

      this.records =
        response.data;

      this.currentView =
        "applications";

      if(this.records.length > 0){

        this.headers =
          Object.keys(
            this.records[0]
          );
      }
    },

    async shortlist(id) {

      const token =
        localStorage.getItem("token");

      await api.put(
        `/company/application/${id}/shortlist`,
        {},
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Shortlisted"
      );
    },

    async reject(id) {

      const token =
        localStorage.getItem("token");

      await api.put(
        `/company/application/${id}/reject`,
        {},
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Rejected"
      );
    },

    async select(id) {

      const token =
        localStorage.getItem("token");

      await api.put(
        `/company/application/${id}/select`,
        {},
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Candidate Selected"
      );
    },

    logout() {

      localStorage.clear();

      this.$router.push("/");
    }
  }
};
</script>

<style>
.container{
  width:1000px;
  margin:auto;
  padding:20px;
}

input{
  width:100%;
  margin-bottom:10px;
  padding:10px;
}

button{
  margin-right:10px;
  padding:10px;
}

table{
  width:100%;
  border-collapse:collapse;
}

th,td{
  border:1px solid #ddd;
  padding:10px;
}
</style>