import { createRouter, createWebHistory } from "vue-router";
import Signup from "./pages/Signup.vue";
import Login from "./pages/Login.vue";
import Error from "./pages/Error.vue";
import Admin from "./pages/Admin.vue";

const routes = [
  {
    path: "/signup/:category?", // this ? is passed for optional path parameters in Vue
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
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
