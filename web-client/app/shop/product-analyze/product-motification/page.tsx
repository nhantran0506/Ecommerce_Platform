"use client";
import { InputTypeEnum } from "@/constant/enum";
import { IProductMotificationPage } from "@/interface/UI/IProductPage";
import { IInputItem } from "@/interface/UI/IProfile";
import { useProductId } from "@/state/state";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Input,
  Textarea,
} from "@nextui-org/react";

const ProductMotificationPage: React.FC<IProductMotificationPage> = ({
  isOpen,
  onOpenChange,
}) => {
  const { productId } = useProductId();

  // TODO: Fetch data using productId

  const listFormInput: IInputItem[] = [
    {
      type: InputTypeEnum.text,
      label: "Product name",
      placeholder: "Enter product name",
      value: productId != "" ? `Product Name with ${productId}` : "",
    },
    {
      type: InputTypeEnum.number,
      label: "Price",
      placeholder: "0.00",
      value: productId != "" ? 10 : 0,
    },
    {
      type: InputTypeEnum.textarea,
      label: "Description",
      placeholder: "Enter description",
      value: productId != "" ? `Product description with ${productId}` : "",
    },
  ];

  return (
    <div>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center">
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1 font-bold text-2xl">
                {productId != "" ? "Update Product" : "New Product"}
              </ModalHeader>
              <ModalBody>
                <div className="grid grid-cols-2 gap-4">
                  {listFormInput.map((item, index) => (
                    <div
                      key={index}
                      className={`mb-4 ${
                        listFormInput.length % 2 !== 0 &&
                        index === listFormInput.length - 1
                          ? "col-span-2"
                          : ""
                      }`}
                    >
                      {item.type == InputTypeEnum.textarea ? (
                        <Textarea
                          label={item.label}
                          placeholder={item.placeholder}
                          className="w-full font-bold"
                          labelPlacement="outside"
                          value={item.value?.toString()}
                        />
                      ) : (
                        <Input
                          autoFocus
                          variant="bordered"
                          type={item.type}
                          label={item.label}
                          value={item.value?.toString()}
                          placeholder={item.placeholder}
                          labelPlacement={"outside"}
                          isClearable={item.type == InputTypeEnum.text}
                          className="font-bold"
                          endContent={
                            item.type == InputTypeEnum.number ? (
                              <div className="pointer-events-none flex items-center font-normal">
                                <span className="text-default-400 text-small">
                                  VND
                                </span>
                              </div>
                            ) : null
                          }
                        />
                      )}
                    </div>
                  ))}
                </div>
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
                <Button color="primary" onPress={onClose}>
                  Apply
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
};

export default ProductMotificationPage;
