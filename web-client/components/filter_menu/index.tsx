import { useState } from "react";
import { Checkbox, Slider } from "@nextui-org/react";

interface FilterMenuProps {
  onFilterChange: (filters: FilterOptions) => void;
  categories: ICategory[];
}

interface FilterOptions {
  categories: string[];
  priceRange: [number, number];
  minRating: number;
}

const FilterMenu: React.FC<FilterMenuProps> = ({
  onFilterChange,
  categories,
}) => {
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 1000]);
  const [minRating, setMinRating] = useState<number>(0);

  const handleCategoryChange = (categoryName: string, isSelected: boolean) => {
    const newSelectedCategories = isSelected
      ? [...selectedCategories, categoryName]
      : selectedCategories.filter((cat) => cat !== categoryName);

    setSelectedCategories(newSelectedCategories);
    emitFilterChange(newSelectedCategories, priceRange, minRating);
  };

  const handlePriceRangeChange = (value: number[]) => {
    const newRange: [number, number] = [value[0], value[1]];
    setPriceRange(newRange);
    emitFilterChange(selectedCategories, newRange, minRating);
  };

  const handleRatingChange = (value: number) => {
    setMinRating(value);
    emitFilterChange(selectedCategories, priceRange, value);
  };

  const emitFilterChange = (
    categories: string[],
    price: [number, number],
    rating: number
  ) => {
    onFilterChange({
      categories,
      priceRange: price,
      minRating: rating,
    });
  };

  return (
    <div className="w-48 border rounded-lg p-4 h-fit">
      <h2 className="text-lg font-bold mb-4">FILTER</h2>

      {/* Categories Section */}
      <div className="mb-6">
        <h3 className="font-medium mb-2">Categories</h3>
        <div className="flex flex-col gap-2">
          {categories.map((category) => (
            <Checkbox
              key={category.category_id}
              size="sm"
              onChange={(e) =>
                handleCategoryChange(category.category_name, e.target.checked)
              }
            >
              {category.category_name}
            </Checkbox>
          ))}
        </div>
      </div>

      {/* Price Range Section */}
      <div className="mb-6">
        <h3 className="font-medium mb-2">Price Range</h3>
        <Slider
          label="Price"
          step={50}
          minValue={0}
          maxValue={1000}
          value={priceRange}
          onChange={(value) => handlePriceRangeChange(value as number[])}
          className="max-w-md"
          formatOptions={{ style: "currency", currency: "USD" }}
        />
        <div className="text-sm mt-2">
          ${priceRange[0]} - ${priceRange[1]}
        </div>
      </div>

      {/* Rating Section */}
      <div className="mb-6">
        <h3 className="font-medium mb-2">Minimum Rating</h3>
        <Slider
          label="Stars"
          step={1}
          minValue={0}
          maxValue={5}
          value={minRating}
          onChange={(value) => handleRatingChange(value as number)}
          className="max-w-md"
          marks={[
            { value: 0, label: "0★" },
            { value: 5, label: "5★" },
          ]}
        />
      </div>
    </div>
  );
};

export default FilterMenu;
