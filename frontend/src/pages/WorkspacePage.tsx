import { useEffect } from "react";
import api from "@/services/api/client";

export function WorkspacePage() {
  useEffect(() => {
    async function loadMe() {
      try {
        const response = await api.get("/me");
        console.log("User:", response.data);
      } catch (error) {
        console.error(error);
      }
    }

    loadMe();
  }, []);

  return <div>Workspace</div>;
}