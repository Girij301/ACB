import { api } from "@/services/api";

import type {
  ListDirectoryRequest,
  ListDirectoryResponse,
  ReadFileResponse,
  WorkspaceResponse,
} from "./types";


export class WorkspaceService {

  static async listDirectory(
    payload: ListDirectoryRequest = {},
  ): Promise<
    WorkspaceResponse<ListDirectoryResponse>
  > {

    const response =
      await api.post<
        WorkspaceResponse<ListDirectoryResponse>
      >(
        "/files/list",
        payload,
      );


    return response.data;
  }


  static async readFile(
    path: string,
  ): Promise<
    WorkspaceResponse<ReadFileResponse>
  > {

    const response =
      await api.post<
        WorkspaceResponse<ReadFileResponse>
      >(
        "/files/read",
        {
          path,
        },
      );


    return response.data;
  }
}