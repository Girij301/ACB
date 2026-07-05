import type {
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";

type GetToken = () => Promise<string | null>;

export function registerInterceptors(
  api: AxiosInstance,
  getToken: GetToken,
) {
  const requestInterceptor = api.interceptors.request.use(
    async (
      config: InternalAxiosRequestConfig,
    ) => {
      const token = await getToken();

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    },
  );

  const responseInterceptor = api.interceptors.response.use(
    (response) => response,
    (error) => Promise.reject(error),
  );

  

  return () => {
    api.interceptors.request.eject(requestInterceptor);
    api.interceptors.response.eject(responseInterceptor);
  };
}