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
} from "@nextui-org/react";
import { useState, useRef, useEffect } from "react";
import { API_BASE_URL } from "@/libraries/api";
import productAPIs from "@/api/product";

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

  const [formData, setFormData] = useState({
    product_name: "",
    product_description: "",
    price: "",
    category_id: "",
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
      const formDataToSend = new FormData();

      // Find the selected category name based on the selected category_id
      const selectedCategory = categories.find(
        (cat) => cat.category_id === formData.category_id
      );

      // Append basic product data
      formDataToSend.append("product_name", formData.product_name);
      formDataToSend.append(
        "product_description",
        formData.product_description
      );
      formDataToSend.append("price", formData.price);
      // Send the category name instead of ID
      formDataToSend.append("category", selectedCategory?.category_name || "");

      // Append image files
      selectedFiles.forEach((file) => {
        formDataToSend.append("images", file);
      });

      const token = localStorage.getItem("token");
      const response = await fetch(`${API_BASE_URL}/products/create`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formDataToSend,
      });

      if (!response.ok) {
        throw new Error(`Create product failed with status ${response.status}`);
      }

      // Close modal and reset form
      if (onOpenChange) {
        onOpenChange(false);
      }
    } catch (error) {
      console.error("Failed to create product:", error);
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
                    <Select
                      label="Category"
                      placeholder="Select category"
                      className="w-full"
                      value={formData.category_id}
                      onChange={(e) =>
                        handleInputChange("category_id", e.target.value)
                      }
                    >
                      {categories?.map(
                        (category: {
                          category_id: string;
                          category_name: string;
                        }) => (
                          <SelectItem
                            key={category.category_id}
                            value={category.category_id}
                          >
                            {category.category_name}
                          </SelectItem>
                        )
                      )}
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
                  Create Product
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
