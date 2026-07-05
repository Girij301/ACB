import { useEffect, type PropsWithChildren } from "react";
import { useAuth } from "@clerk/clerk-react";

import api from "./client";
import { registerInterceptors } from "./interceptors";

export function ApiProvider({
  children,
}: PropsWithChildren) {
  const { getToken } = useAuth();

  useEffect(() => {
    const cleanup = registerInterceptors(
      api,
      getToken,
    );

    return cleanup;
  }, [getToken]);

  return <>{children}</>;
}