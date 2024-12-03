import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import { IOrderHistory } from "@/interface/Data/IOrderData";

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
      throw new Error(`Failed to checkout with status ${response.status}`);
    }

    const data = await response.json();
    return data;
  }

  async getOrderHistory(): Promise<IOrderHistory[]> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_ORDER_HISTORY}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(
        `Failed to fetch order history with status ${response.status}`
      );
    }

    const data = await response.json();
    return data;
  }

  async getOrderById(orderId: string): Promise<IOrderDetails> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_ORDER_BY_ID}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ order_id: orderId }),
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch order with status ${response.status}`);
    }

    const data = await response.json();
    return data;
  }

  async restoreOrder(orderId: string): Promise<void> {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_BASE_URL}${API_ROUTES.RESTORE_ORDER}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ order_id: orderId }),
    });

    if (!response.ok) {
      throw new Error(`Failed to restore order with status ${response.status}`);
    }
  }
}

const orderAPIs = new Order();
export default orderAPIs;
