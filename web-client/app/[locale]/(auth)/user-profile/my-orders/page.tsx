import OrderCard, { IOrderItem } from "@/components/order_card";
import SectionHeader from "@/components/section_header";
import { listOrderItem } from "@/data/data";

const MyOrdersPage = () => {
  return (
    <SectionHeader
      title={"Order History"}
      content={
        <div className="grid grid-cols-2 gap-4">
          {listOrderItem.map((item, index) => (
            <OrderCard
              key={index}
              index={item.id}
              status={item.status}
              listOrderItem={item.listOrderItem}
              createdAt={""}
            />
          ))}
        </div>
      }
    />
  );
};

export default MyOrdersPage;
