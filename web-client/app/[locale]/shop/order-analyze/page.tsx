import OrderCard, { IOrderItem } from "@/components/order_card";
import SectionHeader from "@/components/section_header";
import { listOrderItem } from "@/data/data";

const OrderAnalyzePage = () => {
  return (
    <SectionHeader
      title={"Order History"}
      content={
        <div className="grid grid-cols-2 gap-4">
          {listOrderItem.map((item, index) => (
            <OrderCard
              key={index}
              id={item.id}
              status={item.status}
              listOrderItem={item.listOrderItem}
            />
          ))}
        </div>
      }
    />
  );
};

export default OrderAnalyzePage;
