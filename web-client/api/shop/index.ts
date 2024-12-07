import { API_BASE_URL, API_ROUTES } from "@/libraries/api";

class Shop {
  async createShop(reqBody: IReqCreateShop): Promise<any> {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_BASE_URL}${API_ROUTES.CREATE_SHOP}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(reqBody),
    });

    if (!response.ok) {
      throw new Error(`createShop failed with status ${response.status}`);
    }

    const data = (await response.json()) as any;
    return data;
  }

  async getShopInfo(id: string): Promise<any> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_SHOP}/${id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        // body: JSON.stringify(),
      }
    );

    if (!response.ok) {
      throw new Error(`createShop failed with status ${response.status}`);
    }

    const data = (await response.json()) as any;
    return data;
  }
}

export const shopAPIs = new Shop();
export default shopAPIs;
