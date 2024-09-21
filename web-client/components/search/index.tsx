import { Input } from "@nextui-org/react";
import { Search } from "react-feather";

const SearchBar = () => {
  return (
    <div className="w-10/12">
      <Input
        isClearable
        radius="lg"
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
          <Search className=" mb-0.5 dark:text-white/90 text-black pointer-events-none flex-shrink-0" />
        }
      />
    </div>
  );
};

export default SearchBar;
