interface StatCardProps {
    title: string;
    value: string | number;
  }
  
  export default function StatCard({ title, value }: StatCardProps) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold text-gray-700 mb-2">{title}</h2>
        <p className="text-3xl font-bold text-black">{value}</p>
      </div>
    );
  }