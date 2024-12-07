"use client";
import { InputTypeEnum } from "@/constant/enum";
import { IProductMotificationPage } from "@/interface/UI/IProductPage";
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
  Chip,
  Select,
  SelectItem,
  useDisclosure,
} from "@nextui-org/react";
import { useState, useRef, useEffect } from "react";
import { API_BASE_URL , API_ROUTES} from "@/libraries/api";
import productAPIs from "@/api/product";
import { CircleCheck } from "lucide-react";

interface ICategory {
  category_id: string; // e.g. "cd621c55-04a6-482c-9b4e-dc356231d49f"
  category_name: string; // e.g. "SHIRT"
}

const ProductMotificationPage: React.FC<IProductMotificationPage> = ({
  isOpen,
  onOpenChange,
}) => {
  const { productId } = useProductId();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { 
    isOpen: isSuccessOpen, 
    onOpen: onSuccessOpen, 
    onOpenChange: onSuccessOpenChange 
  } = useDisclosure();

  const [formData, setFormData] = useState({
    product_name: "",
    product_description: "",
    price: "",
    category_id: "",
    inventory: "",
  });
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState<ICategory[]>([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await productAPIs.getAllCategories();
        setCategories(response);
      } catch (error) {
        console.error("Failed to fetch categories:", error);
      }
    };

    fetchCategories();
  }, []);

  useEffect(() => {
    const fetchProductDetails = async () => {
      if (!productId) return;
      
      try {
        setLoading(true);
        const product = await productAPIs.getProductById(productId);
        setFormData({
          product_name: product.product_name,
          product_description: product.product_description,
          price: product.price.toString(),
          category_id: product.product_category[0] || "",
          inventory: product.inventory.toString(),
        });
      } catch (error) {
        console.error("Failed to fetch product details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProductDetails();
  }, [productId]);

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setSelectedFiles(Array.from(files));
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      
      if (!formData.product_name || !formData.price || !formData.category_id) {
        throw new Error("Please fill in all required fields");
      }

      const formDataToSend = new FormData();

      const selectedCategory = categories.find(cat => cat.category_id === formData.category_id);
      const categoryName = selectedCategory ? selectedCategory.category_name : '';

      formDataToSend.append('product_name', formData.product_name);
      formDataToSend.append('product_description', formData.product_description);
      formDataToSend.append('price', formData.price);
      formDataToSend.append('inventory', formData.inventory);
      formDataToSend.append('category', categoryName);

      if (productId) {
        formDataToSend.append('product_id', productId);
      } else if (selectedFiles.length === 0) {
        return;
      }

      selectedFiles.forEach((file) => {
        formDataToSend.append('images', file);
      });

      const endpoint = productId 
        ? `${API_BASE_URL}${API_ROUTES.UPDATE_PRODUCT}`
        : `${API_BASE_URL}${API_ROUTES.CREATE_PRODUCT}`;

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: formDataToSend,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Operation failed with status ${response.status}`);
      }

      setFormData({
        product_name: "",
        product_description: "",
        price: "",
        category_id: "",
        inventory: "",
      });
      setSelectedFiles([]);
      
      onSuccessOpen();
      if (onOpenChange) {
        onOpenChange(false);
      }
    } catch (error) {
      console.error('Failed to process product:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Modal
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        placement="top-center"
        size="2xl"
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1 font-bold text-2xl">
                {productId != "" ? "Update Product" : "New Product"}
              </ModalHeader>
              <ModalBody>
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <Input
                      label="Product Name"
                      placeholder="Enter product name"
                      value={formData.product_name}
                      onChange={(e) =>
                        handleInputChange("product_name", e.target.value)
                      }
                      className="w-full"
                    />
                  </div>

                  <div className="col-span-1">
                    <Input
                      type="number"
                      label="Price"
                      placeholder="0.00"
                      value={formData.price}
                      onChange={(e) =>
                        handleInputChange("price", e.target.value)
                      }
                      startContent={
                        <div className="pointer-events-none flex items-center">
                          <span className="text-default-400 text-small">$</span>
                        </div>
                      }
                    />
                  </div>

                  <div className="col-span-1">
                    <Input
                      type="number"
                      label="Inventory"
                      placeholder="0"
                      value={formData.inventory}
                      onChange={(e) => handleInputChange("inventory", e.target.value)}
                      className="w-full"
                    />
                  </div>

                  <div className="col-span-1">
                    <Select
                      label="Category"
                      placeholder="Select category"
                      className="w-full"
                      value={formData.category_id}
                      onChange={(e) => handleInputChange("category_id", e.target.value)}
                    >
                      {categories?.map((category) => (
                        <SelectItem
                          key={category.category_id}
                          value={category.category_name}
                        >
                          {category.category_name}
                        </SelectItem>
                      ))}
                    </Select>
                  </div>

                  <div className="col-span-2">
                    <Textarea
                      label="Description"
                      placeholder="Enter product description"
                      value={formData.product_description}
                      onChange={(e) =>
                        handleInputChange("product_description", e.target.value)
                      }
                      className="w-full"
                    />
                  </div>

                  <div className="col-span-2">
                    <input
                      type="file"
                      multiple
                      ref={fileInputRef}
                      onChange={handleFileChange}
                      className="hidden"
                      accept="image/*"
                    />
                    <Button
                      color="primary"
                      variant="bordered"
                      onPress={() => fileInputRef.current?.click()}
                    >
                      Upload Images
                    </Button>
                    <div className="flex gap-2 mt-2">
                      {selectedFiles.map((file, index) => (
                        <Chip key={index} className="capitalize">
                          {file.name}
                        </Chip>
                      ))}
                    </div>
                  </div>
                </div>
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
                <Button
                  color="primary"
                  onPress={handleSubmit}
                  isLoading={loading}
                >
                  {productId ? 'Update Product' : 'Create Product'}
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>

      <Modal isOpen={isSuccessOpen} onOpenChange={onSuccessOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex mb-1 gap-2 items-center text-2xl">
                Success <CircleCheck color="green" size={30} />
              </ModalHeader>
              <ModalBody className="mb-2">
                <div>{productId ? "Product updated successfully!" : "Product created successfully!"}</div>
              </ModalBody>
              <ModalFooter>
                <Button color="primary" onPress={onClose}>
                  Ok
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
