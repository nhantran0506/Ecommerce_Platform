import { API_BASE_URL, API_ROUTES } from "@/libraries/api";

class Order {
  async checkout(reqBody: IOrderProduct[]): Promise<IOrderResponse> {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_BASE_URL}${API_ROUTES.ORDER_PRODUCT}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(reqBody),
    });

    if (!response.ok) {
      throw new Error(`checkout failed with status ${response.status}`);
    }

    const data = await response.json() as IOrderResponse;
    return data;
  }
}

export const orderAPIs = new Order();
export default orderAPIs;
