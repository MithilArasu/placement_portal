import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import CompanyDashboard from "../views/CompanyDashboard.vue";
import AdminDashboard from "../views/AdminDashboard.vue";

const routes = [
  { path: "/", component: Login },
  { path: "/student", component: StudentDashboard },
  { path: "/company", component: CompanyDashboard },
  { path: "/admin", component: AdminDashboard }
];

export default createRouter({
  history: createWebHistory(),
  routes
});