import { API_BASE_URL, API_ROUTES } from "@/libraries/api";

class Auth {
  async login(reqBody: IReqLogin): Promise<IResLogin> {
    const response = await fetch(`${API_BASE_URL}${API_ROUTES.LOGIN}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(reqBody),
    });

    if (!response.ok) {
      throw new Error(`Login failed with status ${response.status}`);
    }

    const data = (await response.json()) as IResLogin;
    return data;
  }

  async getCurrentUser(): Promise<IResGetUser> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_CURRENT_USER}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`getCurrentUser failed with status ${response.status}`);
    }

    const data = (await response.json()) as IResGetUser;
    return data;
  }

  async updateCurrentUser(reqBody: IReqUpdateUser): Promise<any> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.UPDATE_CURRENT_USER}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(reqBody),
      }
    );

    if (!response.ok) {
      throw new Error(
        `updateCurrentUser failed with status ${response.status}`
      );
    }

    const data = (await response.json()) as any;
    return data;
  }
}

export const authAPIs = new Auth();
export default authAPIs;
