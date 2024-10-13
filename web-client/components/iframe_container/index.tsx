interface IframeContainerProps {
    title: string;
    src: string;
    height?: string;
  }
  
  export default function IframeContainer({ title, src, height = "400px" }: IframeContainerProps) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold text-gray-700 mb-4">{title}</h2>
        <iframe
          src={src}
          className="w-full border-none"
          style={{ height }}
          title={title}
        />
      </div>
    );
  }