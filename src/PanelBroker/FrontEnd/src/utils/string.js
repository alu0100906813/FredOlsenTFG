
const CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789';

export const capitalize = (stringToCapitalize) => {
  return stringToCapitalize[0].toUpperCase() + stringToCapitalize.substring(1, stringToCapitalize.length);
};

export const randomString = (length = 5) => {
  let result = '';
  while (result.length < length) {
    const randomIndex = Math.trunc(Math.random() * 100000) % CHARS.length;
    result = result + CHARS[randomIndex];
  }
  return result;
}