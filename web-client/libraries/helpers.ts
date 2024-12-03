export const truncateText = (str: string) => {
  return str.length > 0 ? str.substring(0, 60) + "..." : str;
};

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString(); // Customize the format as needed
}
