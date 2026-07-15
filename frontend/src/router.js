import { createRouter, createWebHistory } from "vue-router";
import Signup from "./pages/Signup.vue";
import Login from "./pages/Login.vue";
import Error from "./pages/Error.vue";
import Admin from "./pages/Admin.vue";
import Pending from "./pages/Pending.vue";
import Blacklisted from "./pages/Blacklisted.vue";
import Company from "./pages/Company.vue";

import Student from "./pages/Student.vue";

const routes = [
  {
    path: "/signup/:category?",
    component: Signup,
    props: true,
  },
  {
    path: "/login",
    component: Login,
  },
  {
    path: "/",
    component: Login,
  },
  {
    path: "/Error/:status?/:message?",
    component: Error,
    props: true 
  },
  {
    path: "/admin/:page?",
    component: Admin,
    props: true
  },
  {
    path: "/pending",
    component: Pending
  },
  {
    path: "/blacklisted",
    component: Blacklisted
  },
  {
    path: "/company_hr/:page?/:action?",
    component: Company,
    props: true
  },
  {
    path: "/student/:page?/:action?",
    component: Student,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
