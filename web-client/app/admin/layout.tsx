import AdminSidebar from "@/components/admin_sidebar";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex">
      <AdminSidebar />
      <div className="flex-1 ml-64 p-8">
        {children}
      </div>
    </div>
  );
}

