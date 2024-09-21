export const truncateText = (str: string) => {
  return str.length > 0 ? str.substring(0, 60) + "..." : str;
};
