import { ReactNode } from "react";

interface ISectionHeader {
  title: string;
  content: ReactNode;
}

const SectionHeader: React.FC<ISectionHeader> = ({ title, content }) => {
  return (
    <div className="mb-8">
      <p className="text-xl font-semibold mb-8">{title}</p>
      {content}
    </div>
  );
};

export default SectionHeader;
