import { useRoute, useRouter } from "vue-router";

const apiUrl = import.meta.env.VITE_API_BASE_URL;

export const useCheckIdentity = () => {
  const router = useRouter();

  const route = useRoute()

  const checkIdentity = () => {
    fetch(`${apiUrl}/api/identity`, {
      method: "GET",
      credentials: "include",
    }).then(async (response) => {
      const jsonResponse = await response.json();
      if (response.ok) {
        router.push(`/${jsonResponse.role}`);
      } else {
        if (!(route.path.startsWith("/signup"))) {
          router.push("/"); 
        }
      }
    });
  };

  return checkIdentity;
};
