
export const truncDecimals = (numberToTrunc, numberOfDecimals = 2) => {
  return Math.round(numberToTrunc * 10**numberOfDecimals) / 10**numberOfDecimals;
}