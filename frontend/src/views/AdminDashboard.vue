<template>
  <div class="container">

    <h1>Admin Dashboard</h1>

    <div class="card">
      <h3>Total Students</h3>
      <p>{{ stats.total_students }}</p>
    </div>

    <div class="card">
      <h3>Total Companies</h3>
      <p>{{ stats.total_companies }}</p>
    </div>

    <div class="card">
      <h3>Total Drives</h3>
      <p>{{ stats.total_drives }}</p>
    </div>

    <div class="card">
      <h3>Total Applications</h3>
      <p>{{ stats.total_applications }}</p>
    </div>

    <div class="actions">
      <button @click="loadStudents">
        Students
      </button>

      <button @click="loadCompanies">
        Companies
      </button>

      <button @click="loadPlacements">
        Placements
      </button>
    </div>

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
            v-if="
              currentView === 'companies' ||
              currentView === 'students'
            "
          >
            Actions
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

          <!-- Company Actions -->

          <td v-if="currentView === 'companies'">

            <button
              v-if="
                record.approval_status === 'PENDING'
              "
              @click="
                approveCompany(record.id)
              "
            >
              Approve
            </button>

            <button
              v-if="
                record.approval_status === 'PENDING'
              "
              @click="
                rejectCompany(record.id)
              "
            >
              Reject
            </button>

            <span
              v-if="
                record.approval_status === 'APPROVED'
              "
            >
              Approved
            </span>

            <span
              v-if="
                record.approval_status === 'REJECTED'
              "
            >
              Rejected
            </span>

          </td>

          <!-- Student Actions -->

          <td v-if="currentView === 'students'">

            <button
              v-if="
                !record.is_blacklisted
              "
              @click="
                blacklistStudent(record.id)
              "
            >
              Blacklist
            </button>

            <span
              v-if="
                record.is_blacklisted
              "
            >
              Blacklisted
            </span>

          </td>

        </tr>

      </tbody>

    </table>

    <br>

    <button @click="logout">
      Logout
    </button>

  </div>
</template>

<script>
import api from "../services/api";

export default {

  data() {
    return {
      stats: {},
      records: [],
      headers: [],
      currentView: ""
    };
  },

  async mounted() {

    const token =
      localStorage.getItem("token");

    const response =
      await api.get(
        "/admin/dashboard",
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

    this.stats =
      response.data;
  },

  methods: {

    async loadStudents() {

      const token =
        localStorage.getItem("token");

      const response =
        await api.get(
          "/admin/students",
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
        "students";

      if(this.records.length > 0){

        this.headers =
          Object.keys(
            this.records[0]
          );
      }
    },

    async loadCompanies() {

      const token =
        localStorage.getItem("token");

      const response =
        await api.get(
          "/admin/companies",
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
        "companies";

      if(this.records.length > 0){

        this.headers =
          Object.keys(
            this.records[0]
          );
      }
    },

    async loadPlacements() {

      const token =
        localStorage.getItem("token");

      const response =
        await api.get(
          "/admin/placements",
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
        "placements";

      if(this.records.length > 0){

        this.headers =
          Object.keys(
            this.records[0]
          );
      }
    },

    async approveCompany(companyId) {

      const token =
        localStorage.getItem("token");

      await api.put(
        `/admin/company/${companyId}/approve`,
        {},
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Company Approved"
      );

      this.loadCompanies();
    },

    async rejectCompany(companyId) {

      const token =
        localStorage.getItem("token");

      await api.put(
        `/admin/company/${companyId}/reject`,
        {},
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Company Rejected"
      );

      this.loadCompanies();
    },

    async blacklistStudent(studentId) {

      const token =
        localStorage.getItem("token");

      await api.put(
        `/admin/student/${studentId}/blacklist`,
        {},
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      alert(
        "Student Blacklisted"
      );

      this.loadStudents();
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

.card{
  border:1px solid #ddd;
  padding:15px;
  margin-bottom:10px;
  border-radius:8px;
}

.actions{
  margin:20px 0;
}

button{
  margin-right:10px;
  padding:10px 15px;
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