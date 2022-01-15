
export const getTimeFromStringDate = (stringDate) => {
  let date = new Date(stringDate);
  return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
};