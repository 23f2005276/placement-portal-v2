import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

export const useCheckIdentity = () => {
  const router = useRouter();

  const route = useRoute()

  const checkIdentity = () => {
    if (route.path === "/pending" || route.path === "/blacklisted") {
      return;
    }
    fetch(`${apiUrl}/api/identity`, {
      method: "GET",
      credentials: "include",
    }).then(async (response) => {
      const jsonResponse = await response.json();
      if (response.ok) {
        localStorage.setItem("user_id", jsonResponse.user_id);
        if (!route.path.startsWith(`/${jsonResponse.role}`)) {
          router.push(`/${jsonResponse.role}`);
        }
      } else {
        if (response.status === 403 && (jsonResponse.message === "pending" || jsonResponse.message === "blacklisted")) {
          router.push(`/${jsonResponse.message}`);
        } else {
          if (!(route.path.startsWith("/signup"))) {
            localStorage.removeItem("user_id");
            router.push("/"); 
          }
        }
      }
    });
  };

  return checkIdentity;
};
