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
}

export const authAPIs = new Auth();
export default authAPIs;
