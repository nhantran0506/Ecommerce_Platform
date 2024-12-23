import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { Input } from "@nextui-org/react";
import { Search } from "react-feather";

const SearchBar = ({ className = "w-10/12" }) => {
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearchSubmit = () => {
    if (searchQuery.trim()) {
      router.push(
        `/${locale}/products?search=${encodeURIComponent(searchQuery)}`
      );
    }
  };

  const handleClear = () => {
    setSearchQuery("");
    router.push(`/${locale}/products`);
  };

  return (
    <div className={className}>
      <Input
        isClearable
        radius="lg"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSearchSubmit();
          }
        }}
        classNames={{
          input: [
            "bg-transparent",
            "text-black/60 dark:text-white/90",
            "placeholder:text-default-700/50 dark:placeholder:text-white/60",
          ],
          innerWrapper: "bg-transparent",
          inputWrapper: [
            "bg-default-200/50",
            "dark:bg-default/60",
            "backdrop-blur-xl",
            "backdrop-saturate-200",
            "hover:bg-default-200/70",
            "dark:hover:bg-default/70",
            "group-data-[focus=true]:bg-default-200/50",
            "dark:group-data-[focus=true]:bg-default/60",
            "!cursor-text",
          ],
        }}
        placeholder="Type to search..."
        startContent={
          <Search className="mb-0.5 dark:text-white/90 text-black pointer-events-none flex-shrink-0" />
        }
        onClear={() => handleClear()}
      />
    </div>
  );
};

export default SearchBar;
