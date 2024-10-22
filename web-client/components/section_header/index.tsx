import { Button } from "@nextui-org/react";
import { ReactNode } from "react";

interface ISectionHeader {
  title: string;
  content: ReactNode;
  action?: ReactNode;
}

const SectionHeader: React.FC<ISectionHeader> = ({
  title,
  content,
  action,
}) => {
  return (
    <div className="mb-8">
      <div className="flex justify-between mb-8">
        <h1 className="font-bold text-3xl">{title}</h1>
        {action}
      </div>
      {content}
    </div>
  );
};

export default SectionHeader;
