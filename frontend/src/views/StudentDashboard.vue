<template>
  <div class="container">

    <h1>Student Dashboard</h1>

    <button @click="loadDrives">
      Available Drives
    </button>

    <button @click="loadApplications">
      My Applications
    </button>

    <button @click="loadPlacements">
      My Placements
    </button>

    <button @click="logout">
      Logout
    </button>

    <p v-if="records.length === 0 && currentView !== ''">
      No records found
    </p>

    <table v-if="records.length > 0">

      <thead>
        <tr>

          <th
            v-for="key in headers"
            :key="key"
          >
            {{ key }}
          </th>

          <th v-if="currentView === 'drives'">
            Action
          </th>

        </tr>
      </thead>

      <tbody>

        <tr
          v-for="(record,index) in records"
          :key="index"
        >

          <td
            v-for="key in headers"
            :key="key"
          >
            {{ record[key] }}
          </td>

          <td v-if="currentView === 'drives'">

            <button
              @click="applyDrive(record.id)"
            >
              Apply
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
      records: [],
      headers: [],
      currentView: ""
    };
  },

  methods: {

    async loadDrives() {

      const token = localStorage.getItem(
        "token"
      );

      const response = await api.get(
        "/student/drives",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      console.log(
        "Drives:",
        response.data
      );

      this.records = response.data;

      this.currentView = "drives";

      if(this.records.length > 0){
        this.headers = Object.keys(
          this.records[0]
        );
      }
    },

    async loadApplications() {

      const token = localStorage.getItem(
        "token"
      );

      const response = await api.get(
        "/student/applications",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      console.log(
        "Applications:",
        response.data
      );

      this.records = response.data;

      this.currentView = "applications";

      if(this.records.length > 0){
        this.headers = Object.keys(
          this.records[0]
        );
      }
    },

    async loadPlacements() {

      const token = localStorage.getItem(
        "token"
      );

      const response = await api.get(
        "/student/placements",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      console.log(
        "Placements:",
        response.data
      );

      this.records = response.data;

      this.currentView = "placements";

      if(this.records.length > 0){
        this.headers = Object.keys(
          this.records[0]
        );
      }
    },

    async applyDrive(driveId) {

      const token = localStorage.getItem(
        "token"
      );

      try {

        const response = await api.post(
          `/student/apply/${driveId}`,
          {},
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        );

        alert(
          response.data.message
        );

      }

      catch(error) {

        if(
          error.response &&
          error.response.data.error
        ) {

          alert(
            error.response.data.error
          );

        }

        else {

          alert(
            "Application Failed"
          );
        }
      }
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
  width:900px;
  margin:auto;
  padding:20px;
}

button{
  margin-right:10px;
  padding:10px;
  margin-bottom:10px;
}

table{
  width:100%;
  border-collapse:collapse;
  margin-top:20px;
}

th,td{
  border:1px solid #ddd;
  padding:10px;
}

p{
  margin-top:20px;
  color:gray;
}
</style>