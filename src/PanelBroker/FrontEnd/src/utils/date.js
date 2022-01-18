
export const getTimeFromStringDate = (stringDate) => {
  let date = new Date(stringDate);
  const addZeroIfLess10 = (numberToAdd) => {
    return numberToAdd <= 9 ? '0' + numberToAdd : numberToAdd;
  }
  return `${addZeroIfLess10(date.getHours())}:${addZeroIfLess10(date.getMinutes())}:${addZeroIfLess10(date.getSeconds())}`;
};